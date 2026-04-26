import re
import os

# ─────────────────────────────────────────────────────────
#  EXTRACTIVE SUMMARIZER  (fast, no model download needed)
# ─────────────────────────────────────────────────────────
def _extractive_summary(text: str) -> str:
    """Pick the most informative sentences from the report."""
    KEYWORDS = [
        'hemoglobin', 'glucose', 'cholesterol', 'tsh', 'thyroid',
        'platelet', 'wbc', 'rbc', 'creatinine', 'bilirubin', 'sgpt',
        'sgot', 'triglyceride', 'hdl', 'ldl', 'hba1c', 'insulin',
        'anemia', 'diabetes', 'hypertension', 'normal', 'abnormal',
        'elevated', 'low', 'high', 'deficiency', 'kidney', 'liver',
        'interpretation', 'result', 'finding', 'recommendation',
    ]
    sentences = [s.strip() for s in re.split(r'[.!\n]+', text) if len(s.strip()) > 25]
    scored = []
    for s in sentences:
        sl = s.lower()
        score = sum(1 for k in KEYWORDS if k in sl)
        if score > 0:
            scored.append((score, s))
    scored.sort(reverse=True)
    top = [s for _, s in scored[:6]]
    if not top:
        top = sentences[:4]
    return '. '.join(top) + '.' if top else "No summary available."


# ─────────────────────────────────────────────────────────
#  BART SUMMARIZER  (optional – only if already cached)
# ─────────────────────────────────────────────────────────
_BART_MODEL = "facebook/bart-large-cnn"
_summarizer = None


def _is_bart_cached() -> bool:
    """
    Check if BART model weights are already downloaded locally.

    IMPORTANT: We ONLY check the local filesystem — no network calls.
    The old transformers.utils.cached_file() approach would attempt to
    reach HuggingFace even for a cache check, causing the upload to hang
    indefinitely if there's no internet or the connection is slow.
    """
    # Check standard HuggingFace hub cache directory
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
    if not os.path.isdir(cache_dir):
        return False

    # Look for any folder that contains 'bart-large-cnn' in its name
    try:
        for entry in os.listdir(cache_dir):
            if "bart-large-cnn" in entry.lower():
                model_dir = os.path.join(cache_dir, entry)
                # Verify it actually has model weights (not just an empty folder)
                if os.path.isdir(model_dir):
                    files = os.listdir(model_dir)
                    has_weights = any(
                        f.endswith((".bin", ".safetensors", ".pt"))
                        for f in files
                    )
                    if has_weights:
                        return True
    except Exception:
        pass

    return False


def get_summarizer():
    """
    Return BART pipeline only if model is already cached locally.
    Falls back to fast extractive summarizer immediately if not cached.
    Never makes network calls — completely offline safe.
    """
    global _summarizer
    if _summarizer is not None:
        return _summarizer

    if not _is_bart_cached():
        print("[INFO] BART model not cached locally - using fast extractive summarizer.")
        _summarizer = "fallback"
        return _summarizer

    try:
        from transformers import pipeline
        import torch
        print("[INFO] Loading cached BART model...")
        _summarizer = pipeline(
            "summarization",
            model=_BART_MODEL,
            device=0 if torch.cuda.is_available() else -1,
            max_length=512, min_length=80, do_sample=False,
            # local_files_only=True prevents any network call during load
            model_kwargs={"local_files_only": True},
        )
        print("[OK] BART model loaded!")
    except Exception as e:
        print(f"[WARN] BART load error: {e} - using extractive fallback.")
        _summarizer = "fallback"

    return _summarizer


# ─────────────────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────────────────
def summarize_medical_text(text: str) -> str:
    """Summarize a medical report. Uses BART if cached locally, extractive otherwise."""
    if not text or len(text.strip()) < 30:
        return "Report text too short to summarize. Please check the uploaded file is readable."

    # Truncate to 900 words to keep inference fast
    words = text.split()
    if len(words) > 900:
        text = " ".join(words[:900])

    model = get_summarizer()
    if model == "fallback":
        return _extractive_summary(text)

    try:
        result = model(text, max_length=300, min_length=60, do_sample=False)
        return result[0]["summary_text"]
    except Exception:
        return _extractive_summary(text)


