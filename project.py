from cgitb import text
from lib2to3.pgen2.token import LEFTSHIFT
from textwrap import fill
import tkinter
from tkinter import *
from tkinter import filedialog
from turtle import title
from tkinter import messagebox
  

####################################################################################################
window = Tk()
window.resizable(0,0)


window.geometry('800x500')
window.config(bg='lightgrey')
window.title("PDF TO EPUB")
icon = PhotoImage(file="ebook.png")
window.iconphoto(True,icon)
choose_file = PhotoImage(file="choosefile.png")


def to_pub(file_path,save_path):
    import os
    from turtle import end_fill
    import fitz
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTFigure
    from pdfminer.layout import LTTextBoxHorizontal
    

    # print(save_path)
    # abcdef=input("look at save path")
    base_name = os.path.basename(file_path)
    file_name = os.path.splitext(base_name)[0]

    label9.config(text='10%')
    window.update_idletasks()

    os.chdir(save_path)
    page_no = -1
    img_li = []
    str1 = ''
    for page_layout in extract_pages(file_path):
        lii = []
        page_no = page_no + 1
        for element in page_layout:
            # print(element)
            i=0
            if isinstance(element, LTFigure):
                # print('image  ' + element.name + "  " + str(element.x1) + "  " + str(element.y1) )
                # diict[element.y1] = '{}.png'.format(element.name)
                lii.append([element.y1,'img','{}.png'.format(element.name)])
                img_li.append('{}.png'.format(element.name))

                output = PdfFileWriter() 
                input2 = PdfFileReader(open(file_path, 'rb')) 

                page = input2.getPage(page_no)
                page.cropBox.upperLeft = (element.x0,element.y0)
                page.cropBox.lowerRight = (element.x1,element.y1)
                output.addPage(page) 

                outputStream = open('{}.pdf'.format(element.name),'wb') 
                output.write(outputStream) 
                outputStream.close()
                # input.close() 
                # print("PDF {} created".format(element.name))

                pdffile = "{}.pdf".format(element.name)
                doc = fitz.open(pdffile)
                page = doc.load_page(0)  # number of page
                pix = page.get_pixmap()
                output = "{}.png".format(element.name)
                pix.save(output)
                doc.close()
                

            elif isinstance(element, LTTextBoxHorizontal):
                lii.append([element.y1,'text', element.get_text()])
                i=i+1
        # break  
        from operator import itemgetter
        lii = sorted(lii, key=itemgetter(0),reverse=True)
        # print('sortd list is : ')
        # print(lii)
        print("---------------------------image saved--------------------------------------")
        label9.config(text='40%')
        window.update_idletasks()


        for arr in lii:
            if arr[1] == 'text':
                str1 = str1 + "<p> {} </p>".format(arr[2])
            if arr[1] == 'img':
                str1 = str1 + '<p><img alt=" " src="images/{}" /><br/></p>'.format(arr[2])
        # print(str1)
    # print(str1)
    # print(img_li)

    #pdf metadata
    print("---------------After read,crop,png--------------------")

    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument


    print("---------------before meta--------------------")
    with open(file_path, 'rb') as fp:
        parser = PDFParser(fp)
        doc2 = PDFDocument(parser)

    dicc = doc2.info[0] #stored in dictornary
    # print(dicc)
    print("---------------after meta--------------------")

    # for keyss, valuess in dicc.items():
        # print(str(keyss)+" : "+str(valuess))


    label9.config(text='60%')
    window.update_idletasks()

    #creating ebook
    from ebooklib import epub
    from PIL import Image  # you need pip install Pillow
    import io
    import os
    import random
    book = epub.EpubBook()

    print("---------------Start ebook--------------------")
    #load image file
    imagess = []
    for images in os.listdir():
        # print(imageroot)
        if(images.endswith(".png") or images.endswith(".jpg") or images.endswith(".jpeg") or images.endswith(".bmp") and  os.path.basename(images) in img_li):
            imagess.append(images)
    # print(imagess)

    print("--------------ebook meta--------------------")
    #adding metadata
    uni_val = str(random.randrange(100000,999999))
    book.set_identifier('sample'+uni_val)# random.randrange(100000,999999)
    book.set_title('sample'+uni_val)# random.randrange(100000,999999)
    for keyss, valuess in dicc.items():
        book.set_unique_metadata('DC',str(keyss),str(valuess),None)

    print("---------------after ebook meta--------------------")
    # create chapter
    c1 = epub.EpubHtml(title='Sample', file_name='chap_01.xhtml', lang='hr')

    # <html><head></head><body><h1>Introduction</h1><p>Introduction paragraph where i explain what is happening.</p></body></html>
    c1.content=u'''<html><head> </head><body>  <h1> </h1> <p> !|CONTENT|! </p></body></html>'''
    c1.content = c1.content.replace('!|CONTENT|!',str1)

    # add chapter
    book.add_item(c1)

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    label9.config(text='70%')
    window.update_idletasks()

    print("---------------bef adding imgs to ebook--------------------")
    j=0 
    #while loop to add image 1 by 1 into epub
    while(j < len(imagess)):
        image_name = os.path.splitext(imagess[j])[0]
        image_ext = os.path.splitext(imagess[j])[1]
        img1 = Image.open(imagess[j])  # 'image1.jpeg' should locate in current directory for this example
        b = io.BytesIO()
        img1.save(b, image_ext.replace('.',''))
        b_image1 = b.getvalue()

        # define Image file path in .epub
        image1_item = epub.EpubItem(uid=image_name, file_name='images/{}'.format(imagess[j]), media_type='image/{}'.format(image_ext), content=b_image1)

        # add Image file
        book.add_item(image1_item)
        j=j+1

    label9.config(text='90%')
    window.update_idletasks()

    print("---------------after ebook add img--------------------")
    # add CSS file
    style = 'body {color: white;} img {align: center;} '
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)


    #epub spine
    book.spine = ['nav', c1]

    #saving epub
    epub.write_epub('{}.epub'.format(file_name), book, {})
    label9.config(text='100%')
    window.update_idletasks()
    print("---------------ebook created --------------------")
    

