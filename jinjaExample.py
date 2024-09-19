import pandas as pd
import jinja2
import pdfkit
from random import getrandbits, randint

# pdfkit is just a wrapper for whktmltopdf. you need to install wkhtml and have it on the path
# alternatively, you can move wkhtmltoimage.exe, wkhtmltopdf.exe and wkhtmltox.dll into the working directory

# Create some data
def random_hex(length=10):
    return '%0x' % getrandbits(length * 4)

df = pd.DataFrame([{"number":randint(0,100),
                    "name":random_hex(15),
                    "data1":random_hex(5),
                    "data2":random_hex(5),
                    "data3":random_hex(5)} for i in range(10)])[['number','name','data1','data2','data3']]

# Don't include the dataframe index in the html output,
# add the appropriate css class, and don't draw the border.
dfhtml = df.to_html(index=False, classes="table-title", border=False)

# Load the template
env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
template = env.get_template("tableTemplate.html")
# pass df, title, message to the template.
html_out = template.render(df=dfhtml,
                           title="Jinja2 Example",
                           message="This is an example text input")

# write the html to file
with open("output.html", 'wb') as file_:
    file_.write(html_out.encode("utf-8"))

# write the pdf to file
pdfkit.from_string(html_out, output_path="output.pdf", css=["template.css"])