def simplify_medical_summary(summary: str, metrics: dict) -> str:
    """Append patient-friendly interpretation of the extracted metric values."""
    interpretations = []

    checks = {
        "hemoglobin":    [(None, 12,   "Your Hemoglobin ({v} g/dL) is LOW — may indicate anemia."),
                          (17,   None, "Your Hemoglobin ({v} g/dL) is HIGH — consult your doctor."),
                          (12,   17,   "Your Hemoglobin ({v} g/dL) is NORMAL. ✓")],
        "glucose":       [(None, 70,   "Blood Glucose ({v} mg/dL) is LOW — risk of hypoglycemia."),
                          (125,  None, "Blood Glucose ({v} mg/dL) is HIGH — possible diabetes."),
                          (70,   125,  "Blood Glucose ({v} mg/dL) is NORMAL. ✓")],
        "cholesterol":   [(200,  None, "Total Cholesterol ({v} mg/dL) is HIGH — heart disease risk."),
                          (None, 200,  "Total Cholesterol ({v} mg/dL) is within acceptable range. ✓")],
        "triglycerides": [(150,  None, "Triglycerides ({v} mg/dL) are HIGH."),
                          (None, 150,  "Triglycerides ({v} mg/dL) are NORMAL. ✓")],
        "tsh":           [(None, 0.4,  "TSH ({v} mIU/L) is LOW — may indicate hyperthyroidism."),
                          (4.0,  None, "TSH ({v} mIU/L) is HIGH — may indicate hypothyroidism."),
                          (0.4,  4.0,  "TSH ({v} mIU/L) is NORMAL. ✓")],
        "creatinine":    [(1.2,  None, "Creatinine ({v} mg/dL) is HIGH — kidney function may be impaired."),
                          (None, 1.2,  "Creatinine ({v} mg/dL) is NORMAL. ✓")],
        "wbc":           [(None, 4.5,  "WBC ({v} k/uL) is LOW — possible immune issue."),
                          (11,   None, "WBC ({v} k/uL) is HIGH — possible infection or inflammation."),
                          (4.5,  11,   "WBC ({v} k/uL) is NORMAL. ✓")],
        "mch":           [(None, 27,   "MCH ({v} pg) is LOW — may suggest iron-deficiency anemia."),
                          (33,   None, "MCH ({v} pg) is HIGH — may indicate macrocytic anemia."),
                          (27,   33,   "MCH ({v} pg) is NORMAL. ✓")],
        "mchc":          [(None, 32,   "MCHC ({v} g/dL) is LOW — may indicate iron-deficiency or thalassemia."),
                          (36,   None, "MCHC ({v} g/dL) is HIGH — may indicate dehydration or spherocytosis."),
                          (32,   36,   "MCHC ({v} g/dL) is NORMAL. ✓")],
        "mcv":           [(None, 80,   "MCV ({v} fL) is LOW — microcytic anemia likely."),
                          (100,  None, "MCV ({v} fL) is HIGH — macrocytic anemia, check B12/folate."),
                          (80,   100,  "MCV ({v} fL) is NORMAL. ✓")],
        "haematocrit":   [(None, 36,   "Haematocrit ({v}%) is LOW — may indicate anemia or blood loss."),
                          (48,   None, "Haematocrit ({v}%) is HIGH — possible dehydration or polycythemia."),
                          (36,   48,   "Haematocrit ({v}%) is NORMAL. ✓")],
        "platelets":     [(None, 150,  "Platelets ({v} k/µL) are LOW — bleeding risk, consult doctor."),
                          (400,  None, "Platelets ({v} k/µL) are HIGH — possible thrombocytosis."),
                          (150,  400,  "Platelets ({v} k/µL) are NORMAL. ✓")],
        "rbc":           [(None, 4.0,  "RBC ({v} M/µL) is LOW — possible anemia."),
                          (5.5,  None, "RBC ({v} M/µL) is HIGH — possible polycythemia."),
                          (4.0,  5.5,  "RBC ({v} M/µL) is NORMAL. ✓")],
    }

    for key, rules in checks.items():
        if key not in metrics:
            continue
        v = metrics[key]
        for lo, hi, msg in rules:
            if (lo is None or v >= lo) and (hi is None or v < hi):
                interpretations.append(msg.replace("{v}", str(v)))
                break

    if interpretations:
        summary += "\n\n📊 Key Findings:\n" + "\n".join(f"  • {i}" for i in interpretations)
    return summary