##############################################################################

def choose_fi():
    # print("you choosed a file")
    global str22
    file_path = filedialog.askopenfilename(filetypes = ( ('pdf files', '*.pdf'), ('All files', '*.*') ))
    file_path = file_path.replace('/','\\')
    str22 =r'{}'.format(file_path)
    print(str22)
    if str22:    
        button2.config(state=ACTIVE)



def save_loc():
    # print("you get saved location")
    global str33
    save_path = filedialog.askdirectory()
    save_path = save_path.replace('/','\\')
    str33 =r'{}'.format(save_path)
    print(str33)
    if str33:
        button3.config(state=ACTIVE)
    


def convert_save():
    print("before calling" + 'file path  ' +str22+ 'save path  ' +str33)
    label9.grid(row=0,column=3)
    to_pub(str22,str33)
    if label9.cget("text")=="100%":
        messagebox.showinfo("Info", "Task Completed")
    else:
        messagebox.showerror('Error','ERROR')




frame1=Frame(window, bg="#d2e5fc",width=800, height=120)
frame1.place(x=0,y=0,)

frame2=Frame(window, bg="#d2e5fc", width=800)
frame2.place(x=0,y=120)

frame6=Frame(window, bg="#d2e5fc", width=800, height=120)
frame6.place(x=0,y=380)

frame3=Frame(window, bg="#d2e5fc", width=800, height=120)
frame3.place(x=0,y=380)

frame4=Frame(window, bg="#d1d1d1", width=600, height=200)
frame4.place(x=100,y=150)

frame5=Frame(window, bg="#d1d1d1", width=500, height=150)
frame5.place(x=150,y=150)

frame6=Frame(window, bg="#d1d1d1", width=500, height=50)
frame6.place(x=150,y=300)


button1 = Button(frame6, text="Choose File",font=("Helvetica", 15),bg="#91c3ff",command=choose_fi)
button1.grid(row=0,column=0,padx=25)

button2 = Button(frame6, text="Save location",font=("Helvetica", 15),bg="#91c3ff",command=save_loc,state=DISABLED)
button2.grid(row=0,column=1,padx=25)

button3 = Button(frame6, text="Convert",font=("Helvetica", 15,),bg="#91c3ff",command=convert_save,state=DISABLED)
button3.grid(row=0,column=2,padx=25)



label1 = Label(window,text="PDF to EPUB converter",font=("Helvetica", 37,'bold'),background='#d2e5fc',)
label1.pack(pady=10)

label2 = Label(window,text="Convert PDF to EPUB offline and easily get eBook file format from PDF.",font=("Helvetica", 13),background='#d2e5fc')
label2.pack()

# choose_file = PhotoImage(file="choosefile.png")
label3 = Label(frame5,text="",background='#d1d1d1',image=choose_file)
label3.pack(padx=202)

label4 = Label(frame3,text="How to convert:",font=("Helvetica", 16,'bold'),background='#d2e5fc')
label4.grid(row=0,column=0,pady=5)

label5 = Label(frame3,text='''Step 1:\nAdd your PDF file using \nthe Choose File button''',font=("Helvetica", 13),background='#d2e5fc')
label5.grid(row=1,column=0,padx=35)

label6 = Label(frame3,text='''Step 2:\nDefine file\n saving path''',font=("Helvetica", 13),background='#d2e5fc')
label6.grid(row=1,column=1,padx=35)

label7 = Label(frame3,text='''Step 2:\nClick on \nConvert button''',font=("Helvetica", 13),background='#d2e5fc')
label7.grid(row=1,column=2,padx=35)

label8 = Label(frame3,text='''Step 3:\nWait for \nfew seconds''',font=("Helvetica", 13),background='#d2e5fc')
label8.grid(row=1,column=3,padx=35)

label9 = Label(frame6,text="00%",font=("Helvetica", 21,'bold'),background='#d2e5fc',)


window.mainloop()







