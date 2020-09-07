import re
import textract
# import PyPDF2
import fitz  # this is pymupdf
import ftfy




def pdf_to_text_pymupdf(pdf_file_path):
    with fitz.open(pdf_file_path) as doc:
        text_extracted = ""
        for page in doc:
            text_extracted += ftfy.fix_text(page.getText())

        return text_extracted.encode()


def pdf_to_text_textract(pdf_file_path):
    try:
        page_text = textract.process(pdf_file_path, encoding='ascii', method='pdfminer',
                                     layout=False)  # , encoding='ascii'
        print('method=pdfminer')
        return page_text
    except:
        pass

    try:
        page_text = textract.process(pdf_file_path, language='eng', method='tesseract',
                                     layout=False)  # , encoding='ascii'
        print('method=tesseract')
        return page_text
    except:
        pass

    try:
        page_text = textract.process(pdf_file_path, layout=False)  # , encoding='ascii'
        print('method=default')
        return page_text
    except:
        pass

    return ''


# def pdf_to_text_pypdf(_pdf_file_path):
#     pdf_content = PyPDF2.PdfFileReader(open(_pdf_file_path, "rb"))
#     # 'Rb' Opens a file for reading only in binary format.
#     # The file pointer is placed at the beginning of the file
#     text_extracted = ""  # A variable to store the text extracted from the entire PDF

#     for x in range(0, pdf_content.getNumPages()):  # text is extracted page wise
#         pdf_text = ""  # A variable to store text extracted from a page
#         pdf_text = pdf_text + pdf_content.getPage(x).extractText()
#         # Text is extracted from page 'x'
#         text_extracted = text_extracted + "".join(i for i in pdf_text if ord(i) < 128) + "\n\n\n"
#         # Non-Ascii characters are eliminated and text from each page is separated
#     return text_extracted

