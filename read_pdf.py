import pdfplumber

try:
    with pdfplumber.open('critical_blood_report.pdf') as pdf:
        text = pdf.pages[0].extract_text()
        print("--- CONTENT ---")
        print(text)
        print("---------------")
except Exception as e:
    print(f"Error: {e}")
