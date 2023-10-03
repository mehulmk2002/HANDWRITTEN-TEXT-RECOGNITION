from tkinter import *
import tkinter.filedialog as fd
from PIL import ImageTk, Image
import math
import pickle
import numpy
import pytesseract
import cv2
import os
import shutil
from translate import Translator
from keras.models import load_model
#import sounddevice as sd
from scipy.io.wavfile import write
#import wavio as WV


def Check_image_history_folder():
    """ Function check setup related folder  """

    if os.path.isdir("./Image_data"):
        pass
    else:
        os.mkdir("./Image_data")

    if os.path.isfile("./Image_data/Image_data.pkl"):
        pass
    else:
        Image_data_pickle_file = open("./Image_data/Image_data.pkl", "wb")
        pickle.dump([], Image_data_pickle_file)
        Image_data_pickle_file.close()

    if os.path.isfile("./Image_data/Image_count.pkl"):
        pass
    else:
        Image_count_file = open("./Image_data/Image_count.pkl", "wb")
        pickle.dump([1], Image_count_file)
        Image_count_file.close()


# Call Setup folder checking function ...
Check_image_history_folder()


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


# Variable which store processing Image Path

filename = None

Open_image_path = None


def Open_image():
    """ Function which Option Image option window and process for translation """

    global Open_image_path, filename

    filetypes = (
        ('text files', '*.png'
                       ''),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    """ Read Image count pickle file """

    # Open Image count pickle file

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

    shutil.copy(filename, f'./Image_data/{Image_count}.png')
    Image_count_int = int(Image_count)

    # Write in Image count pickle file

    Image_count_file_write = open("./Image_data/Image_count.pkl", "wb")
    pickle.dump([Image_count_int + 1], Image_count_file_write)
    Image_count_file_write.close()

    """ Store Process image path in Global variable """

    Open_image_path = filename

    # Disable main window

    Option_window.withdraw()

    # Open Image translation showing window

    Image_window()


def Convert_more_image():
    """ Function for convert more image for Image window function """

    global Image_window_list
    Option_window.deiconify()
    Image_window_list[0].withdraw()


def Image_window():
    """ Particular image window that translation of Uploaded image using image path"""

    global Open_image_path, Image_translation

    def Convert_to_other_language_function():
        Choose_language_option_window()

    """ Image window start """

    Image_window_screen = Toplevel(Option_window)

    # Call Update Image history data function

    Set_image_translation_history_data()

    # Store this window instance in list

    Image_window_list.clear()
    Image_window_list.append(Image_window_screen)

    """ Set Image window height and Width """

    Image_window_height = 600
    Image_window_width = 1100

    Image_window_x = (Image_window_screen.winfo_screenwidth() // 2) - (Image_window_width // 2)
    Image_window_y = (Image_window_screen.winfo_screenheight() // 2) - (Image_window_height // 2) - 30

    Image_window_screen.geometry(f'{Image_window_width}x{Image_window_height}+{Image_window_x}+{Image_window_y}')

    Image_window_screen.resizable(False, False)

    """ Image window main frame """

    Image_window_main_frame = Canvas(Image_window_screen, height=Image_window_height, width=Image_window_width,
                                     bg="white")
    Image_window_main_frame.place(x=0, y=0)

    # Division line

    Image_window_main_frame.create_line(601, 0, 601, 600, fill="#2c2c2c")

    """ 1. Main Image frame """

    Image_frame = Frame(Image_window_main_frame, height=Image_window_height, width=600,
                        bg="#ececec")
    Image_frame.place(x=0, y=0)

    # Open Processing Image

    Processing_image = Image.open(Open_image_path)
    Processing_image = Processing_image.resize((550, 550))
    Processing_image = ImageTk.PhotoImage(Processing_image)

    # Processing image shown label

    Processing_image_show = Label(Image_frame, image=Processing_image,
                                  bd=0)
    Processing_image_show.place(x=25, y=25)

    """ Output information shown main frame """

    Choose_language_transfer_language = Frame(Image_window_main_frame, height=600, width=500,
                                              bg='white')
    Choose_language_transfer_language.place(x=602, y=0)

    """ Translation title and Image translation show main frame """

    Output_information_frame = Canvas(Choose_language_transfer_language, height=540, width=500,
                                      bg='white', highlightthickness=0)
    Output_information_frame.place(x=0, y=0)

    # Translation title

    Translation_title = Label(Output_information_frame, text="Translation", font=("calibri", 13),
                              bd=0, fg='white', bg='#2c2c2c')
    Translation_title.place(x=5, y=5, relheight=0.06, relwidth=0.4)

    """ Translation shown frame """

    Image_output = Text(Output_information_frame, font=("calibri", 13), bd=0,
                        highlightthickness=1, highlightcolor="#f1f1f1", highlightbackground="#f1f1f1",
                        width=53, height=25)
    Image_output.place(x=8, y=50)

    # Translate text from Image using pytesseract

    Translate_object = Image.open(Open_image_path)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    Translate_text = pytesseract.image_to_string(Translate_object)
    Language_translation_text = Translate_text.replace("\n", "\t")

    # Add Translation text to global list

    Image_translation.clear()
    Image_translation.append(Language_translation_text)
    Image_output.insert('1.0', Translate_text)

    """ Convert more image and Translate to other language option main frame """

    Translate_to_another_copy = Frame(Choose_language_transfer_language, height=50, width=500, bg="#2c2c2c")
    Translate_to_another_copy.place(x=0, y=550)

    # 1. Convert more image option

    Convert_more_option_button = Button(Translate_to_another_copy, text="Convert more Image", bg="#ececec",
                                        bd=0, padx=3, pady=3, font=("calibri", 12),
                                        fg="#2c2c2c", cursor="hand2", command=Convert_more_image)
    Convert_more_option_button.place(x=10, y=10)
    Convert_more_option_button.bind('Enter', Option_button_hover_effect)
    Convert_more_option_button.bind('<Leave>', Option_button_remove_hover_effect)

    # 2. Convert to another language option

    Convert_to_another_language = Button(Translate_to_another_copy, text="Convert to another language", bg="#ececec",
                                         bd=0, padx=3, pady=3, font=("calibri", 12),
                                         fg="#2c2c2c", cursor="hand2", command=Convert_to_other_language_function,
                                         activebackground="#ececec", activeforeground="#2c2c2c")
    Convert_to_another_language.place(x=170, y=10)
    Convert_to_another_language.bind('<Enter>', Option_button_hover_effect)
    Convert_to_another_language.bind('<Leave>', Option_button_remove_hover_effect)

    Image_window_screen.config(bg="white")

    # Bind Close button property function
    Image_window_screen.protocol("WM_DELETE_WINDOW", Convert_more_image)
    Image_window_screen.mainloop()


# Store Image translation text and Image window name in list

Image_translation = []

Image_window_list = []

# Store convert text to another language output

Translation_language_output = []

Convert_language_screen_name = []


def Choose_language_option_window():
    """ Window which available language option for image translation data """

    global Image_translation, Translation_language_output

    def Label_hover_effect(event):
        """ Label hover effect """

        event.widget.config(fg="#050505")

    def Label_hover_effect_remove(event):
        """ Label remove hover effect """

        event.widget.config(fg="#212121")

    def Convert_to_another_language_function(language):
        """ Function which convert Image translation to another language """

        translator = Translator(to_lang=language)
        translation = translator.translate(Image_translation[0])

        Translation_language_output.clear()
        Translation_language_output.append(translation)

        Choose_language.destroy()
        Language_translation_window()

    """ Choose language option window """

    Choose_language = Toplevel()

    # Store window name in list

    Convert_language_screen_name.clear()
    Convert_language_screen_name.append(Choose_language)

    # Set window Height and Width

    Choose_language_screen_height = 400
    Choose_language_screen_width = 300
    Choose_language_x = (Choose_language.winfo_screenwidth() // 2) - (Choose_language_screen_width // 2)
    Choose_language_y = (Choose_language.winfo_screenheight() // 2) - (Choose_language_screen_height // 2)
    Choose_language.geometry(
        f'{Choose_language_screen_width}x{Choose_language_screen_height}+{Choose_language_x}+{Choose_language_y}')

    # Set Title

    Choose_language.title("Choose translation language")
    Choose_language.resizable(False, False)

    # Choose language main title

    Choose_language_title = Label(Choose_language, text="Choose language", font=("calibri", 13), bd=0, fg="#2f00ff",
                                  bg='white')
    Choose_language_title.pack(anchor=CENTER, pady=5)

    """ All available language option """

    # 1. Hindi option

    Hindi_option = Button(Choose_language, text="Hindi", bg="#ececec", font=("calibri", 12), bd=0,
                          fg='#2c2c2c', cursor="hand2", command=lambda: Convert_to_another_language_function("Hindi"))
    Hindi_option.pack(anchor=CENTER, pady=7, ipadx=1, ipady=4)
    Hindi_option.bind('<Enter>', Label_hover_effect)
    Hindi_option.bind('<Leave>', Label_hover_effect_remove)

    # 2. English option

    English_option = Button(Choose_language, text="English", bg="#ececec", font=("calibri", 12), bd=0,
                            fg='#2c2c2c', command=lambda: Convert_to_another_language_function("eng"),
                            cursor="hand2")
    English_option.pack(anchor=CENTER, pady=7, ipadx=0.5, ipady=4)
    English_option.bind('<Enter>', Label_hover_effect)
    English_option.bind('<Leave>', Label_hover_effect_remove)

    # 3. German option

    German_option = Button(Choose_language, text="German", bg="#ececec", font=("calibri", 12), bd=0,
                           fg='#2c2c2c', command=lambda: Convert_to_another_language_function("GERMAN"),
                           cursor="hand2")
    German_option.pack(anchor=CENTER, pady=7, ipadx=1, ipady=4)
    German_option.bind('<Enter>', Label_hover_effect)
    German_option.bind('<Leave>', Label_hover_effect_remove)

    # 4. Spanish option

    Spanish_option = Button(Choose_language, text="Spanish", bg="#ececec", font=("calibri", 12), bd=0,
                            fg='#2c2c2c', command=lambda: Convert_to_another_language_function("SPANISH"),
                            cursor="hand2")
    Spanish_option.pack(anchor=CENTER, pady=7, ipadx=1, ipady=4)
    Spanish_option.bind('<Enter>', Label_hover_effect)
    Spanish_option.bind('<Leave>', Label_hover_effect_remove)

    # Set background color

    Choose_language.config(bg='white')
    Choose_language.mainloop()


def Language_translation_window():
    """ Image data translation output shown window """

    Convert_data = Toplevel()

    # Set window Height and Width

    Convert_data_screen_height = 500
    Convert_data_screen_width = 600
    Convert_data_x = (Convert_data.winfo_screenwidth() // 2) - (Convert_data_screen_width // 2)
    Convert_data_y = (Convert_data.winfo_screenheight() // 2) - (Convert_data_screen_height // 2)
    Convert_data.geometry(
        f'{Convert_data_screen_width}x{Convert_data_screen_height}+{Convert_data_x}+{Convert_data_y}')

    # Set Title

    Convert_data.title("Translation")
    Convert_data.resizable(False, False)

    """ Convert data show main frame """

    Convert_data_main_frame = Frame(Convert_data, height=500, width=600, bg="white", bd=0)
    Convert_data_main_frame.place(x=0, y=0)

    # Convert data

    Convert_data_text_widget = Text(Convert_data_main_frame, height=23, width=65, bd=0, font=("calibri", 13))
    Convert_data_text_widget.place(x=10, y=10)
    Convert_data_text_widget.insert('1.0', Translation_language_output[0])

    # Set background color

    Convert_data.config(bg='white')
    Convert_data.mainloop()


def Image_history_click(event, path):
    """ Function which run when user click on any history related image """

    global Open_image_path

    # Set Image path
    Open_image_path = path
    print("path is: ",path)
    # Hide Option window
    Option_window.withdraw()

    # Run Image window function
    Image_window()


""" Canvas scrolling related function """


def Main_mousewheel_function(event):
    """ Mouse wheel function """

    Image_history_list_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')


def Enter_main_file_frame(event):
    # -- Bind MouseWheel event
    Image_history_list_canvas.bind_all('<MouseWheel>', Main_mousewheel_function)


def Leave_main_file_frame(event):
    # -- Unbind MouseWheel event
    Image_history_list_canvas.unbind_all('<MouseWheel>')


# Set Flag value for History images related click

Call_Image_window_flag = 0


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

            Option_window.withdraw()

    cam.release()

    cv2.destroyAllWindows()

    # Call Open Image window function
    if Call_Image_window_flag == 1:
        Image_window()


# List which store Traffic rule show screen name

Traffic_list_screen_list = []


def Close_screen():
    Option_window.deiconify()
    Traffic_list_screen_list[0].withdraw()


# Store Live traffic rule detection related image path

Live_traffic_rule_detection_image_path = None

Screen_call = 0



""" --- Main window  --- """

Option_window = Tk()

# Window Height and Width

Option_window_height = 550
Option_window_width = 700
Option_window_x = (Option_window.winfo_screenwidth() // 2) - (Option_window_width // 2)
Option_window_y = (Option_window.winfo_screenheight() // 2) - (Option_window_height // 2)

# Window Background color

Option_window_background_color = "white"

Option_window.geometry(f'{Option_window_width}x{Option_window_height}+{Option_window_x}+{Option_window_y}')

# Window Title

Option_window.title("Image automation")

""" All option frame and History data frame """

Option_and_history_frame = Frame(Option_window, height=Option_window_height, width=Option_window_width,
                                 bg=Option_window_background_color)
Option_and_history_frame.place(x=0, y=0)

""" All option frame """

Option_frame = Frame(Option_window, height=65, width=Option_window_width, bg="#2c2c2c")
Option_frame.place(x=0, y=0)

# 1. Image upload option
Image_upload_option = Button(Option_frame, text="Upload Image", bg="#ececec",
                             bd=0, padx=3, pady=3, font=("calibri", 12),
                             fg="#2c2c2c", cursor="hand2", command=Open_image, activebackground='#ececec',
                             activeforeground="#2c2c2c")
Image_upload_option.place(x=15, y=15)
Image_upload_option.bind('<Enter>', Option_button_hover_effect)
Image_upload_option.bind('<Leave>', Option_button_remove_hover_effect)

# 2. Live detection option
Live_detection_option = Button(Option_frame, text="Live detect", bg="#ececec",
                               bd=0, padx=3, pady=3, font=("calibri", 12),
                               fg="#2c2c2c", cursor="hand2", activebackground='#ececec',
                               activeforeground="#2c2c2c", command=Live_detect_image)
Live_detection_option.place(x=130, y=15)
Live_detection_option.bind('<Enter>', Option_button_hover_effect)
Live_detection_option.bind('<Leave>', Option_button_remove_hover_effect)


# 5. Sound record


# Translation image history information label

Translation_image_history_title = Label(Option_and_history_frame, text="History", font=("calibri", 13),
                                        fg="#0010ff", bg="white")
Translation_image_history_title.place(x=10, y=68)

Image_history_main_frame = Frame(Option_and_history_frame, width=Option_window_width, height=550, bd=0,
                                 bg="white")
Image_history_main_frame.place(x=0, y=100)

# Base-canvas
Image_history_list_canvas = Canvas(Image_history_main_frame, width=Option_window_width - 2, height=400,
                                   bg="white", highlightthickness=0, bd=0)
Image_history_list_canvas.pack(side="left")

# Base-scroll-frame
Image_history_frame = Frame(Image_history_list_canvas, bg="white", height=445)
Image_history_list_canvas.create_window((0, 0), window=Image_history_frame, anchor='nw')


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
        Option_window.update()


Set_image_translation_history_data()

# Set Background color

Option_window.resizable(False, False)
Option_window.config(bg=Option_window_background_color, highlightthickness=1, highlightcolor="#2c2c2c",
                     highlightbackground="#2c2c2c")

Option_window.mainloop()