# ─────────────────────────────────────────────────────────
#  CRITICAL THRESHOLDS
# ─────────────────────────────────────────────────────────
CRITICAL_THRESHOLDS = {
    "hemoglobin":    {"low": 8.0,  "high": 19.5},
    "glucose":       {"low": 50.0, "high": 250.0},
    "cholesterol":   {"high": 300.0},
    "triglycerides": {"high": 400.0},
    "creatinine":    {"high": 3.0},
    "tsh":           {"low": 0.1,  "high": 15.0},
    "wbc":           {"low": 2.0,  "high": 35.0},
    "platelets":     {"low": 50.0, "high": 900.0},
    "sgpt":          {"high": 250.0},
    "sgot":          {"high": 250.0},
}

def is_critical_metric(key: str, value: float) -> bool:
    """Check if a metric value is within the 'Critical' range."""
    limits = CRITICAL_THRESHOLDS.get(key)
    if not limits:
        return False
    
    low = limits.get("low")
    high = limits.get("high")
    
    if low is not None and value <= low:
        return True
    if high is not None and value >= high:
        return True
    
    return False


# ─────────────────────────────────────────────────────────
#  STRUCTURED RECOMMENDATIONS  (for rich frontend display)
# ─────────────────────────────────────────────────────────
METRIC_META = {
    "hemoglobin": {
        "unit": "g/dL", "label": "Hemoglobin",
        "range": [12, 17], "min_display": 5, "max_display": 22,
        "low":  {"title": "Low Hemoglobin (Anemia Risk)",
                 "tips": ["Eat iron-rich foods: spinach, lentils, red meat",
                          "Take iron + Vitamin C supplements (helps absorption)",
                          "Avoid tea/coffee right after meals (blocks iron)",
                          "Get a serum ferritin test to confirm iron deficiency",
                          "Follow up with your doctor if fatigue persists"]},
        "high": {"title": "High Hemoglobin",
                 "tips": ["Stay well hydrated throughout the day",
                          "Avoid smoking — it raises hemoglobin artificially",
                          "Rule out polycythemia vera with your doctor",
                          "Reduce high-altitude exposure if applicable"]},
    },
    "glucose": {
        "unit": "mg/dL", "label": "Blood Glucose",
        "range": [70, 100], "min_display": 40, "max_display": 300,
        "low":  {"title": "Low Blood Sugar (Hypoglycemia)",
                 "tips": ["Eat small, frequent meals every 3–4 hours",
                          "Carry glucose tablets or fruit juice when going out",
                          "Avoid skipping meals or prolonged fasting",
                          "Monitor blood sugar regularly at home"]},
        "high": {"title": "High Blood Sugar (Diabetes Risk)",
                 "tips": ["Reduce sugar, white rice, and processed carbohydrates",
                          "Walk 30 minutes daily — exercise improves insulin sensitivity",
                          "Stay hydrated — drink 8–10 glasses of water daily",
                          "Get HbA1c test to assess 3-month glucose average",
                          "Consult an endocrinologist if fasting glucose > 126 mg/dL"]},
    },
    "cholesterol": {
        "unit": "mg/dL", "label": "Total Cholesterol",
        "range": [100, 200], "min_display": 50, "max_display": 350,
        "high": {"title": "High Cholesterol (Heart Risk)",
                 "tips": ["Avoid fried food, ghee, and full-fat dairy",
                          "Eat oats, nuts, and olive oil (raise good HDL)",
                          "Exercise at least 150 min/week (cardio preferred)",
                          "Get LDL / HDL ratio checked — it's more important",
                          "Doctor may prescribe statins if LDL > 190 mg/dL"]},
        "low":  {"title": "Cholesterol is Normal",
                 "tips": ["Maintain a balanced diet and regular exercise",
                          "Get labs rechecked annually"]},
    },
    "triglycerides": {
        "unit": "mg/dL", "label": "Triglycerides",
        "range": [0, 150], "min_display": 0, "max_display": 500,
        "high": {"title": "High Triglycerides",
                 "tips": ["Cut down on sugar, alcohol, and refined carbs",
                          "Eat fatty fish (salmon, mackerel) twice a week",
                          "Omega-3 supplements are clinically proven to help",
                          "Lose 5–10% body weight if overweight"]},
        "low":  {"title": "Triglycerides are Normal ✓",
                 "tips": ["Keep up your healthy lifestyle habits"]},
    },
    "tsh": {
        "unit": "mIU/L", "label": "TSH (Thyroid)",
        "range": [0.4, 4.0], "min_display": 0, "max_display": 10,
        "low":  {"title": "Low TSH (Possible Hyperthyroidism)",
                 "tips": ["Get Free T3 and Free T4 tested",
                          "Watch for symptoms: rapid heart rate, anxiety, weight loss",
                          "Avoid iodine supplements without doctor advice",
                          "Consult an endocrinologist"]},
        "high": {"title": "High TSH (Possible Hypothyroidism)",
                 "tips": ["Get Free T4 tested to confirm hypothyroidism",
                          "Watch for fatigue, hair loss, weight gain, cold sensitivity",
                          "Doctor may prescribe Levothyroxine",
                          "Recheck TSH every 6 months after treatment"]},
    },
    "creatinine": {
        "unit": "mg/dL", "label": "Creatinine",
        "range": [0.5, 1.2], "min_display": 0, "max_display": 5,
        "high": {"title": "High Creatinine (Kidney Stress)",
                 "tips": ["Drink at least 2–3 liters of water daily",
                          "Reduce protein intake temporarily (meat, supplements)",
                          "Avoid NSAIDs (ibuprofen) — they strain kidneys",
                          "Get eGFR test to measure kidney filtration rate",
                          "See a nephrologist if creatinine > 2 mg/dL"]},
        "low":  {"title": "Creatinine is Normal ✓",
                 "tips": ["Good kidney function — keep hydrated"]},
    },
    "wbc": {
        "unit": "k/µL", "label": "White Blood Cells",
        "range": [4.5, 11], "min_display": 0, "max_display": 25,
        "low":  {"title": "Low WBC (Leukopenia)",
                 "tips": ["Avoid contact with sick individuals",
                          "Wash hands frequently — immune system is weaker",
                          "Check if medications (chemo, antibiotics) are causing it",
                          "Doctor may order bone marrow tests if persistent"]},
        "high": {"title": "High WBC (Possible Infection/Inflammation)",
                 "tips": ["Look for signs of infection: fever, pain, redness",
                          "Get a differential WBC count to identify cell type",
                          "Rest and treat underlying infection",
                          "Recheck in 2 weeks after antibiotic treatment"]},
    },
    "rbc": {
        "unit": "M/µL", "label": "Red Blood Cells",
        "range": [4.0, 5.5], "min_display": 2, "max_display": 8,
        "low":  {"title": "Low RBC Count",
                 "tips": ["Increase iron and B12 rich foods",
                          "Rule out chronic blood loss (ulcers, menstruation)",
                          "Bone marrow evaluation if severely low"]},
        "high": {"title": "High RBC Count",
                 "tips": ["Ensure adequate hydration",
                          "Rule out polycythemia vera",
                          "Stop smoking"]},
    },
    "platelets": {
        "unit": "k/µL", "label": "Platelets",
        "range": [150, 400], "min_display": 0, "max_display": 700,
        "low":  {"title": "Low Platelets (Thrombocytopenia)",
                 "tips": ["Avoid aspirin and blood thinners",
                          "Watch for unusual bruising or bleeding",
                          "Doctor may check for dengue, ITP, or medication side effects",
                          "Severe cases (< 50k) need urgent medical attention"]},
        "high": {"title": "High Platelets",
                 "tips": ["Usually a reactive rise due to infection or iron deficiency",
                          "Rule out essential thrombocythemia with doctor",
                          "Monitor if repeatedly elevated"]},
    },
    "sgpt": {
        "unit": "U/L", "label": "SGPT (ALT)",
        "range": [7, 56], "min_display": 0, "max_display": 200,
        "high": {"title": "High SGPT — Liver Stress",
                 "tips": ["Avoid alcohol completely during elevated liver enzymes",
                          "Stop or reduce paracetamol/NSAIDs",
                          "Eat a light, low-fat, vegetable-rich diet",
                          "Get hepatitis B & C tests ruled out",
                          "Recheck after 4–6 weeks of diet changes"]},
        "low":  {"title": "SGPT is Normal ✓",
                 "tips": ["Good liver health — avoid excess alcohol"]},
    },
    "sgot": {
        "unit": "U/L", "label": "SGOT (AST)",
        "range": [10, 40], "min_display": 0, "max_display": 200,
        "high": {"title": "High SGOT — Liver/Muscle Concern",
                 "tips": ["Could indicate liver disease or muscle injury",
                          "Get SGOT/SGPT ratio assessed together",
                          "Check if intense exercise caused muscle breakdown",
                          "Consult doctor if both SGPT and SGOT are elevated"]},
        "low":  {"title": "SGOT is Normal ✓",
                 "tips": ["Keep up healthy diet habits"]},
    },
    "hdl": {
        "unit": "mg/dL", "label": "HDL (Good Cholesterol)",
        "range": [60, 999], "min_display": 0, "max_display": 120,
        "low":  {"title": "Low HDL — Cardiovascular Risk",
                 "tips": ["Exercise regularly — it's the best way to raise HDL",
                          "Quit smoking — it dramatically lowers HDL",
                          "Eat healthy fats: olive oil, avocado, nuts",
                          "Avoid trans fats completely (packaged snacks)"]},
        "high": {"title": "HDL is Excellent ✓",
                 "tips": ["Great! High HDL protects your heart",
                          "Keep exercising and eating well"]},
    },
    "ldl": {
        "unit": "mg/dL", "label": "LDL (Bad Cholesterol)",
        "range": [0, 100], "min_display": 0, "max_display": 300,
        "high": {"title": "High LDL — Heart Disease Risk",
                 "tips": ["Reduce saturated fats: red meat, butter, cheese",
                          "Eat soluble fiber: oats, beans, fruits",
                          "Exercise lowers LDL by 5–10%",
                          "Statin therapy if LDL > 160 mg/dL with risk factors"]},
        "low":  {"title": "LDL is Optimal ✓",
                 "tips": ["Excellent! Keep up the healthy diet"]},
    },
    "mch": {
        "unit": "pg", "label": "MCH",
        "range": [27, 33], "min_display": 15, "max_display": 45,
        "low":  {"title": "Low MCH — Iron Deficiency Anemia Likely",
                 "tips": ["Increase iron-rich foods: red meat, spinach, lentils",
                          "Take iron supplements with Vitamin C for better absorption",
                          "Get serum ferritin and iron binding capacity tested",
                          "Rule out thalassemia with a haemoglobin electrophoresis test",
                          "Follow up with doctor after 3 months of iron therapy"]},
        "high": {"title": "High MCH — Macrocytic Anemia",
                 "tips": ["Get Vitamin B12 and Folate levels tested urgently",
                          "Eat B12-rich foods: eggs, dairy, meat, fish",
                          "Folate sources: leafy greens, legumes, fortified cereals",
                          "Avoid excessive alcohol — it depletes B12 and folate",
                          "Doctor may recommend B12 injections if severely deficient"]},
    },
    "mchc": {
        "unit": "g/dL", "label": "MCHC",
        "range": [32, 36], "min_display": 20, "max_display": 42,
        "low":  {"title": "Low MCHC — Hypochromic Anemia",
                 "tips": ["Often paired with low MCH — iron deficiency is likely",
                          "Increase dietary iron and consider supplements",
                          "Get iron panel: serum iron, ferritin, TIBC",
                          "Thalassemia screening may be needed if chronic",
                          "Recheck CBC after 8 weeks of iron treatment"]},
        "high": {"title": "High MCHC — Possible Spherocytosis",
                 "tips": ["High MCHC can indicate hereditary spherocytosis",
                          "Get a peripheral blood smear done",
                          "Check for signs of jaundice or enlarged spleen",
                          "Consult a haematologist for further evaluation",
                          "Severe dehydration can also raise MCHC — stay hydrated"]},
    },
    "mcv": {
        "unit": "fL", "label": "MCV",
        "range": [80, 100], "min_display": 50, "max_display": 130,
        "low":  {"title": "Low MCV — Microcytic Anemia",
                 "tips": ["Most common cause is iron deficiency — get ferritin tested",
                          "Thalassemia is another common cause — get Hb electrophoresis",
                          "Eat iron-rich foods and consider iron supplements",
                          "Avoid tea/coffee with meals — they block iron absorption",
                          "Doctor may investigate chronic disease as a cause"]},
        "high": {"title": "High MCV — Macrocytic Anemia",
                 "tips": ["Get Vitamin B12 and Folate tested immediately",
                          "Reduce or eliminate alcohol intake",
                          "Eat eggs, dairy, meat for B12; leafy greens for folate",
                          "Hypothyroidism can also cause high MCV — check TSH",
                          "Some medications (methotrexate, hydroxyurea) raise MCV"]},
    },
    "haematocrit": {
        "unit": "%", "label": "Haematocrit (PCV)",
        "range": [36, 48], "min_display": 15, "max_display": 65,
        "low":  {"title": "Low Haematocrit — Anemia",
                 "tips": ["Low PCV usually mirrors low hemoglobin — treat anemia",
                          "Increase iron, B12, and folate in your diet",
                          "Rule out chronic blood loss (ulcers, heavy periods)",
                          "Stay well hydrated but also rest adequately",
                          "Recheck CBC after 6–8 weeks of treatment"]},
        "high": {"title": "High Haematocrit — Possible Dehydration or Polycythemia",
                 "tips": ["Drink at least 2–3 litres of water daily",
                          "Stop smoking — it raises haematocrit",
                          "Rule out polycythemia vera with a JAK2 mutation test",
                          "Avoid diuretics unless prescribed",
                          "High altitude living can raise haematocrit — normal if so"]},
    },
}


