from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(data):

    filename = "AI_Health_Report.pdf"


    pdf = canvas.Canvas(
        filename,
        pagesize=letter
    )


    pdf.setFont(
        "Helvetica-Bold",
        18
    )


    pdf.drawString(
        150,
        750,
        "AI Smart Health Report"
    )


    pdf.setFont(
        "Helvetica",
        12
    )


    y = 700


    for key, value in data.items():

        pdf.drawString(
            80,
            y,
            f"{key}: {value}"
        )

        y -= 30



    pdf.save()


    return filename