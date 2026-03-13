# 🔧 Tesseract Configuration Guide for RAGnosis

Your Tesseract **IS installed** and working (`v5.5.0.20241111` confirmed). However, the Flask backend isn't picking it up yet.

## Quick Fix (Most Likely to Work)

### Step 1: **RESTART THE FLASK SERVER**

This is the #1 reason - Flask caches Python modules. Stop and restart your backend:

```bash
# In your backend directory
# 1. Stop the running Flask server (Ctrl+C in terminal)
# 2. Restart it with:

python app.py
```

Watch the console output. You should see:
```
[TESS] ✓ Found Tesseract at: C:\Program Files\Tesseract-OCR\tesseract.exe
[TESS] TESSDATA_PREFIX set to: ...
```

---

## If It Still Doesn't Work

### Step 2: **Run the Diagnostic Script**

From the `backend/` directory:

```bash
python check_tesseract.py
```

This will show:
- If Tesseract is detected in standard locations
- If it's executable
- The exact status when RAGnosis loads

### Step 3: **Manually Configure in .env (If Needed)**

If the diagnostic shows Tesseract found, but upload still fails:

Edit `backend/.env` and add:

```bash
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

Then restart Flask again.

---

## Verify It's Working

### Option A: Check Health Endpoint
```
http://localhost:5000/api/health
```

Response should show:
```json
{
  "status": "ok",
  "message": "RAGnosis API is running",
  "tesseract": {
    "tesseract_found": true,
    "tesseract_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
    "tessdata_prefix": "C:\\Program Files\\Tesseract-OCR\\tessdata",
    ...
  }
}
```

### Option B: Full Diagnostic Endpoint
```
http://localhost:5000/api/diagnostics/tesseract
```

---

## What Was Fixed

✅ **Auto-detection improved** - Now checks standard Windows paths more reliably
✅ **Custom path support** - Can set `TESSERACT_CMD` in `.env`
✅ **Better error messages** - Clear instructions when Tesseract is missing
✅ **Diagnostic endpoints** - Can check status without uploading files
✅ **Lazy initialization** - Tesseract is discovered on first use if not found at startup

---

## If That Still Doesn't Work

1. **Verify Tesseract installation:**
   ```bash
   "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   ```
   Should print version info. ✓ You confirmed this works!

2. **Check tessdata folder exists:**
   ```bash
   dir "C:\Program Files\Tesseract-OCR\tessdata"
   ```
   Should list language files (eng.traineddata, etc.)

3. **Check Flask console logs:**
   When you restart Flask, watch the console for `[TESS]` messages:
   ```
   [TESS] ✓ Found Tesseract at: ...
   [TESS] TESSDATA_PREFIX set to: ...
   ```

4. **Last resort - Set path explicitly in .env:**
   ```bash
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

---

## Screenshot Upload Quick Test

1. Open http://localhost:5173
2. Login
3. Go to **Upload Report** tab
4. Take a screenshot of any text (or use an image file)
5. Upload it
6. Should see the extracted text and analysis!

---

**Need more help?** Check `backend/uploads/` folder for error logs, or review Flask console output when uploading.
