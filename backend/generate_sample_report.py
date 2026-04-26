from PIL import Image, ImageDraw
import os

# Create a blank white image
img = Image.new('RGB', (800, 1000), color='white')
d = ImageDraw.Draw(img)

# Title
# Since we don't have easy access to custom fonts, we'll use default
d.text((300, 40), "CITY PATHOLOGY LAB", fill=(0, 0, 0))
d.text((320, 70), "Katraj, Pune - 411046", fill=(100, 100, 100))

# Patient Info
d.text((50, 150), "Patient Name: Demo User", fill=(0, 0, 0))
d.text((50, 180), "Age/Gender: 28 / Male", fill=(0, 0, 0))
d.text((500, 150), "Date: 25-Apr-2026", fill=(0, 0, 0))
d.text((500, 180), "Report ID: RAG-9999", fill=(0, 0, 0))

# Table Header
d.line((50, 220, 750, 220), fill=(0, 0, 0), width=2)
d.text((60, 230), "TEST PARAMETER", fill=(0,0,0))
d.text((300, 230), "OBSERVED VALUE", fill=(0,0,0))
d.text((500, 230), "NORMAL RANGE", fill=(0,0,0))
d.line((50, 260, 750, 260), fill=(0, 0, 0), width=1)

# Metrics (Critical)
d.text((60, 280), "Hemoglobin mg/dL", fill=(0,0,0)) # Using mg/dL to help regex if needed
d.text((310, 280), "6.5", fill=(0,0,0)) 
d.text((510, 280), "12.0 - 17.0", fill=(100,100,100))

d.text((60, 320), "Glucose mg/dL", fill=(0,0,0))
d.text((310, 320), "350", fill=(0,0,0)) 
d.text((510, 320), "70.0 - 100.0", fill=(100,100,100))

d.text((60, 360), "WBC k/uL", fill=(0,0,0))
d.text((310, 360), "32.0", fill=(0,0,0)) 
d.text((510, 360), "4.5 - 11.0", fill=(100,100,100))

d.text((60, 400), "Platelets k/uL", fill=(0,0,0))
d.text((310, 400), "45", fill=(0,0,0)) 
d.text((510, 400), "150 - 400", fill=(100,100,100))

# Footer
d.line((50, 900, 750, 900), fill=(0, 0, 0), width=1)
d.text((250, 920), "*** End of Report ***", fill=(0,0,0))

# Save
output_path = os.path.join(os.getcwd(), "sample_critical_report.jpg")
img.save(output_path)
print(f"Sample report created at: {output_path}")
