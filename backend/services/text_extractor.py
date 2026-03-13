import re
import os
import sys
import logging
import subprocess
import tempfile
import numpy as np

import pdfplumber
import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)

# ── Tesseract Initialization ──────────────────────────────────────────────────
_TESSERACT_CMD = None
_TESSERACT_INITIALIZED = False


def _find_tesseract():
    """Find and initialize Tesseract OCR engine."""
    global _TESSERACT_CMD, _TESSERACT_INITIALIZED

    if _TESSERACT_INITIALIZED:
        return _TESSERACT_CMD

    _TESSERACT_INITIALIZED = True

    # 1. Try custom path from .env TESSERACT_CMD (highest priority)
    env_cmd = os.environ.get("TESSERACT_CMD")
    if env_cmd:
        print(f"[TESS] Checking TESSERACT_CMD from .env: {env_cmd}")
        if os.path.isfile(env_cmd):
            try:
                result = subprocess.run([env_cmd, "--version"], capture_output=True, timeout=5)
                if result.returncode == 0:
                    print(f"[TESS] Found Tesseract at: {env_cmd}")
                    _TESSERACT_CMD = env_cmd
                    pytesseract.pytesseract.tesseract_cmd = env_cmd  # set immediately
                    _setup_environment(env_cmd)
                    return _TESSERACT_CMD
            except Exception as e:
                print(f"[TESS] TESSERACT_CMD failed: {e}")

    # 2. Try standard Windows locations
    if sys.platform == "win32":
        candidates = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
            os.path.expandvars(r"%ProgramFiles%\Tesseract-OCR\tesseract.exe"),
        ]
        for path in candidates:
            if os.path.isfile(path):
                try:
                    result = subprocess.run([path, "--version"], capture_output=True, timeout=5)
                    if result.returncode == 0:
                        print(f"[TESS] Found Tesseract at: {path}")
                        _TESSERACT_CMD = path
                        pytesseract.pytesseract.tesseract_cmd = path  # set immediately
                        _setup_environment(path)
                        return _TESSERACT_CMD
                except Exception as e:
                    print(f"[TESS] Path invalid {path}: {e}")

    # 3. Try system PATH
    try:
        result = subprocess.run(["tesseract", "--version"], capture_output=True, timeout=5)
        if result.returncode == 0:
            print(f"[TESS] Found Tesseract in system PATH")
            _TESSERACT_CMD = "tesseract"
            pytesseract.pytesseract.tesseract_cmd = "tesseract"
            return _TESSERACT_CMD
    except Exception:
        pass

    print("[TESS] Tesseract NOT FOUND")
    return None


def _setup_environment(tess_path: str):
    """Configure environment variables for Tesseract."""
    tess_dir = os.path.dirname(tess_path)
    if tess_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = tess_dir + os.pathsep + os.environ.get("PATH", "")
    tessdata_dir = os.path.join(tess_dir, "tessdata")
    if os.path.isdir(tessdata_dir):
        os.environ["TESSDATA_PREFIX"] = tessdata_dir
        print(f"[TESS] TESSDATA_PREFIX set to: {tessdata_dir}")
    else:
        print(f"[TESS] Warning: tessdata dir not found at {tessdata_dir}")


def get_tesseract_status():
    """Return diagnostic information about Tesseract setup."""
    if not _TESSERACT_INITIALIZED:
        _find_tesseract()
    return {
        "tesseract_found": _TESSERACT_CMD is not None,
        "tesseract_path": _TESSERACT_CMD,
        "pytesseract_cmd": pytesseract.pytesseract.tesseract_cmd,
        "tessdata_prefix": os.environ.get("TESSDATA_PREFIX"),
        "env_tesseract_cmd": os.environ.get("TESSERACT_CMD"),
        "platform": sys.platform,
    }


