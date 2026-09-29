from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os


def create_pdf(title, content):

    os.makedirs("generated/pdfs", exist_ok=True)

    filename = f"{title.replace(' ', '_')}.pdf"
    path = os.path.join("generated/pdfs", filename)

    document = SimpleDocTemplate(
        path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(title, styles["Title"])
    )

    story.append(Spacer(1, 20))

    for paragraph in content.split("\n"):

        if paragraph.strip():

            story.append(
                Paragraph(
                    paragraph,
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 10)
            )

    document.build(story)

    return path