import argparse
import json
import pickle
import math
import shutil
from typing import Tuple, List
import cv2
import editdistance
from path import Path
from dataloader_iam import Batch
from model import Model, DecoderType
from preprocessor import Preprocessor
import os
from tkinter.filedialog import askopenfile
import tkinter.filedialog as fd
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from translate import Translator
import cv2
import matplotlib.pyplot as plt
import pytesseract
import re
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from gtts import gTTS
from playsound import playsound

recval=''
img_path=''
tem_hi_list=[]

#================image proceessing============================

def call_img(img_path):
    #select_image()
    img = cv2.imread(img_path)
    img10=cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Convert to RGB 

    bfilter = cv2.bilateralFilter(img, 50, 100,50)
    edged = cv2.Canny(bfilter, 30, 200) 
    img=cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)
    img = draw_boxes_on_text(img,img10)

def draw_boxes_on_text(img,img10):
    import os
  
    import shutil

    # Deleting an non-empty folder
    dir_path = r"img"
    shutil.rmtree(dir_path, ignore_errors=True)
    print("Deleted '%s' directory successfully" % dir_path)

    path = 'img'
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)

    raw_data = pytesseract.image_to_data(img)
    img_c=0
    print(raw_data)
    for count, data in enumerate(raw_data.splitlines()):

        if count > 0:
            data = data.split()
            if len(data) == 12:
                x, y, w, h, content = int(data[6]), int(data[7]), int(data[8]), int(data[9]), data[11]
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 255, 0), 1)
                print("X",x,"X2:",w+x," Y",y," y:",h+y)
                crop = img10[y-1:y+h+1,x-1:x+w+1] 
                count_img = str(img_c)
                img_c=img_c+1
                iname="./img/"+count_img+".png"
                cv2.imwrite(iname,crop)
              
    return img


#====================3.....<MODEL>

class FilePaths:
    fn_char_list = '../model/charList.txt'
    fn_summary = '../model/summary.json'
    fn_corpus = '../data/corpus.txt'

def get_img_height() -> int:
    return 32

def get_img_size(line_mode: bool = False) -> Tuple[int, int]:
   
    if line_mode:
        return 256, get_img_height()
    return 128, get_img_height()

def char_list_from_file() -> List[str]:
    with open(FilePaths.fn_char_list) as f:
        return list(f.read())

history_list=[]
def infer(model: Model, fn_img: Path) -> None:

    img = cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE)
    assert img is not None

    preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
    img = preprocessor.process_img(img)

    batch = Batch([img], None, 1)
    recognized, probability = model.infer_batch(batch, True)
    print(f'Recognized: "{recognized[0]}"')
    recVal=recognized[0]+" "
    #input_text.set(recVal)
    notepad.insert(END,recVal)
    global tem_hi_list
    tem_hi_list.append(recVal)
    print(f'Probability: {probability[0]}')
    
def main():
    global args
    global model
    
    decoder_mapping = {'bestpath': DecoderType.BestPath,
                       'beamsearch': DecoderType.BeamSearch,
                       'wordbeamsearch': DecoderType.WordBeamSearch}
    
    decoder_type = decoder_mapping['bestpath']

    model = Model(char_list_from_file(), decoder_type, must_restore=True, dump=False)
#======Calling The Model============    
main()

#=======</MODEL>


#========Open the IMG after that recognized text and save into History=============================

def open_file():
   
   global img_path
   filetypes = (
        ('text files', '*.png;*.jpg;*.jpeg'
                       ''),
        ('All files', '*.*')
    )

   img_path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
   
   print("path :=====> ",img_path)



   Image_count_file_read = open("./Image_data/Image_count.pkl", "rb")
   Image_count_file_data = pickle.load(Image_count_file_read)
   Image_count = Image_count_file_data[0]
   Image_count_file_read.close()

   """ Update All Process Image data storage file """

   Image_data_pickle_read = open("./Image_data/Image_data.pkl", "rb")
   Image_data = pickle.load(Image_data_pickle_read)
   Image_data_pickle_read.close()

    # Add New Image count value in previous data
   Image_data.append(Image_count)

   Image_data_pickle_write = open("./Image_data/Image_data.pkl", "wb")
   pickle.dump(Image_data, Image_data_pickle_write)
   Image_data_pickle_write.close()

   """ Copy Process Image from source to destination """

   shutil.copy(img_path, f'./Image_data/{Image_count}.png')
   Image_count_int = int(Image_count)

    # Write in Image count pickle file

   Image_count_file_write = open("./Image_data/Image_count.pkl", "wb")
   pickle.dump([Image_count_int + 1], Image_count_file_write)
   Image_count_file_write.close()

   """ Store Process image path in Global variable """

   Open_image_path = img_path

    # Disable main window

   #Window.withdraw()

   call_img(img_path)
   handwritten_recognized_text(img_path)