def _ensure_tesseract():
    """
    Guarantee pytesseract.tesseract_cmd is set before every OCR call.
    This is the core fix for 'tesseract not in PATH' errors on Windows.
    Called defensively at the top of EVERY function that touches Tesseract.
    """
    global _TESSERACT_CMD
    if not _TESSERACT_CMD:
        _find_tesseract()
    if not _TESSERACT_CMD:
        raise RuntimeError(
            "Tesseract OCR engine not found.\n"
            "Install from: https://github.com/UB-Mannheim/tesseract/wiki\n"
            "Then set TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe in your .env"
        )
    # Always re-set — prevents other libraries from overwriting it
    pytesseract.pytesseract.tesseract_cmd = _TESSERACT_CMD


# Initialize immediately at module load — before anything else
_TESSERACT_CMD = _find_tesseract()


# ── Optional heavy dependencies ───────────────────────────────────────────────
try:
    import cv2
    _HAVE_CV2 = True
except ImportError:
    _HAVE_CV2 = False
    logger.warning("opencv-python not installed — image preprocessing disabled")

try:
    from pdf2image import convert_from_path
    _HAVE_PDF2IMAGE = True
except ImportError:
    _HAVE_PDF2IMAGE = False
    logger.warning("pdf2image not installed — image-PDF fallback disabled")


# ── Helpers ───────────────────────────────────────────────────────────────────

def allowed_file(filename: str, allowed: set) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed


def _safe_open_image(file_path: str) -> Image.Image:
    """
    Open any image file and return a clean RGB PIL Image.

    Screenshots from Windows (Snipping Tool, PrtSc, etc.) are saved as
    RGBA or Palette-mode PNGs.  cv2 and Tesseract both crash on those unless
    they are normalised to plain RGB first.

    Mode handling:
      P    (palette)      → convert via RGBA to preserve transparency
      RGBA (with alpha)   → composite onto white background, drop alpha
      LA   (grey + alpha) → same
      L    (greyscale)    → keep as-is (Tesseract handles L fine)
      other               → convert to RGB
    """
    img = Image.open(file_path)
    img.load()  # force full decode into memory now
    logger.info(f"[IMG] Opened: size={img.size}, mode={img.mode}, fmt={img.format}")

    # Palette mode — go via RGBA to handle transparent PNGs correctly
    if img.mode == "P":
        img = img.convert("RGBA")

    # Alpha channel modes — composite onto white background, then drop alpha
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        channels = img.split()
        alpha = channels[-1]  # last channel is always alpha for RGBA / LA
        if img.mode == "LA":
            img = img.convert("RGBA")
        background.paste(img, mask=alpha)
        img = background
        logger.info(f"[IMG] Composited alpha onto white background -> RGB")

    # Any remaining non-RGB, non-L mode (CMYK, YCbCr, I, F …)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
        logger.info(f"[IMG] Converted to RGB")

    return img


