from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

def generate_pdf():
    # Render HTML content
    html_string = render_to_string('example_pdf_template.html', {'data': 'Sample Data'})

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="example.pdf"'  # Set to 'attachment' for download

    # Generate the PDF
    HTML(string=html_string).write_pdf(response)

    return response
