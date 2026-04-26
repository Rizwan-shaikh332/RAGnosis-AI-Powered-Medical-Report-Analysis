from fpdf import FPDF
import os

class MedicalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'CITY DIAGNOSTIC CENTER', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Katraj-Kondhwa Road, Katraj, Pune - 411046', 0, 1, 'C')
        self.cell(0, 5, 'Phone: +91 20 2437 0000 | Email: reports@citydiag.com', 0, 1, 'C')
        self.line(10, 35, 200, 35)
        self.ln(10)

    def footer(self):
        self.set_y(-25)
        self.set_font('Arial', 'I', 8)
        self.line(10, self.y, 200, self.y)
        self.cell(0, 10, 'This report is computer generated and does not require a physical signature.', 0, 0, 'C')
        self.set_y(-15)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')

def create_report():
    pdf = MedicalReport()
    pdf.add_page()
    
    # Patient Details
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(35, 7, 'Patient Name:', 0)
    pdf.set_font('Arial', '', 11)
    pdf.cell(60, 7, 'DEMO USER (CRITICAL TEST)', 0)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(35, 7, 'Sample Date:', 0)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, '25-Apr-2026', 0, 1)
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(35, 7, 'Age / Gender:', 0)
    pdf.set_font('Arial', '', 11)
    pdf.cell(60, 7, '28 Years / Male', 0)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(35, 7, 'Lab ID:', 0)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, 'PL-2026-999', 0, 1)
    
    pdf.ln(10)
    
    # Table Header
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 10, ' Test Parameter', 1, 0, 'L', True)
    pdf.cell(40, 10, ' Observed Value', 1, 0, 'C', True)
    pdf.cell(30, 10, ' Unit', 1, 0, 'C', True)
    pdf.cell(60, 10, ' Reference Range', 1, 1, 'C', True)
    
    # Critical Results
    pdf.set_font('Arial', '', 10)
    
    # Hemoglobin
    pdf.cell(60, 10, ' Hemoglobin (Hb)', 1)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, ' 6.2 (CRITICAL)', 1, 0, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(30, 10, ' g/dL', 1, 0, 'C')
    pdf.cell(60, 10, ' 13.0 - 17.0', 1, 1, 'C')
    
    # WBC
    pdf.cell(60, 10, ' WBC Count', 1)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, ' 35,000 (H)', 1, 0, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(30, 10, ' /cumm', 1, 0, 'C')
    pdf.cell(60, 10, ' 4,000 - 11,000', 1, 1, 'C')

    # Platelets
    pdf.cell(60, 10, ' Platelet Count', 1)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, ' 40,000 (L)', 1, 0, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(30, 10, ' /cumm', 1, 0, 'C')
    pdf.cell(60, 10, ' 1,50,000 - 4,50,000', 1, 1, 'C')
    
    # Blood Glucose
    pdf.cell(60, 10, ' Blood Glucose (Random)', 1)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, ' 420 (CRITICAL)', 1, 0, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(30, 10, ' mg/dL', 1, 0, 'C')
    pdf.cell(60, 10, ' 70 - 140', 1, 1, 'C')

    pdf.ln(10)
    
    # Interpretation
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 10, 'INTERPRETATION:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, '1. Severe Anemia (Hemoglobin 6.2 g/dL): Requires immediate clinical evaluation and possibly blood transfusion. \n2. Significant Leukocytosis (WBC 35,000): Suggestive of acute infection or severe inflammation. \n3. Severe Thrombocytopenia (Platelets 40,000): High risk of spontaneous bleeding. \n4. Severe Hyperglycemia (Glucose 420): Indicative of uncontrolled diabetes or ketoacidosis risk. \n\nIMMEDIATE DOCTOR CONSULTATION IS MANDATORY.', 0)

    # Save
    output_path = os.path.join(os.getcwd(), 'critical_blood_report.pdf')
    pdf.output(output_path)
    print(f"PDF Successfully created at: {output_path}")

if __name__ == '__main__':
    create_report()