def _pil_to_cv(img: Image.Image) -> np.ndarray:
    """Convert a PIL RGB image to a cv2 BGR ndarray."""
    rgb = np.array(img.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def _deskew(gray_bin: np.ndarray) -> np.ndarray:
    """Detect skew angle via Hough transform and rotate to correct it."""
    edges = cv2.Canny(gray_bin, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
                             minLineLength=100, maxLineGap=10)
    if lines is None:
        return gray_bin
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 != x1:
            angles.append(np.degrees(np.arctan2(y2 - y1, x2 - x1)))
    if not angles:
        return gray_bin
    median_angle = np.median(angles)
    if abs(median_angle) > 15:   # only correct small skews
        return gray_bin
    h, w = gray_bin.shape
    M = cv2.getRotationMatrix2D((w / 2, h / 2), median_angle, 1.0)
    return cv2.warpAffine(gray_bin, M, (w, h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)


def preprocess_image(img: Image.Image) -> Image.Image:
    """
    Multi-step preprocessing pipeline to improve OCR accuracy.

    CRITICAL DESIGN PRINCIPLE:
    Every single step is wrapped in its own try/except.
    If ANY step crashes (e.g. wrong dtype from a screenshot), the pipeline
    skips that step and continues — the Flask backend NEVER stops.

    Steps:
      1. Normalise to RGB  (handles RGBA/P/LA screenshot formats)
      2. Convert to grayscale
      3. Scale up small images  (< 1200 px wide -> better Tesseract DPI)
      4. Ensure uint8 dtype    ** CRITICAL: cv2 crashes on float/16-bit **
      5. Adaptive threshold    (binarize, removes coloured backgrounds)
      6. Denoise
      7. Deskew
    """
    # Step 1: Normalise PIL mode
    try:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
    except Exception as e:
        logger.warning(f"[PRE] Mode normalise failed: {e}")

    if not _HAVE_CV2:
        try:
            return img.convert("L")
        except Exception:
            return img

    # Step 2: Grayscale
    gray = None
    try:
        mat = _pil_to_cv(img)
        gray = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    except Exception as e:
        logger.warning(f"[PRE] Grayscale failed: {e} — returning original image")
        return img

    # Step 3: Scale up small images
    try:
        h, w = gray.shape
        if w < 1200:
            scale = max(2.0, 1200 / w)
            gray = cv2.resize(gray, None, fx=scale, fy=scale,
                              interpolation=cv2.INTER_CUBIC)
    except Exception as e:
        logger.warning(f"[PRE] Resize failed: {e} — continuing at original size")

    # Step 4: Ensure uint8 dtype  <-- most common screenshot crash point
    try:
        if gray.dtype != np.uint8:
            logger.info(f"[PRE] dtype={gray.dtype} — normalising to uint8")
            gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
            gray = gray.astype(np.uint8)
    except Exception as e:
        logger.warning(f"[PRE] dtype normalise failed: {e}")
        try:
            gray = gray.astype(np.uint8)
        except Exception:
            try:
                return Image.fromarray(gray)
            except Exception:
                return img

    # Step 5: Adaptive binarization
    binary = gray   # safe fallback if threshold fails
    try:
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=31, C=10
        )
    except Exception as e:
        logger.warning(f"[PRE] adaptiveThreshold failed: {e} — using grayscale")

    # Step 6: Denoise
    denoised = binary   # safe fallback
    try:
        denoised = cv2.fastNlMeansDenoising(binary, h=10)
    except Exception as e:
        logger.warning(f"[PRE] Denoise failed: {e} — skipping")

    # Step 7: Deskew
    try:
        denoised = _deskew(denoised)
    except Exception as e:
        logger.warning(f"[PRE] Deskew failed: {e} — skipping")

    # Return final PIL image
    try:
        return Image.fromarray(denoised)
    except Exception as e:
        logger.warning(f"[PRE] fromarray failed: {e} — returning grayscale PIL")
        try:
            return img.convert("L")
        except Exception:
            return img


# ── Core OCR call ─────────────────────────────────────────────────────────────

def _tesseract_ocr(img: Image.Image) -> str:
    """
    Run Tesseract on a PIL Image.
    Strategy A: direct subprocess per PSM mode (most reliable on Windows).
    Strategy B: pytesseract.image_to_string fallback if subprocess fails.
    Returns the longest successful result.
    """
    _ensure_tesseract()

    # Save to temp PNG — always as RGB or L; avoids mode-related save errors.
    # IMPORTANT: We close the file BEFORE calling Tesseract.
    # On Windows, open file handles are exclusively locked — Tesseract cannot
    # open a file that Python still has open, causing silent failures.
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".png")
    try:
        os.close(tmp_fd)  # close the OS-level file descriptor immediately
        save_img = img if img.mode in ("RGB", "L") else img.convert("RGB")
        save_img.save(tmp_path, "PNG")
    except Exception as save_err:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        raise RuntimeError(f"Failed to save temp image: {save_err}") from save_err

    logger.info(f"[TESS] Temp image: {tmp_path}")

    try:
        results = []

        # Strategy A: subprocess (bypasses pytesseract PATH bugs on Windows)
        # IMPORTANT: use text=False (binary mode) then decode as utf-8 manually.
        # text=True on Windows uses the system default encoding (cp1252) which
        # crashes on bytes Tesseract outputs that cp1252 cannot represent (0x9d etc).
        for psm in ["4", "6", "11"]:
            try:
                cmd = [_TESSERACT_CMD, tmp_path, "stdout", "--psm", psm, "--oem", "3"]
                env = os.environ.copy()
                r = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=False,          # binary — we decode manually below
                    timeout=30,
                    env=env,
                )
                if r.returncode == 0 and r.stdout:
                    # Decode as utf-8, replace undecodable bytes so we never crash
                    stdout_text = r.stdout.decode("utf-8", errors="replace").strip()
                    if stdout_text:
                        results.append(stdout_text)
                        logger.info(f"[TESS] subprocess PSM {psm}: {len(stdout_text)} chars")
                    else:
                        logger.warning(f"[TESS] subprocess PSM {psm}: empty output")
                else:
                    stderr_text = r.stderr.decode("utf-8", errors="replace") if r.stderr else ""
                    logger.warning(f"[TESS] subprocess PSM {psm} failed (rc={r.returncode}): {stderr_text[:120]}")
            except subprocess.TimeoutExpired:
                logger.warning(f"[TESS] subprocess PSM {psm} timeout")
            except Exception as e:
                logger.warning(f"[TESS] subprocess PSM {psm} exception: {e}")

        # Strategy B: pytesseract fallback (catches edge cases subprocess misses)
        if not results:
            logger.info("[TESS] subprocess failed — trying pytesseract fallback")
            for psm in ["6", "4", "11"]:
                try:
                    t = pytesseract.image_to_string(img, config=f"--oem 3 --psm {psm}")
                    if t.strip():
                        results.append(t.strip())
                        logger.info(f"[TESS] pytesseract PSM {psm}: {len(t)} chars")
                except Exception as e:
                    logger.warning(f"[TESS] pytesseract PSM {psm}: {e}")

        if not results:
            raise RuntimeError(
                f"All Tesseract strategies failed.\n"
                f"cmd={_TESSERACT_CMD}\n"
                f"TESSDATA_PREFIX={os.environ.get('TESSDATA_PREFIX')}"
            )

        best = max(results, key=len)
        logger.info(f"[TESS] Best result: {len(best)} chars")
        return best

    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


