import jinja2
from weasyprint import HTML


def html_formatter_default(template, data):
    """Format the HTML template with the data"""
    try:
        with open(template, 'r') as f:
            template = Template(f.read())
            return template.render(data=data)
    except Exception as e:
        print(e)


def html_formatter(template, data):
    """Format the HTML template with the data"""
    try:
        templateLoader = jinja2.FileSystemLoader(searchpath="templates")
        templateEnv = jinja2.Environment(loader=templateLoader, autoescape=True)
        template = templateEnv.get_template(template)
        return template.render(data=data)
    except Exception as e:
        print(e)


def pdf_formatter(template, data, file_name):
    """Format the PDF template with the data"""
    try:
        message = html_formatter(template, data)
        html = HTML(string=message)
        filename = f"{file_name}.pdf"
        html.write_pdf(target=filename, zoom=0.1)
    except Exception as e:
        print(e)