def build_recommendations(metrics: dict) -> list:
    """Return a list of structured recommendation objects for each metric."""
    results = []
    for key, value in metrics.items():
        meta = METRIC_META.get(key)
        if not meta:
            continue
        lo, hi = meta["range"]
        if value < lo:
            status = "low"
        elif value > hi:
            status = "high"
        else:
            status = "normal"

        rec = meta.get(status)
        if not rec:
            continue

        rng = meta["max_display"] - meta["min_display"]
        pct    = max(0, min(100, (value       - meta["min_display"]) / rng * 100)) if rng else 50
        lo_pct = max(0, min(100, (lo          - meta["min_display"]) / rng * 100)) if rng else 0
        hi_pct = max(0, min(100, (hi          - meta["min_display"]) / rng * 100)) if rng else 100

        results.append({
            "key":          key,
            "label":        meta["label"],
            "value":        value,
            "unit":         meta["unit"],
            "status":       status,
            "is_critical":  is_critical_metric(key, value),
            "normal_range": f"{lo}–{hi} {meta['unit']}",
            "normal_lo":    lo,
            "normal_hi":    hi,
            "pct":          round(pct, 1),
            "lo_pct":       round(lo_pct, 1),
            "hi_pct":       round(hi_pct, 1),
            "rec_title":    rec["title"],
            "rec_tips":     rec["tips"],
        })
    return results