# ── Main extraction functions ─────────────────────────────────────────────────

def extract_text_from_image(file_path: str) -> str:
    """
    High-accuracy OCR for JPG / PNG / screenshot files.

    Uses 4 independent strategies — if one crashes, the next runs.
    The Flask backend will NEVER stop due to a bad screenshot format.

    Strategy 1 — preprocess (grayscale + binarize + denoise) -> subprocess OCR
    Strategy 2 — raw RGB image -> subprocess OCR  (no preprocessing)
    Strategy 3 — pytesseract.image_to_string with multiple PSMs
    Strategy 4 — greyscale PIL only -> pytesseract  (absolute last resort)
    """
    logger.info(f"[OCR] Starting image extraction: {file_path}")
    _ensure_tesseract()

    # Open and normalise — handles ALL screenshot formats (RGBA, P, LA, etc.)
    try:
        img = _safe_open_image(file_path)
        logger.info(f"[OCR] Image ready: size={img.size}, mode={img.mode}")
    except Exception as e:
        raise Exception(f"Cannot open image file: {e}") from e

    text = ""

    # Strategy 1: preprocess -> OCR
    try:
        logger.info("[OCR] Strategy 1: preprocess + OCR")
        processed = preprocess_image(img)
        text = _tesseract_ocr(processed)
        logger.info(f"[OCR] Strategy 1: {len(text)} chars")
    except Exception as e:
        logger.warning(f"[OCR] Strategy 1 failed: {e}")

    # Strategy 2: raw RGB -> OCR
    if len(text) < 30:
        try:
            logger.info("[OCR] Strategy 2: raw RGB, no preprocessing")
            text = _tesseract_ocr(img)
            logger.info(f"[OCR] Strategy 2: {len(text)} chars")
        except Exception as e:
            logger.warning(f"[OCR] Strategy 2 failed: {e}")

    # Strategy 3: pytesseract direct, multi-PSM
    if len(text) < 30:
        try:
            logger.info("[OCR] Strategy 3: pytesseract direct multi-PSM")
            _ensure_tesseract()
            for psm in ["6", "4", "11", "3"]:
                try:
                    t = pytesseract.image_to_string(img, config=f"--oem 3 --psm {psm}")
                    if len(t.strip()) > len(text):
                        text = t.strip()
                except Exception:
                    pass
            logger.info(f"[OCR] Strategy 3: {len(text)} chars")
        except Exception as e:
            logger.warning(f"[OCR] Strategy 3 failed: {e}")

    # Strategy 4: greyscale PIL fallback
    if len(text) < 30:
        try:
            logger.info("[OCR] Strategy 4: greyscale PIL fallback")
            _ensure_tesseract()
            grey = img.convert("L")
            text = pytesseract.image_to_string(grey, config="--oem 3 --psm 6")
            logger.info(f"[OCR] Strategy 4: {len(text)} chars")
        except Exception as e:
            logger.warning(f"[OCR] Strategy 4 failed: {e}")

    logger.info(f"[OCR] FINAL: {len(text)} chars extracted")
    return text


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF.
    1. pdfplumber  — fast, works for digital/selectable-text PDFs.
    2. pdf2image + OCR — fallback for scanned / image-only PDFs.
    """
    text = ""

    # Strategy 1: pdfplumber
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        text = text.strip()
    except Exception as e:
        logger.warning(f"[PDF] pdfplumber failed: {e}")
        text = ""

    # Strategy 2: pdf2image -> OCR
    if len(text) < 80 and _HAVE_PDF2IMAGE:
        logger.info("[PDF] Little text found — falling back to image OCR per page")
        try:
            _ensure_tesseract()
            pages = convert_from_path(file_path, dpi=250)
            ocr_parts = []
            for page_img in pages:
                processed = preprocess_image(page_img)
                ocr_parts.append(_tesseract_ocr(processed))
            text = "\n".join(ocr_parts).strip()
        except Exception as e:
            logger.error(f"[PDF] pdf2image OCR fallback failed: {e}", exc_info=True)

    return text


def extract_text(file_path: str, file_ext: str) -> str:
    """Main entry point. Supports pdf, jpg, jpeg, png (including screenshots)."""
    _ensure_tesseract()
    if file_ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_ext in ("jpg", "jpeg", "png"):
        return extract_text_from_image(file_path)
    return ""


# ── Out-of-Knowledge-Base Detection ──────────────────────────────────────────

_MEDICAL_KEYWORDS = [
    "hemoglobin", "haemoglobin", "hgb", "hb",
    "glucose", "blood sugar", "fbs", "hba1c",
    "cholesterol", "triglyceride", "ldl", "hdl", "lipid",
    "wbc", "white blood", "leukocyte", "tlc",
    "rbc", "red blood", "erythrocyte",
    "platelet", "plt", "thrombocyte",
    "creatinine", "urea", "bun", "kidney", "renal", "gfr",
    "sgpt", "sgot", "alt", "ast", "liver", "bilirubin",
    "tsh", "thyroid", "t3", "t4",
    "blood pressure", "systolic", "diastolic",
    "mcv", "mch", "mchc", "haematocrit", "hematocrit", "pcv",
    "complete blood count", "cbc", "haematology",
    "serum", "plasma",
]


def is_medical_report(text: str) -> bool:
    """Returns True if the text looks like a medical lab report (>=2 keywords)."""
    if not text or len(text.strip()) < 40:
        return False
    t = text.lower()
    hits = sum(1 for kw in _MEDICAL_KEYWORDS if kw in t)
    return hits >= 2


# ── Metric Extraction ─────────────────────────────────────────────────────────

def _parse_num(s: str) -> float | None:
    try:
        return float(s.replace(",", ""))
    except Exception:
        return None


def extract_medical_metrics(text: str) -> dict:
    """Extract common lab values from raw OCR text using multi-strategy regex."""
    metrics = {}
    text_lower = text.lower()

    NUM = r"([\d,]+\.?\d*)"
    SEP = r"[\s\:\=\|]+"

    patterns = {
        "hemoglobin":    rf"(?:h(?:a)?emoglobin|hgb|hb(?!\w)){SEP}{NUM}",
        "glucose":       rf"(?:glucose|blood\s*sugar|fbs|fasting\s*blood\s*sugar|rbs|random\s*blood\s*sugar){SEP}{NUM}",
        "cholesterol":   rf"(?:total\s*cholesterol|serum\s*cholesterol|cholesterol,?\s*total){SEP}{NUM}",
        "triglycerides": rf"(?:triglycerides?|tg|triacylglycerol){SEP}{NUM}",
        "hdl":           rf"(?:hdl[\s\-]?c?|hdl\s*cholesterol|high\s*density){SEP}{NUM}",
        "ldl":           rf"(?:ldl[\s\-]?c?|ldl\s*cholesterol|low\s*density){SEP}{NUM}",
        "wbc":           rf"(?:total\s+wbc\s+count|wbc(?:\s+count)?|white\s*blood\s*(?:cell|count|corpuscle)s?|leukocytes?|tlc|total\s*leucocyte){SEP}{NUM}",
        "rbc":           rf"(?:rbc(?:s)?\s*count|rbc|red\s*blood\s*(?:cell|count|corpuscle)(?:s)?|erythrocytes?){SEP}{NUM}",
        "platelets":     rf"(?:platelet(?:\s*count)?|plt|thrombocytes?){SEP}{NUM}",
        "creatinine":    rf"(?:creatinine|creat|s\.?\s*creatinine|serum\s*creatinine){SEP}{NUM}",
        "urea":          rf"(?:urea|bun|blood\s*urea\s*nitrogen|s\.?\s*urea|serum\s*urea){SEP}{NUM}",
        "sgpt":          rf"(?:sgpt|alt|alanine\s*(?:amino)?transferase|alanine\s*transaminase){SEP}{NUM}",
        "sgot":          rf"(?:sgot|ast|aspartate\s*(?:amino)?transferase|aspartate\s*transaminase){SEP}{NUM}",
        "tsh":           rf"(?:tsh|thyroid\s*stimulating\s*hormone|serum\s*tsh){SEP}{NUM}",
        "mcv":           rf"(?:mcv|mean\s*corpuscular\s*volume){SEP}{NUM}",
        "mch":           rf"(?:mch(?!c)|mean\s*corpuscular\s*h(?:a)?emoglobin(?!\s*conc)){SEP}{NUM}",
        "mchc":          rf"(?:mchc|mean\s*corpuscular\s*h(?:a)?emoglobin\s*conc){SEP}{NUM}",
        "haematocrit":   rf"(?:p\.?c\.?v\.?|h(?:a)?ematocrit|packed\s*cell\s*volume){SEP}{NUM}",
        "systolic_bp":   r"(?:systolic|bp|blood\s*pressure)[\s\:=]*(\d{2,3})\s*/",
        "diastolic_bp":  r"(?:diastolic|bp|blood\s*pressure)[\s\:=]*\d{2,3}\s*/\s*(\d{2,3})",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            val = _parse_num(match.group(1))
            if val is not None:
                metrics[key] = val

    # Line-scan fallback for tightly-packed table rows
    extra_keywords = {
        "hemoglobin":    ["haemoglobin", "hemoglobin", "hgb"],
        "wbc":           ["total wbc count", "wbc count", "wbc", "white blood cell", "tlc", "leukocyte"],
        "rbc":           ["rbcs count", "rbc count", "rbc", "red blood cell", "erythrocyte"],
        "platelets":     ["platelet count", "platelet", "plt", "thrombocyte"],
        "glucose":       ["glucose", "blood sugar", "fbs", "rbs"],
        "cholesterol":   ["total cholesterol", "cholesterol"],
        "triglycerides": ["triglyceride", "tg"],
        "mcv":           ["mcv", "mean corpuscular volume"],
        "mch":           ["mch", "mean corpuscular haemoglobin"],
        "haematocrit":   ["pcv", "haematocrit", "hematocrit", "packed cell"],
    }
    for key, kws in extra_keywords.items():
        if key in metrics:
            continue
        for kw in kws:
            for line in text_lower.splitlines():
                if kw in line:
                    m = re.search(r"([\d,]+\.?\d*)", line)
                    if m:
                        val = _parse_num(m.group(1))
                        if val is not None and val > 0:
                            metrics[key] = val
                            break
            if key in metrics:
                break

    # Unit normalisation
    if "wbc" in metrics and metrics["wbc"] > 100:
        metrics["wbc"] = round(metrics["wbc"] / 1000, 2)       # cells/cumm -> k/uL

    if "platelets" in metrics:
        p = metrics["platelets"]
        if p < 10:
            metrics["platelets"] = round(p * 100, 1)            # lakhs -> k/uL
        elif p > 1000:
            metrics["platelets"] = round(p / 1000, 1)           # raw -> k/uL

    if "rbc" in metrics and metrics["rbc"] > 20:
        metrics["rbc"] = round(metrics["rbc"] / 1_000_000, 2)  # abs count -> M/uL

    # MCH is in pg — typical range 27-33. If extracted as thousands (e.g. 3000), fix it
    if "mch" in metrics and metrics["mch"] > 100:
        metrics["mch"] = round(metrics["mch"] / 100, 1)

    # MCHC is in g/dL — typical range 32-36. Normalise if way off
    if "mchc" in metrics and metrics["mchc"] > 100:
        metrics["mchc"] = round(metrics["mchc"] / 10, 1)

    # MCV is in fL — typical range 80-100. Normalise if extracted as raw number
    if "mcv" in metrics and metrics["mcv"] > 200:
        metrics["mcv"] = round(metrics["mcv"] / 10, 1)

    # Haematocrit is a percentage — typical range 36-48%
    # If extracted as a decimal (e.g. 0.36), convert to percent
    if "haematocrit" in metrics and metrics["haematocrit"] < 1:
        metrics["haematocrit"] = round(metrics["haematocrit"] * 100, 1)

    return metrics


# ── Report Type Detection ─────────────────────────────────────────────────────

def detect_report_type(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["hemoglobin", "haemoglobin", "rbc", "wbc", "platelet", "cbc", "complete blood"]):
        return "Blood / CBC Report"
    elif any(w in t for w in ["glucose", "hba1c", "insulin", "diabetes"]):
        return "Diabetes / Glucose Report"
    elif any(w in t for w in ["cholesterol", "triglyceride", "ldl", "hdl", "lipid"]):
        return "Lipid Panel Report"
    elif any(w in t for w in ["creatinine", "urea", "kidney", "renal", "gfr"]):
        return "Kidney Function Report"
    elif any(w in t for w in ["sgpt", "sgot", "liver", "bilirubin", "hepatic"]):
        return "Liver Function Report"
    elif any(w in t for w in ["tsh", "t3", "t4", "thyroid"]):
        return "Thyroid Report"
    elif any(w in t for w in ["x-ray", "xray", "mri", "ct scan", "radiology", "scan"]):
        return "Radiology Report"
    return "General Medical Report"