from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import pandas as pd

def generate_pdf_report(csv_file="encryption_results.csv"):
    df = pd.read_csv(csv_file)
    doc = SimpleDocTemplate("Encryption_Report.pdf", pagesize=A4)
    elements = []
    
    elements.append(Paragraph("<b>Hybrid MD5–SHA256 Image Encryption Report</b>", None))
    elements.append(Spacer(1, 20))
    
    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    print("✅ PDF report generated: Encryption_Report.pdf")

if __name__ == "__main__":
    generate_pdf_report()
