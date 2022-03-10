from pdf2image import convert_from_path 
import textract
import pytesseract
import os
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'
cwd = os.getcwd()
path1 = os.path.join(cwd,"Report_for_KH1000082166 (1).pdf")
print(path1)

def extraction(path1):
    # text = textract.process(path1)
    # text = b''.join([text])
    # inter = text.decode("utf-8")
    #if "\x0c\x0c\x0c\x0c\x0c" in inter:
    pages=convert_from_path(path1,poppler_path=r'C:\Users\Nitin\Desktop\Hacks\TSEC_Hacks_2022\src\ResearchPoint\poppler-0.68.0\bin')
    image_counter=1
    for page in pages:
        filename= "page_"+str(image_counter)+".jpg"
        page.save(path1+filename,'JPEG')
        image_counter=image_counter+1
        filelimit=image_counter
        text=''
        for i in range(1,filelimit):
            filename=path1+"page_"+str(i)+".jpg"
            text=text + str(((pytesseract.image_to_string(Image.open(filename)))))
            
        inter=text

    return inter