#Recognizing One By One IMG=====            
   pt="E:/8th_Sem_FSEP/Notebook/src/img/"
#    if filetypes:
   if False:
        import os
        lst = os.listdir("./img/") # your directory path
        number_files = len(lst)
        global tem_hi_list
        tem_hi_list=[]
        for i in range(0,number_files):
            nm=str(i)
            infer(model,pt+nm+".png")
        history_list.append(tem_hi_list)


#================ O Charecter Recognition ============================

def handwritten_recognized_text(img_path):
        

    import cv2
    import string
    import pytesseract
    import matplotlib.pyplot as plt
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    bfilter = cv2.bilateralFilter(img, 50, 100,50)
    edged = cv2.Canny(bfilter, 30, 200) 
    img=cv2.cvtColor(edged, cv2.COLOR_BGR2RGB)
    texts = pytesseract.image_to_string(img)
    print(texts)
    notepad.insert(END,texts)

#============4.....Open MCQ Test Checker Window============================================ 

def mcq_test_checker():
    Window.destroy()
    from MCQ_Test_Checker import MCQ_Test_Checker


#============4.....translate Function============================================ 
def translate():
    inputValue=notepad.get("1.0","end-1c")
    print("Value is{ "+inputValue+" }")

    translated_string=inputValue

    translator=Translator(to_lang="hi")
    translation=translator.translate(translated_string)
    print(translation)
    translated_text.delete("1.0","end")
    translated_text.insert(END,translation)

#======PDF

def pdf_convertor():
    
    
    from fpdf import FPDF
    
    
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)
    
    pdf_recognized_text=notepad.get("1.0","end-1c")
    #pdf_translated_text=translated_text.get("1.0","end-1c")

    print("me:  ",pdf_recognized_text)
    # pdf.cell(200, 10, txt = pdf_translated_text,
    #         ln = 1)
    
    x = re.split("\n", pdf_recognized_text)
    print('LIIIIIST ISSSS:',x)
    for cell in x:
        print("======>",cell)
    # add another cell
        pdf.cell(200, 10, txt = cell,
            ln = 2)
    
    # save the pdf with name .pdf
    pdf.output("myPDF.pdf") 


#============5.....Audio Code============================================ 
an=0
def audio():
    inputValue=notepad.get("1.0","end-1c")
    print("hello")
    tts = gTTS(inputValue)
    str_au=str(an)+'Audio.mp3'
    tts.save(str_au)
   
    # import required module

    # for playing note.mp3 file
    playsound(str_au)

def audioH():
    inputValue=translated_text.get("1.0","end-1c")
    print("hello")
    tts = gTTS(inputValue)
    tts.save('Audio1.mp3')

    # for playing note.mp3 file
    playsound('Audio1.mp3')    


#========6 Main GUI========>>>>>>>>>>>>>>>>>>>>>>>>>>
Window = tk.Tk()
from PIL import Image, ImageTk
Window.title('Handwritten Text Recognizer')
Window.minsize(1210, 700)
Window.maxsize(1210, 700)
Window.resizable(False, False)
Window.configure(bg='skyblue')


import cv2
import os

def Live_detect_image():
    """ Function which detect live image and translate """

    global Open_image_path, filename, Call_Image_window_flag

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed

            Image_count_file_read = open("./Image_data/Image_count.pkl", "rb")
            Image_count_file_data = pickle.load(Image_count_file_read)
            Image_count = Image_count_file_data[0]
            Image_count_file_read.close()

            img_name = f"{Image_count}.png"
            cv2.imwrite(f"./Image_data/{img_name}", frame)
            img_counter += 1

            Call_Image_window_flag = 1

            # Set filename
            filename = f"./{img_name}"

            # Read Image data pickle file

            Image_data_pickle_read = open("./Image_data/Image_data.pkl", "rb")
            Image_data = pickle.load(Image_data_pickle_read)
            Image_data_pickle_read.close()

            # Append value in Image data list

            Image_data.append(Image_count)

            # Write Image data pickle file

            Image_data_pickle_write = open("./Image_data/Image_data.pkl", "wb")
            pickle.dump(Image_data, Image_data_pickle_write)
            Image_data_pickle_write.close()

            Image_count_int = int(Image_count)

            # Update Image count value in Image count txt file

            Image_count_file_write = open("./Image_data/Image_count.pkl", "wb")
            pickle.dump([Image_count_int + 1], Image_count_file_write)
            Image_count_file_write.close()

            Open_image_path = f"./Image_data/{filename}"

            print("==> ",Open_image_path)
            if Call_Image_window_flag == 1:
                handwritten_recognized_text(Open_image_path)
    cam.release()

    cv2.destroyAllWindows()

    # Call Open Image window function




