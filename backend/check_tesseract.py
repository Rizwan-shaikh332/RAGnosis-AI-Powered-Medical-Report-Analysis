#!/usr/bin/env python3
"""
Quick Tesseract diagnostic script.
Run this to verify Tesseract is properly configured.
"""
import os
import sys
import subprocess

print("=" * 70)
print("🔍 RAGNOSIS TESSERACT DIAGNOSTIC")
print("=" * 70)

# Check environment
print(f"\n📋 System Info:")
print(f"   Platform: {sys.platform}")
print(f"   Python: {sys.version}")
print(f"   CWD: {os.getcwd()}")

# Check .env setting
print(f"\n📄 .env Configuration:")
env_cmd = os.environ.get("TESSERACT_CMD")
if env_cmd:
    print(f"   ✓ TESSERACT_CMD set to: {env_cmd}")
else:
    print(f"   ✗ TESSERACT_CMD not set in .env")

# Check standard locations
print(f"\n🔎 Checking standard Windows locations:")
candidates = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
]

found = False
for path in candidates:
    exists = os.path.isfile(path)
    status = "✓" if exists else "✗"
    print(f"   {status} {path}")
    if exists and not found:
        found = True
        print(f"      → Testing...")
        try:
            result = subprocess.run([path, "--version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"      ✓ EXECUTABLE")
                print(f"      Version: {result.stdout.decode().split(chr(10))[0]}")
            else:
                print(f"      ✗ NOT EXECUTABLE (returncode: {result.returncode})")
        except Exception as e:
            print(f"      ✗ ERROR: {e}")

# Check PATH
print(f"\n🛣️  Checking system PATH:")
try:
    result = subprocess.run(["tesseract", "--version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        print(f"   ✓ Found tesseract in PATH")
        print(f"   Version: {result.stdout.decode().split(chr(10))[0]}")
except Exception:
    print(f"   ✗ tesseract not found in PATH")

# Import and test the module
print(f"\n🧪 Testing RAGnosis module import:")
try:
    from services.text_extractor import get_tesseract_status, _find_tesseract, _TESSERACT_CMD

    # Force discovery
    status = get_tesseract_status()
    print(f"   ✓ Module imported successfully")
    print(f"   ")
    print(f"   Tesseract Status:")
    print(f"      Found: {status['tesseract_found']}")
    print(f"      Path: {status['tesseract_path']}")
    print(f"      TESSDATA: {status['tessdata_prefix']}")
    print(f"      Platform: {status['platform']}")

except Exception as e:
    print(f"   ✗ Module import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("If all checks pass, try uploading a screenshot now!")
print("=" * 70)
