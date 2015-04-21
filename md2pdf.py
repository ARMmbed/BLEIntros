import yaml
import os
import re
from pyPdf import PdfFileWriter, PdfFileReader

img_pattern = r'!\[.*?\](\(.+?\))'

def remove_first_slash(s):
    full, toreplace = s.group(0), s.group(1)
    if toreplace.startswith('(/'):
        newtext = '(../' + toreplace[2:]
    else:
        newtext = toreplace
    return full.replace(toreplace, newtext)

def append_pdf(input, output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

f = open('mkdocs.yml')
y = yaml.load(f)
f.close()
os.chdir('Docs')
output = PdfFileWriter()
for fname in [e[0] for e in y['pages']]:
    with open(fname, 'rt') as f:
        origdata = f.read()
        data = re.sub(img_pattern, remove_first_slash, origdata)
    tempname, pdfname = fname + '.temp', fname.replace(".md", ".pdf")
    htmlname = tempname + '.html'
    with open(tempname, 'wt') as f:
        f.write(data)
    os.system("grip --wide --export %s %s" % (tempname, htmlname))
    os.system("wkhtmltopdf -l %s %s" % (htmlname, pdfname))
    append_pdf(PdfFileReader(file(pdfname, "rb")), output)
    [os.remove(f) for f in [tempname, htmlname, pdfname]]

os.chdir('..')
output.write(file('output.pdf', 'wb'))