def Option_button_hover_effect(event):
    """ Option button Hover effect function """

    Option_button = event.widget

    # Change background color
    Option_button.config(bg="white")


def Option_button_remove_hover_effect(event):
    """ Option button remove hover effect function """

    Option_button = event.widget

    # Change Background color
    Option_button.config(bg="#ececec")



Option_window_height = 550
Option_window_width = 1210

Option_frame = Frame(Window, height=65, width=Option_window_width, bg="#2c2c2c")
Option_frame.place(x=0, y=0)

# 1. Image upload option
Image_upload_option = Button(Option_frame, text="Upload Image", 
                             bd=0, padx=3, pady=0, font=("calibri", 16,'bold'),
                             fg="white",bg="#2c2c2c", cursor="hand2", activebackground='#ececec',
                             activeforeground="#2c2c2c",command=open_file)
Image_upload_option.place(x=10, y=15)

# 2. Live detection option
Live_detection_option = Button(Option_frame, text="Live Detect",
                               bd=0, padx=3, pady=0, font=("calibri", 16,'bold'),
                               fg="white",bg="#2c2c2c", cursor="hand2", activebackground='#ececec',
                               activeforeground="#2c2c2c", command=Live_detect_image)
Live_detection_option.place(x=165, y=15)

# 3. Traffic rule detection image upload option
Traffic_rule_image_option = Button(Option_frame, text="Normal Text Image",
                                   bd=0, padx=3, pady=0, font=("calibri", 16,'bold'),
                                   fg="white",bg="#2c2c2c", cursor="hand2", activebackground='#ececec',
                                   activeforeground="#2c2c2c", command=open_file)
Traffic_rule_image_option.place(x=300, y=15)

# 4. Live traffic rule detection option

Live_traffic_rule_option = Button(Option_frame, text="MCQ Test Checker", 
                                  bd=0, padx=3, pady=0, font=("calibri", 16,'bold'),
                                  fg="white",bg="#2c2c2c", cursor="hand2", activebackground='#ececec',
                                  activeforeground="#2c2c2c", command=mcq_test_checker)
Live_traffic_rule_option.place(x=500, y=15)





