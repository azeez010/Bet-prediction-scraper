from cgitb import html
from fpdf import FPDF, HTMLMixin
from mail import today_date

class MyFPDF(FPDF, HTMLMixin):
    pass


def make_html(text):
    html = ""
    for i in text:
        if isinstance(i, list):
            html += f"<p>{i[0]}  - {i[1]}</p>"
        else:
            html += f"<br><p><b>{i}</b></p><br>"
    return html




def make_pdf(text):
    html = make_html(text)
    pdf = MyFPDF()
    pdf.set_font('Arial', '', 14)
    #First page
    pdf.add_page()
    pdf.write_html(html)
    pdf.output(f'{today_date()}_prediction.pdf', 'F')
    # pdf.output('html.pdf', 'F')

    # pdf = FPDF()
    # pdf.add_page()
    # pos_y = 5
    # # pdf.write(5, 'Visit ')
    # # # Then put a blue underlined link
    # # pdf.set_text_color(0, 0, 255)
    # # pdf.set_font('', 'U')
    # # pdf.write(15, 'www.fpdf.org', 'http://www.fpdf.org')
    # for line in text:
    #     if isinstance(line, list):
    #         # pdf.set_font('Arial', '', 14)
            # pdf.write(pos_y, line[0])
            # pdf.write(pos_y, line[1])
    #     else:
    #         # pdf.set_font('Arial', 'B', 16)
    #         pdf.write(pos_y, line)
        
    #     pos_y += 5

    
    # pdf.write(40, 10, 'Hello World!')
    # pdf.output('tuto1.pdf', 'F')