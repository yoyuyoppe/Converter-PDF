import sys
import argparse
from pdfminer.pdfparser import PDFDocument, PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine

def convert(path_pdf, path_txt):

    fp = open(path_pdf, 'rb')

    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    #I changed the following 2 parameters to get rid of white spaces inside words:
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    extracted_text = ''

    # Process each page contained in the document.
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text+=lt_obj.get_text()

    if path_txt != 'None':
        with open(path_txt,"wb") as txt_file:
            txt_file.write(extracted_text.encode("utf-8"))

    return extracted_text.encode("utf-8")

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--filepdf')
    parser.add_argument('-t', '--filetxt')

    return parser

#debug
#sys.argv.append('-p vetDocument-4-4-full.pdf')
#sys.argv.append('-t convertedFile.txt')

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

try:
    txt = convert(str(namespace.filepdf).strip(),
                  str(namespace.filetxt)).strip()
    sys.exit(1)
except Exception as e:
    print('ERROR %s' % e)
    sys.exit(0)