#=========================Nave-Bar=================
Upload_image_option = Button(Window, text="Upload Image", bg="#2c2c2c",bd=0, padx=3, pady=6, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", width = 22, command=open_file)
Live_image= Button(Window, text="Live Detect", bg="#2c2c2c",bd=0, padx=3, pady=6, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white",width = 22,command=Live_detect_image)
Normal_text = Button(Window, text="Normal Text Image", bg="#2c2c2c",bd=0, padx=3, pady=6, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white",width = 22,command=open_file)
MCQ_Ans_Sheet = Button(Window, text="MCQ Test Checker", bg="#2c2c2c",bd=0, padx=3, pady=6, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white",width = 22, command=mcq_test_checker)

# Upload_image_option.place(x=10, y=10)
# Live_image.place(x=210, y=10)
# Normal_text.place(x=410, y=10)
# #Online_Text_Rec.place(x=610, y=10)
# MCQ_Ans_Sheet.place(x=810, y=10)
# #Other_activity.place(x=1010, y=10)

# our_canvas=Canvas(Window,width=1190,height=10,bg="skyblue")
# our_canvas.place(x=8, y=60)
# our_canvas.create_rectangle(0,0,1190,10,outline= 'skyblue',width=4,fill="blue")

input_text = StringVar()


#=========================History 331-480 Line=================

# Create a list to keep track of the images

images = []

history_title=Label(Window,text="History",font=('calibri 16'),fg="blue")
history_title.place(x=530, y=75)

Option_window_height = 570
Option_window_width = 670
Option_window_background_color = "white"

Option_and_history_frame = Frame(Window, height=Option_window_height, width=Option_window_width+10,
                                 bg=Option_window_background_color, highlightbackground="blue", highlightthickness=2)
Option_and_history_frame.place(x=520, y=110)


# Translation image history information label

Image_history_main_frame = Frame(Option_and_history_frame, width=Option_window_width, height=Option_window_height, bd=0,
                                 bg="white")
Image_history_main_frame.place(x=0, y=2)

# Base-canvas
Image_history_list_canvas = Canvas(Image_history_main_frame, width=Option_window_width - 2, height=400,
                                   bg="white", highlightthickness=0, bd=0)
Image_history_list_canvas.pack(side="left")

# Base-scroll-frame
Image_history_frame = Frame(Image_history_list_canvas, bg="white", height=445)
Image_history_list_canvas.create_window((0, 0), window=Image_history_frame, anchor='nw')

def Main_mousewheel_function(event):
    """ Mouse wheel function """

    Image_history_list_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')


def Enter_main_file_frame(event):
    # -- Bind MouseWheel event
    Image_history_list_canvas.bind_all('<MouseWheel>', Main_mousewheel_function)


def Leave_main_file_frame(event):
    # -- Unbind MouseWheel event
    Image_history_list_canvas.unbind_all('<MouseWheel>')

# Create scrolling function
def Scroll_function(event):
    Image_history_list_canvas.configure(scrollregion=Image_history_list_canvas.bbox("all"))

Image_history_frame.bind("<Configure>", Scroll_function)
Image_history_frame.bind('<Enter>', Enter_main_file_frame)
Image_history_frame.bind('<Leave>', Leave_main_file_frame)

# Image count start
Image_count_start = 1
# Image label count
Image_label_count = 0
# Image history count data
Image_history_count = None

def Image_history_click(event, path):
    """ Function which run when user click on any history related image """

    global Open_image_path

    # Set Image path
    Open_image_path = path
    print("path is: ",path)
    # Hide Option window
    # Window.withdraw()
    #infer(model,pt+nm+".png")
    call_img(path)
    #infer(model,path)
    #call_img(img_path)
    handwritten_recognized_text(path)
                
    pt="E:/8th_Sem_FSEP/Notebook/src/img/"

   # if path:
    if False:
        import os
        lst = os.listdir("./img/") # your directory path
        number_files = len(lst)
       
        tem_hi_list=[]
        for i in range(0,number_files):
            nm=str(i)
            infer(model,pt+nm+".png")
        

    # # Run Image window function
    # Image_window()



def Set_image_translation_history_data():
    """ Function which set Image History data """

    global Image_count_start, Image_history_count

    Image_count_start = 1

    for item in Image_history_frame.winfo_children():
        item.destroy()

    Image_history = open("./Image_data/Image_count.pkl", "rb")
    Image_history_count = pickle.load(Image_history)
    Image_history.close()

    for i in range(math.ceil(Image_history_count[0] / 4)):
        # Image history particular frame

        Image_history_particular_frame = Frame(Image_history_frame, height=120, width=Option_window_width - 10,
                                               bg="white")
        Image_history_particular_frame.grid(row=i, column=0, pady=10)
        Image_history_particular_frame.update()

        for k in range(5):

            if Image_count_start < Image_history_count[0]:
                # Load image
                Particular_image = Image.open(f'./Image_data/{Image_count_start}.png')
                Particular_image = Particular_image.resize((150, 90))
                Particular_image = ImageTk.PhotoImage(Particular_image)

                # Image history label
                Image_label = Label(Image_history_particular_frame, image=Particular_image, bg="white",
                                    cursor="hand2")
                Image_label.grid(row=i, column=k, padx=10)
                Click_image_path = f"./Image_data/{Image_count_start}.png"
                Image_label.bind('<Button-1>',
                                 lambda event, value1=Click_image_path: Image_history_click(event, value1))
                Image_label.image = Particular_image

                # Update Image count value
                Image_count_start = Image_count_start + 1

        Image_history_main_frame.update()
        Image_history_list_canvas.update()
        Window.update()


Set_image_translation_history_data()


#=================Recognized Text=================

notepad=Text(Window,font=('Courier 18'),borderwidth=1, relief="solid")
#input_text.set('OutPut')
notepad.place(x=4, y=110,height=250, width=500)


#=================Translate & PDF BUTTON=================

Translate_Button = Button(Window, text="Translate", bg="#2E4F4F",bd=0, padx=40, pady=3, font=("calibri", 14),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white",command=lambda: translate())
Translate_Button.place(x=50, y=370)

PDF_Button = Button(Window, text="PDF", bg="#0E8388",bd=0, padx=40, pady=3, font=("calibri", 14),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white",command=lambda: pdf_convertor())
PDF_Button.place(x=300, y=370)

#=================Translated Text=================
translated_text=Text(Window,font=('Courier 18'),borderwidth=1, relief="solid")
translated_text.place(x=4, y=420,height=250, width=500)

#=================Speach Icon=================
p1 = PhotoImage(file = 'sp.png')
Text_Speech = Button(Window, text="Text Speech",image = p1, bg="#ffffff",bd=0, command=lambda: audio())
Text_Speech.place(x=470, y=330)
Text_Speech = Button(Window, text="Text Speech",image = p1, bg="#ffffff",bd=0,command=lambda: audioH())
Text_Speech.place(x=470, y=640)


Window.mainloop()
