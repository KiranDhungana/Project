

from fileinput import filename
import os
import PyPDF2  # module for pdf manipulation
from difflib import Differ, SequenceMatcher
# Python-tesseract is an optical character recognition (OCR) tool for python. That is, it will recognize and “read” the text embedded in images. ##If you don't have tesseract executable in your PATH, include the following: # pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>' # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
import pytesseract
import tkinter as tk  # Module for UI
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile  # module to open file
from PIL import Image, ImageTk  # To load the image, imported the image module


def browseFiles():
    filename = filedialog.askopenfilename(multiple=True, initialdir=".", title="Select a File", filetypes=(
        ("Text files", "*.pdf*"), ("all files", "*.*")))
    if(len(filename))==1:
     print("can't compare single file ")
    for i in range(0, len(filename)):
        if(os.path.exists('pdfcomp%d.txt' % i)):
            os.remove('pdfcomp%d.txt' % i)
        else:
            break

    l = Label(my_w, text=filename, font=('Helvetica bold', 8), wraplength=300)
    l.grid(column=1)

    # print(len(filename))
    i = 0

    while i < len(filename):

        pdf_file = open(filename[i], 'rb') #opens the file in binary format for reading
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        total_pages = pdf_reader.getNumPages()
        # print(
        #     f"The total number of pages in the pdf document is {pdf_reader.numPages}")

        for x in range(total_pages):
            page = pdf_reader.getPage(x)
            textdata = page.extractText()
            with open('pdfcomp%d.txt' % i, 'a', encoding='utf-8', errors='ignore') as f:

                f.write(textdata)
            # print(textdata)

        i = i+1

    for i in range(0, len(filename)):
        for j in range(i+1, len(filename)):
            if(filename[i] != filename[j]):
                with open('pdfcomp%d.txt' % i, encoding="utf8")as file1, open('pdfcomp%d.txt' % j, encoding="utf8")as file2:
                    file1data = file1.read()
                    file2data = file2.read()
                    s = SequenceMatcher(None, file1data, file2data).ratio()
                print(
                    f"The similarity between the text in pdf {i+1} and {j+1} is {s*100}%")








def upload_image():

    f_types = [('Jpg Files', '*.jpg'),
               ('PNG Files', '*.png'), ("all files", "*.*")]   # type of files to select
    filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
    if(len(filename))==1:
     print("can't compare single file ")
    for i in range(0, len(filename)):
        if(os.path.exists('pdfcomp%d.txt' % i)):
            os.remove('pdfcomp%d.txt' % i)
        else:
            break
    # print(filename)# read the image file
    col = 1  # start from column 1
    row = 3  # start from row 3
    for f in filename:
        img = Image.open(f)
        img = img.resize((100, 100))  # new width & height
        img = ImageTk.PhotoImage(img)
        e1 = tk.Label(my_w)
        e1.grid(row=row, column=col)
        e1.image = img
        e1['image'] = img  # garbage collection
        if(col == 3):  # start new line after third column
            row = row+1  # start wtih next row
            col = 1    # start with first column
        else:       # within the same row
            col = col+1
    p = 0
    for x in filename:

        print(filename)
        image = filename[p]
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(Image.open(image), lang="eng")
        with open('comparision%d.txt' % p, 'w') as f:
            f.write(text)
        p = p+1

    for i in range(0, len(filename)):
        for j in range(i+1, len(filename)):
            if(filename[i] != filename[j]):
                with open('comparision%d.txt' % i)as file1, open('comparision%d.txt' % j)as file2:
                    file1data = file1.read()
                    file2data = file2.read()
                    s = SequenceMatcher(None, file1data, file2data).ratio()
            # l = Label(my_w, text=f"The similarity between the text {i+1} and {j+1} is {s*100}%", font=('Helvetica bold', 8), wraplength=300)
            # l.grid(column=1)        
            # text = Label(my_w, text=f"The similarity between the text {i+1} and {j+1} is {s*100}%")
            # text.place(x=40,y=180)        
            print(
                f"The similarity between the text in image {i+1} and {j+1} is {s*100}%")                    


# def pdftotext():
my_w = tk.Tk()
# pdftotext()
my_w.geometry("410x300")  # Size of the window
my_w.title('Plagiarism-checker')
my_font1 = ('times', 18, 'bold')
l1 = tk.Label(my_w, text='Choose pdf or image to compare',
              width=30, font=my_font1)
l1.grid(row=1, column=1, columnspan=4)
b1 = tk.Button(my_w, text='Upload Image',
               width=20, command=lambda: upload_image())
b1.grid(row=2, column=1, columnspan=4)
b2 = tk.Button(my_w, text='Upload file',
               width=20, command=lambda: browseFiles())
b2.grid(row=3, column=1, columnspan=4)



    #  p=p+1


# def converttexttoimage():
    # increase to next column
my_w.mainloop()  # Keep the window open
