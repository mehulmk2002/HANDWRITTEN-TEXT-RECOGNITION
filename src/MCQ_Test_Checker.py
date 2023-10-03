from tkinter import *
import tkinter as tk
from tkinter import Label
newWindow = tk.Tk()
from PIL import Image, ImageTk
import pymysql.cursors
import datetime
from tkcalendar import Calendar, DateEntry
import re
from tkinter import filedialog
import tkinter.filedialog as fd
from tkinter import messagebox
import pickle
import math
import shutil
import cv2
result_Sheet_list=[]
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def insert_into_excel():
    file = filedialog.asksaveasfile(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                    defaultextension='.xlsx',
                                    filetypes=[
                                        ("xlsx file",".xlsx"),
                                        ("PDF file", ".pdf"),
                                    ])
    if file is None:
        return
    print(file)

    match=re.search('.pdf',file.name)
    
    def pdf_convertorm(Fpath):    
        global result_Sheet_list
        from reportlab.lib import colors  
        from reportlab.lib.pagesizes import letter, inch  
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle   
        
        my_doc = SimpleDocTemplate(Fpath, pagesize = letter)  
        my_obj = []  
        reco=len(result_Sheet_list)
        
        my_table = Table(result_Sheet_list, 1 * [1.0 * inch], reco * [0.25 * inch])  

        my_table.setStyle(  
        TableStyle(  
            [  
                ("ALIGN", (1, 1), (0, 0), "LEFT"),  
                ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
                ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),  
                ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
                ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),  
                ("BOX", (0, 0), (-1, -1), 2, colors.black),  
            ]  
        )  
        )  
        my_obj.append(my_table)  
        my_doc.build(my_obj)  
    
    if match:
        pdf_convertorm(file.name)

    else:
        import pandas as pd
        result_Sheet_list.pop(0)
        new_list =result_Sheet_list
        df = pd.DataFrame(new_list,columns =["Result Num",'Id Num','Exam','Sub','Max Marks','Ob marks','Date'])
        writer = pd.ExcelWriter(file.name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Result', index=False)
        writer.save()
        result_Sheet_list.insert(0,["Result Num",'Id Num','Exam','Sub','Max Marks','Ob marks','Date'])


#================================================Screen TWO (Filter)======================================================#
                        #===========================================================#

my_data=[ ["ID_NUMBER","EXAM", "SUBJECT", "MARKS","OBTAINED MARKS","DATE"]]

def data_ana_visua():
    dashboard = Toplevel(newWindow)

#=========student performance Line Chart======call by visualization function
    def student_performance():

        import pymysql.cursors
        db=pymysql.connect(host='localhost',
                                            user='root',
                                            password='Mysql12345',
                                            database='result',
                                            cursorclass=pymysql.cursors.DictCursor)
        cur=db.cursor()

        my_data=[]
        id_num=''
        sub=''
        exam=''
        if(id_number.get()!=''):
            id_num=' AND id_number=\''+id_number.get()+'\''
            print("Type: ",id_number.get())

        if(sub_name.get()!='Select an Subject' and sub_name.get()!='Whole Subject'):
            sub=' AND subjects=\''+sub_name.get()+'\''
            print("Type: ",sub_name.get())

        if(exam_name.get()!='Select an Exam' and exam_name.get()!='Whole Exam'):
            exam=' AND exams=\''+exam_name.get()+'\''
            print("Type: ",exam_name.get())

        sql = "select exams,subjects,max_marks,obtained_marks,Dates from results where 1=1 "+id_num+sub+exam+'ORDER BY Dates;'
        try:
            
            cur.execute(sql)
            #rt=cur.fetchone()
            #print(rt)
            results = cur.fetchall()
            r=1
            c=0
            score=[]
            x1_label=[]
            for row in results:
                mm=0.0
                om=0.0
                per=0.0
                l_exa=''
                l_sub=''
                label=''
                sp=0
                temp_list=[]
                for val in row.values():
                        if(sp==0):
                            l_exa=val+'-'
                            print("exam ma: ",val)

                        if(sp==1):
                            l_sub=val+'\n'
                            print("sub ma: ",val)

                        if(sp==2):
                            mm=float(val)
                            print("max ma: ",val)
                        if(sp==3):
                            om=float(val)
                            print("get ma: ",val)  
                            if(mm==0):
                                per=100
                                
                            else:
                                per=om/mm*100        
                            print("Percentage: ",per)  
                            score.append(per)    
                        if(sp==4):
                            #print(per)
                            print("date:",val)
                            temp_list.append(val)
                            c=c+1
                            label=val
                            x1_label.append(l_exa+l_sub+label)
                        
                        sp=sp+1
                r=r+1
                c=0
                my_data.append(temp_list)
        except:
            print ("Error: unable to fetch data")

        db.close()

        import numpy as np  
        import matplotlib.pyplot as plt  
            

        plt.figure()
        print(score)
        print(x1_label)
        Y1 = score
        X1 = x1_label #['EE(09/03/203)', 'os(09/03/203)', 'maths(09/03/203)', 'EE(04/03/203)', 'CC(09/03/203)', 'math(09/03/203)', 'EE(04/03/23)', 'CC(09/3/203)']  
        plt.plot(X1, Y1, '-bo')  
        plt.xticks(range(len(X1)), X1, rotation=45) 
        # Adding title and labels  
        plt.xlabel("Date")    
        plt.ylabel("Percentage")    
        plt.title("Perormance Of ID Number "+id_number.get())  
        figManager = plt.get_current_fig_manager()
        #figManager.window.showMaximized()
        # Displaying the second line chart with '-.' line  
        plt.show()  

        x = np.array(x1_label)
        y = np.array(score)

        plt.bar(X1,Y1)
        plt.show()

#==========================Percentage Wise Pie Chart=====call by visualization function
    def Category_Percentage():
        sub=''
        exam=''
        if(sub_name.get()!='Select an Subject' and sub_name.get()!='Whole Subject'):
            sub=' AND subjects=\''+sub_name.get()+'\''
            print("Type: ",sub_name.get())

        if(exam_name.get()!='Select an Exam' and exam_name.get()!='Whole Exam'):
            exam=' AND exams=\''+exam_name.get()+'\''
            print("Type: ",exam_name.get())

        import pymysql.cursors
        db=pymysql.connect(host='localhost',
                                            user='root',
                                            password='Mysql12345',
                                            database='result',
                                            cursorclass=pymysql.cursors.DictCursor)
        cur=db.cursor()

        my_data=[]
        id_num=''
        per_till_25=0.0
        per_till_50=0.0
        per_till_75=0.0
        per_till_100=0.0
        mco=0
        sql = "select max_marks,obtained_marks from results where 1=1 "+sub+exam+'ORDER BY Dates;'
        try:
            
            cur.execute(sql)
            #rt=cur.fetchone()
            #print(rt)
            results = cur.fetchall()
            r=1
            c=0
            score=[]

            for row in results:
               
                mm=0.0
                om=0.0
                per=0.0
               
                sp=0
                temp_list=[]
                for val in row.values():
                        
                        if(sp==0):
                            mm=float(val)
                            
                        if(sp==1):
                            om=float(val)
                             
                            if(mm==0):
                                per=100.0
                                
                            else:
                                per=om/mm*100  

                            if(0.0<=per and 25.0>=per):
                                per_till_25=per_till_25+1    
                            elif(26.0<=per and 50.0>=per):
                                per_till_50=per_till_50+1

                            elif(51.0<=per and 75.0>=per):
                                per_till_75=per_till_75+1
                            
                            elif(76.0<=per):
                                per_till_100=per_till_100+1
                            
                            print("Percentage: ",per) 
                            mco=mco+1 
                            score.append(per)       
                        sp=sp+1
                r=r+1
                c=0
                my_data.append(temp_list)
            print("total are: ",mco)
        except:
            print ("Error: unable to fetch data")

        db.close()

        import numpy as np
        import matplotlib.pyplot as plt


        # Creating dataset
        cars = ['0% - 25%', '26% - 50%', '51% - 75%',
                '76% - 100%']

        data = [per_till_25, per_till_50, per_till_75, per_till_100]

        explode = (0.1, 0.0, 0.2, 0.1)

        colors = ( "orange", "cyan", "brown",
                "grey", "indigo", "beige")


        wp = { 'linewidth' : 1, 'edgecolor' : "green" }

        def func(pct, allvalues):
            absolute = int(pct / 100.*np.sum(allvalues))
            return "{:.1f}%\n Student: {:d}".format(pct, absolute)

        fig, ax = plt.subplots(figsize =(10, 7))
        wedges, texts, autotexts = ax.pie(data,
                                        autopct = lambda pct: func(pct, data),
                                        explode = explode,
                                        labels = cars,
                                        shadow = True,
                                        colors = colors,
                                        startangle = 90,
                                        wedgeprops = wp,
                                        textprops = dict(color ="black"))


        ax.legend(wedges, cars,
                title ="Cars",
                loc ="center left",
                bbox_to_anchor =(1, 0, 0.5, 1))

        plt.setp(autotexts, size = 8, weight ="bold")
        ax.set_title("Students Percentage")

        # show plot
        plt.show()


#====Calling Two Function=== call by button
    def visualization():
        if(id_number.get()!=''):
                    # id_num=' AND id_number=\''+id_number.get()+'\''
                    # print("Type: ",id_number.get())
            student_performance()
        Category_Percentage()


    #=======1--. PDF Convertor==== call bye Button
    def pdf_convertor():
        pdf_data_fercher()
        global my_data
        from reportlab.lib import colors  
        from reportlab.lib.pagesizes import letter, inch  
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle   
        
        my_doc = SimpleDocTemplate("mark_sheet.pdf", pagesize = letter)  
        my_obj = []  
        reco=len(my_data)
        
        my_table = Table(my_data, 1 * [1.4 * inch], reco * [0.25 * inch])  

        my_table.setStyle(  
        TableStyle(  
            [  
                ("ALIGN", (1, 1), (0, 0), "LEFT"),  
                ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
                ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),  
                ("VALIGN", (-1, -1), (-1, -1), "TOP"),  
                ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),  
                ("BOX", (0, 0), (-1, -1), 2, colors.black),  
            ]  
        )  
        )  
        my_obj.append(my_table)  
        my_doc.build(my_obj)  

 #=======1--. PDF data_fercher==== call by pdf_convertor functiom
    def pdf_data_fercher():
                
        db=pymysql.connect(host='localhost',
                                        user='root',
                                        password='Mysql12345',
                                        database='result',
                                        cursorclass=pymysql.cursors.DictCursor)
        cur=db.cursor()
        sub=''
        exam_name=''
        id_num=''
        if(sub_name.get()!='Select an Subject' and sub_name.get()!='all'):
            sub=' AND subjects=\''+sub_name.get()+'\''
            print("Type: ",sub_name.get())

        if(id_number.get()!=''):
            id_num=' AND id_number=\''+id_number.get()+'\''
            print("Type: ",id_number.get())

        sql = "select * from results where 1=1 "+sub+id_num
        try:
            global my_data
            cur.execute(sql)
            #rt=cur.fetchone()
            #print(rt)
            results = cur.fetchall()
            r=1
            c=0

            for row in results:
                sp=0
                temp_list=[]
                for val in row.values():
                        if(sp==0):
                            print("return")
                        else:

                            temp_list.append(val)
                            c=c+1
                        sp=sp+1
                r=r+1
                c=0
                my_data.append(temp_list)
        except:
            print ("Error: unable to fetch data")
        
        db.close()


 #=======1--. Show Result in the form of table==== call by button
    def result_table():
                
        import pymysql
        from tkinter import ttk
        from tkinter import messagebox
        import tkinter as tk


        def connection():
            conn = pymysql.connect(
                host='localhost',
                user='root', 
                password='Mysql12345',
                db='result',
            )
            return conn

        def refreshTable():
            global result_Sheet_list
            result_Sheet_list=[["Result Num",'Id Num','Exam','Sub','Max Marks','Ob marks','Date']]
            for data in my_tree.get_children():
                my_tree.delete(data)
                
            for array in read():
                result_Sheet_list.append(list(array))
                print("=======>=======>",array,"type: ",type(array))
                my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

            my_tree.tag_configure('orow', background='#7C96AB', font=('Arial', 12))
            my_tree.grid(row=10, column=0, columnspan=5, rowspan=15, padx=10, pady=20)

        result_root =  Toplevel(newWindow)
        result_root.title("Student Result")
        #result_root.geometry("1080x780")
        result_root.minsize(1080, 780)
        result_root.maxsize(1080, 780)
        style = ttk.Style(result_root)

        style.theme_use("alt")

        my_tree = ttk.Treeview(result_root,show='headings', height=15)

        ph1 = tk.StringVar()
        ph2 = tk.StringVar()
        ph3 = tk.StringVar()
        ph4 = tk.StringVar()
        ph5 = tk.StringVar()
        ph6 = tk.StringVar()
        ph7 = tk.StringVar()

        def setph(word,num):
            if num ==1:
                resultidEntry.config(state="normal")
                ph1.set(word)
                resultidEntry.config(state="disabled")
                
            if num ==2:
                ph2.set(word)
            if num ==3:
                ph3.set(word)
            if num ==4:
                ph4.set(word)
            if num ==5:
                ph5.set(word)
            if num ==6:
                ph6.set(word)
            if num ==7:
                ph7.set(word)
        def read():
            conn = connection()
            cursor = conn.cursor()

            sub=''
            exam=''
            id_num=''
            if(sub_name.get()!='Select an Subject' and sub_name.get()!='Whole Subject'):
                sub=' AND subjects=\''+sub_name.get()+'\''
                print("Type: ",sub_name.get())

            if(exam_name.get()!='Select an Exam' and exam_name.get()!='Whole Exam'):
                exam=' AND exams=\''+exam_name.get()+'\''
                print("Type: ",exam_name.get())

            if(id_number.get()!=''):
                id_num=' AND id_number=\''+id_number.get()+'\''
                print("Type: ",id_number.get())

            sql = "select * from results where 1=1 "+sub+id_num+exam+'ORDER BY Dates;'

            cursor.execute(sql)

            results = cursor.fetchall()
            conn.commit()
            conn.close()
            return results

        def add():
        
            id=stidEntry.get()
            exam=examEntry.get()
            sub=subEntry.get()
            marks=marksEntry.get()
            max_marks=omEntry.get()
            dates=dateEntry.get()

            if (id == "" or id == " ") or (exam == "" or exam == " ") or (sub == "" or sub == " ") or (marks == "" or marks == " ") or (max_marks == "" or max_marks == " "):
                messagebox.showinfo("Error", "Please fill up the blank entry")
                return
            else:
                try:
                    conn = connection()
                    cursor = conn.cursor()

                    id=stidEntry.get()
                    exam=examEntry.get()
                    sub=subEntry.get()
                    marks=marksEntry.get()
                    max_marks=omEntry.get()
                    dates=dateEntry.get()

                    sql = "INSERT INTO results(id_number,exams, \
                            subjects,max_marks,obtained_marks, Dates) \
                            VALUES ('%s', '%s', '%s', '%s','%s','%s')" % \
                            (id,exam, sub,max_marks,marks, dates)

                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
                except:
                    messagebox.showinfo("Error", "Stud ID already exist")
                    return

            refreshTable()
            

        def select():
            try:
                selected_item = my_tree.selection()[0]
                studid = str(my_tree.item(selected_item)['values'][0])
                fname = str(my_tree.item(selected_item)['values'][1])
                lname = str(my_tree.item(selected_item)['values'][2])
                address = str(my_tree.item(selected_item)['values'][3])
                phone = str(my_tree.item(selected_item)['values'][4])
                om = str(my_tree.item(selected_item)['values'][5])
                date = str(my_tree.item(selected_item)['values'][6])
                setph(studid,1)
                setph(fname,2)
                setph(lname,3)
                setph(address,4)
                setph(phone,5)
                setph(om,6)
                setph(date,7)
            except:
                messagebox.showinfo("Error", "Please select a data row")

        def delete():
            decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
            if decision != "yes":
                return 
            else:
                selected_item = my_tree.selection()[0]
                deleteData = str(my_tree.item(selected_item)['values'][0])
                try:
                    conn = connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM results WHERE Id='"+str(deleteData)+"'")
                    conn.commit()
                    conn.close()
                except:
                    messagebox.showinfo("Error", "Sorry an error occured")
                    return

                refreshTable()

        def update():
            
            try:
                selected_item = my_tree.selection()[0]
                selectedStudid = str(my_tree.item(selected_item)['values'][0])
            except:
                messagebox.showinfo("Error", "Please select a data row")

            resId=resultidEntry.get()
            id=stidEntry.get()
            exam=examEntry.get()
            sub=subEntry.get()
            max_marks=marksEntry.get()
            marks=omEntry.get()
            dates=dateEntry.get()

            if (id == "" or id == " ") or (exam == "" or exam == " ") or (sub == "" or sub == " ") or (marks == "" or marks == " ") or (max_marks == "" or max_marks == " "):
                messagebox.showinfo("Error", "Please fill up the blank entry")
                return

            else:
                try:
                    conn = connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE results SET id_number='"+id+"', exams='"+
                    exam+"', subjects='"+
                    sub+"', max_marks='"+
                    max_marks+"', obtained_marks='"+
                    marks+"', Dates='"+
                    dates+"' WHERE Id='"+
                    resId+"' ")
                    conn.commit()
                    conn.close()
                except:
                    messagebox.showinfo("Error", "Stud ID already exist")
                    return

            refreshTable()
        #=====GUI===================
        result_root.configure(bg='#146C94')
        label = Label(result_root, text="Student Results",bg = "#146C94", font=('Arial Bold', 20))
        label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=10)

        studidLabel = Label(result_root, text="Result_ID:",bg = "#146C94", font=('Arial', 15))
        fnameLabel = Label(result_root, text="ID_Number:",bg = "#146C94", font=('Arial', 15))
        lnameLabel = Label(result_root, text="Exam:",bg = "#146C94", font=('Arial', 15))
        addressLabel = Label(result_root, text="Subject:",bg = "#146C94", font=('Arial', 15))
        phoneLabel = Label(result_root, text="Max Marks",bg = "#146C94", font=('Arial', 15))
        obtain_marks = Label(result_root, text="Obtained Marks",bg = "#146C94", font=('Arial', 15))
        date = Label(result_root, text="Date",bg = "#146C94", font=('Arial', 15))
        #=====ROW3==2
        studidLabel.grid(row=3, column=0, columnspan=1, padx=15, pady=5)
        fnameLabel.grid(row=4, column=0, columnspan=1, padx=15, pady=5)
        lnameLabel.grid(row=5, column=0, columnspan=1, padx=15, pady=5)
        addressLabel.grid(row=6, column=0, columnspan=1, padx=15, pady=5)
        phoneLabel.grid(row=7, column=0, columnspan=1, padx=15, pady=5)
        obtain_marks.grid(row=8, column=0, columnspan=1, padx=15, pady=5)
        date.grid(row=9, column=0, columnspan=1, padx=15, pady=5)

        resultidEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph1)
        stidEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph2)
        examEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph3)
        subEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph4)
        phoneEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph5)
        marksEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph5)
        omEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph6)
        dateEntry = Entry(result_root, width=35, bd=5, font=('Arial', 15), textvariable = ph7)

        resultidEntry.grid(row=3, column=1, columnspan=2, padx=5, pady=0)
        stidEntry.grid(row=4, column=1, columnspan=2, padx=5, pady=0)
        examEntry.grid(row=5, column=1, columnspan=2, padx=5, pady=0)
        subEntry.grid(row=6, column=1, columnspan=2, padx=5, pady=0)
        marksEntry.grid(row=7, column=1, columnspan=2, padx=5, pady=0)
        omEntry.grid(row=8, column=1, columnspan=2, padx=5, pady=0)
        dateEntry.grid(row=9, column=1, columnspan=2, padx=5, pady=0)

        addBtn = Button(
            result_root, text="Add", padx=65, pady=10, width=10,
            bd=5, font=('Arial', 15), bg="#84F894", command=add)
        updateBtn = Button(
            result_root, text="Update", padx=65, pady=10, width=10,
            bd=5, font=('Arial', 15), bg="#84E8F8", command=update)
        deleteBtn = Button(
            result_root, text="Delete", padx=65, pady=10, width=10,
            bd=5, font=('Arial', 15), bg="#FF9999", command=delete)
        selectBtn = Button(
            result_root, text="Select", padx=65, pady=10, width=10,
            bd=5, font=('Arial', 15), bg="#EEEEEE", command=select)

        addBtn.grid(row=3, column=4, columnspan=1, rowspan=2)
        updateBtn.grid(row=5, column=4, columnspan=1, rowspan=2)
        deleteBtn.grid(row=7, column=4, columnspan=1, rowspan=2)
        selectBtn.grid(row=9, column=4, columnspan=1, rowspan=1)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial Bold', 14))

        my_tree['columns'] = ("Result_ID","ID_Number","Exam","Subject","Marks","Obtained Marks","Date")

        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Result_ID", anchor=W, width=150)
        my_tree.column("ID_Number", anchor=W, width=150)
        my_tree.column("Exam", anchor=W, width=150)
        my_tree.column("Subject", anchor=W, width=165)
        my_tree.column("Marks", anchor=W, width=120)
        my_tree.column("Obtained Marks", anchor=W, width=170)
        my_tree.column("Date", anchor=W, width=150)

        my_tree.heading("Result_ID", text="Result_ID", anchor=W)
        my_tree.heading("ID_Number", text="ID_Number", anchor=W)
        my_tree.heading("Exam", text="Exam", anchor=W)
        my_tree.heading("Subject", text="Subject", anchor=W)
        my_tree.heading("Marks", text="Marks", anchor=W)
        my_tree.heading("Obtained Marks", text="Obtained Marks", anchor=W)
        my_tree.heading("Date", text="Date", anchor=W)

        refreshTable()
        ex=Button(result_root,text="Export",padx=65, pady=5, width=10,
            bd=1, font=('Arial', 12), bg="#D2001A",command=insert_into_excel).grid(row=25, column=2, columnspan=2)
        result_root.mainloop()





#===========Main ---- Filter Page=================================================

    dashboard.title("FILTER AND VISUALIZE DATA")
    dashboard.minsize(500, 450)
    dashboard.maxsize(500, 450)
    
    dashboard.configure(bg='skyblue')
 
    heading=Label(dashboard,text='FILTER AND VISUALIZE DATA',bg = "skyblue",font=('calibri 18  bold underline'))
    heading.place(x=100,y=20)

    global e_list
    exam_label=Label(dashboard,text='Enter the Exam',bg = "skyblue",font=('calibri 12'))
    exam_label.place(x=50,y=65)
    subject_list=['mid1','mid2','external exam']
    exam_name = StringVar(dashboard)
    exam_name.set("Select an Exam")
    exam_menu = OptionMenu(dashboard, exam_name, *e_list)
    exam_menu.config(bg="#FEFBE9", fg="black")
    exam_menu["menu"].config(bg="#D8D9CF")
    exam_menu.place(x=50,y=90,width=400,height=45)

    global s_list
    subject_label=Label(dashboard,text='Enter the Exam',bg = "skyblue",font=('calibri 12'))
    subject_label.place(x=50,y=135)
    subject_list = ["all","ee", "ec", "cp", "ce"]
    sub_name = StringVar(dashboard)
    sub_name.set("Select an Subject")
    question_menu = OptionMenu(dashboard, sub_name, *s_list)
    question_menu.config(bg="#FEFBE9", fg="black")
    question_menu["menu"].config(bg="#D8D9CF")
    question_menu.place(x=50,y=160,width = 400,height=45)

    id_number_label=Label(dashboard,text='Enter the Id Number',bg = "skyblue",font=('calibri 12'))
    id_number_label.place(x=45,y=215)
    id_number=Entry(dashboard,font=('Courier 20'),borderwidth=1, relief="solid", width = 25)
    id_number.place(x=46,y=240)


    Analytics= Button(dashboard, text="FILTERING",borderwidth=15, bg="#5D9C59",bd=3, padx=10, pady=8, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", width = 47, command=lambda:result_table())
    Analytics.place(x=45,y=300)

    Visualization= Button(dashboard, text="VISUALIZATION", bg="#F7C04A",bd=3, padx=10, pady=8, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", width =47, command=lambda:visualization())
    Visualization.place(x=45,y=360)

    # Exp_pdf= Button(dashboard, text="Export as PDF", bg="#DF2E38",bd=0, padx=10, pady=8, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", width =50, command=pdf_convertor)
    # Exp_pdf.place(x=37,y=420)

    def print_answers():
        print("Selected Option: {}".format(sub_name.get()))
        
        return None
    dashboard.mainloop()

def display_image(img_path):
    # Load the selected image using PIL
    img =Image.open(img_path)

    # Create a new window to display the full-size image
    top = tk.Toplevel()
    top.title("Image")

    # Convert the image to a Tkinter PhotoImage
    img_tk = ImageTk.PhotoImage(img)

    # Create a label to display the full-size image
    label = tk.Label(top, image=img_tk)
    label.pack(padx=5, pady=5)

    # Keep a reference to the PhotoImage to prevent it from being garbage collected
    label.image = img_tk

#================================================Screen ONE======================================================#
                        #===========================================================#


#======= 1. fetch the exam name and store in list =>USE: Its use in option menu
e_list=[]
s_list=[]
def fetch_exam_list():
    db=pymysql.connect(host='localhost',
                                    user='root',
                                    password='Mysql12345',
                                    database='result',
                                    cursorclass=pymysql.cursors.DictCursor)
    cur=db.cursor()
    sql = "select Exam_name from exam"
    try:
        cur.execute(sql)
        results = cur.fetchall()
        global e_list
        e_list=[]
        for row in results:
            for val in row.values():        
                   e_list.append(val)

        print(e_list)
    except:
        print ("Error: unable to fetch data")    
    db.close()

#======= 2. fetch the subject name and store in list =>USE: Its use in option menu
def fetch_sbject_list():
    db=pymysql.connect(host='localhost',
                                    user='root',
                                    password='Mysql12345',
                                    database='result',
                                    cursorclass=pymysql.cursors.DictCursor)
    cur=db.cursor()
    sql = "select sub_name from subjects"
    try:
        cur.execute(sql)
        results = cur.fetchall()
        global s_list
        s_list=[]
        for row in results:
            for val in row.values():        
                   s_list.append(val)

        print(s_list)
    except:
        print ("Error: unable to fetch data")    
    db.close()

#=====Calling above two function
fetch_exam_list()
fetch_sbject_list()
  
#======= 3. recognized text from img =>CALL: its call inside open_file()
def recognized_text(img_path):
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



#======= 4. Open File IMG  =>CALL: its call inside upload Button
def open_file():
   
   global img_path
   filetypes = (
        ('text files', '*.png'
                       ''),
        ('All files', '*.*')
    )

   img_path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
   print(img_path)
   print("path type:=====> ",img_path)
   display_image(img_path)
   call_img(img_path)
   recognized_text(img_path)


#======== 5. Evaluating Marks=> CALL through evaluete Button
marks=0
max_marks=0
def evaluate_marks():
    Evaluation_ans.config(state="normal")
    Evaluation_ans.delete("1.0","end")
    global marks
    global max_marks
    marks=0
    max_marks=0
    your_ans=str(notepad.get("1.0","end-1c"))
    #list_ans=["1.?a","2.?a","3.?d","4.?a","5.?c"]
    for i in range(len(ans_list)):
        #sir=str(i+1)
        set_ans=ans_list[i]
        match=re.search(set_ans,your_ans)
        max_marks=max_marks+1    
        if match:
            marks=marks+1
            x = re.sub("[.?]", "", set_ans,0,re.IGNORECASE)
            print("Right: ",x)
            Evaluation_ans.insert(END,"Right: "+x+"\n")
        else:
            x = re.sub("[.?]", "", set_ans,0,re.IGNORECASE)
            print("Wrong: ",x)
            Evaluation_ans.insert(END,"Wrong: "+x+"\n")
    print("Max Marks: ",max_marks)       
    print("Obtained Marks: ",marks)
    
    Evaluation_ans.config(state="normal")
    Evaluation_ans.insert(END,"You Get Marks: "+str(marks))
    Evaluation_ans.config(state="disabled")


#========6. Set Ans Key========

ans_list=[]
def add_ans():
    ans_number=str(q_number.get())
    inc_num=int(ans_number)+1

    right_ans=str(ans_field.get())
    
    ans=ans_number+".?"+right_ans
    ans_list.append(ans)
    List_ans.insert(END,ans_number+")"+right_ans+"\n")
    #q_number.set(inc_num)
    q_number.delete(0,END)
    q_number.insert(0,inc_num)

def reset_ans():
    global ans_list
    List_ans.delete("1.0","end")
    ans_list=[]


#=====7. INSERT Data Into Database====
def saveRes():
        current_time = datetime.datetime.now()
        db=pymysql.connect(host='localhost',
                                user='root',
                                password='Mysql12345',
                                database='result',
                                cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()

        id=Id_Number.get()
        exam=m_exam_name.get()
        sub=m_sub_name.get()
        dates=date_t.get_date()
        global marks
        global max_marks
        if(id==''):
            messagebox.showinfo("Error", "Enter ID Number")
            return
        if(exam=='Select an Exam'):
            messagebox.showinfo("Error", "Select Exam")
            return
        if(sub=='Select an Subject'):
            messagebox.showinfo("Error", "Select Subject")
            return
        
        sql = "INSERT INTO results(id_number,exams, \
        subjects,max_marks,obtained_marks, Dates) \
        VALUES ('%s', '%s', '%s', '%s','%s','%s')" % \
        (id,exam, sub,max_marks,marks, dates)

        
        try:        
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        db.close()
        print("Add Result successfully")

#======= 8. Add Exam====
def add_exam():
    db=pymysql.connect(host='localhost',
                                user='root',
                                password='Mysql12345',
                                database='result',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor=db.cursor()
    exa=add_Exam.get()
    
    if(exa==''):
        messagebox.showinfo("Error", "Enter Question NumberS")
        return

    sql = "INSERT INTO exam(Exam_name) \
    VALUES ('%s')" % \
    (exa)
    print("Add Exam Successfully")
    try:        
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()

#=======9. Add Subject====
def add_subject():
    db=pymysql.connect(host='localhost',
                                user='root',
                                password='Mysql12345',
                                database='result',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor=db.cursor()

    sub=add_Sub.get()
    if(sub==''):
        messagebox.showinfo("Error", "Enter Subject Name")
        return
   
    sql = "INSERT INTO subjects(sub_name) \
    VALUES ('%s')" % \
    (sub)
    print("Add Subject Successfully")
    try:        
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()



def insert_attendence__into_excel():
    file = filedialog.asksaveasfile(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                defaultextension='.xlsx',
                                filetypes=[
                                    ("xlsx file",".xlsx"),
                                    ("PDF file", ".pdf"),
                                ])
    print("sdded attendence---")
    attendance_str="19P\n12P\n13P\n14A\n19P\n"
    attendance_str=str(notepad.get("1.0","end-1c"))
    attendance_str_in_list = re.split("\n", attendance_str)

    attendance_list=[]
    for at_str in attendance_str_in_list:
        tem_list=[]
        print("ID Number: ",at_str[:-1]," Att:",at_str[-1:])
        tem_list.append(at_str[:-1])
        tem_list.append(at_str[-1:])
        attendance_list.append(tem_list)
    print("LIST OF ATTENDENCE: ",attendance_list)
    import pandas as pd
    new_list =attendance_list
    df = pd.DataFrame(new_list,columns =['ID Number','A/P'])
    writer = pd.ExcelWriter(file.name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Result', index=False)
    writer.save()




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
                   display_image(Open_image_path)
                   recognized_text(Open_image_path)
    cam.release()

    cv2.destroyAllWindows()

    # Call Open Image window function





#<<<<<<<<<<<<<<<<<<<=======---------Main-GUI------------==========>>>>>>>>>>>

newWindow.geometry("200x200")
newWindow.title('MCQ Marks Evaluation')
width= newWindow.winfo_screenwidth()
height= newWindow.winfo_screenheight()
#setting tkinter window size
#window.geometry("%dx%d" % (width, height))
newWindow.minsize(1090, 650)
newWindow.maxsize(1090, 650)
newWindow.configure(bg='skyblue')
#newWindow.option_add( "*font", "Arial 16 bold italic underline" )
my_label = Label(newWindow,text = "MCQ Test Checker",bg = "skyblue",font=('Arial 20 bold underline'))
my_label.pack(pady= 20)
#=========Nav_Bar=========
Upload_ans_sheet= Button(newWindow, text="Upload Image", bg="#2c2c2c",bd=0, padx=50, pady=8, font=("calibri", 14),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white",  command=lambda: open_file())
Live_image_detect= Button(newWindow, text="Live Detect", bg="#2c2c2c",bd=0, padx=55, pady=8, font=("calibri", 14),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white",command=Live_detect_image)
Set_ans= Button(newWindow, text="Set Answer", bg="#2c2c2c",bd=0, padx=107, pady=8, font=("calibri", 14),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white")
Marks_Evalate = Button(newWindow, text="Evaluate", bg="#2c2c2c",bd=0, padx=108, pady=8, font=("calibri", 14),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", command=lambda: evaluate_marks())
Upload_ans_sheet.place(x=20, y=70)
Live_image_detect.place(x=240, y=70)
Set_ans.place(x=450, y=70)
Marks_Evalate.place(x=765, y=70)

#======Recognized Text Field======
notepad=Text(newWindow,font=('Courier 18'),borderwidth=1, relief="solid")
notepad.place(x=20, y=130,height=415, width=420)

#======Set Answer Key Form======
Sir_Num = Label(newWindow,text = "Q.No",bg = "skyblue",font=('Courier 12')).place(x = 450,y = 125) 
q_number=Entry(newWindow,font=('Courier 16'),borderwidth=1, relief="solid")
q_number.place(x=450, y=150, width=35)

Ans_Num = Label(newWindow,text = "Enter Right Option",bg = "skyblue",font=('Courier 12')).place(x = 495,y = 125) 
ans_field=Entry(newWindow,font=('Courier 16'),borderwidth=1, relief="solid")
ans_field.place(x=490, y=150,width=200)

Add_button = Button(newWindow, text="ADD", bg="#2E4F4F",bd=0, padx=10, pady=0, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", command=lambda: add_ans())
Add_button.place(x=700, y=150)

#======Seted Answer Field======
List_ans=Text(newWindow,font=('Courier 18'),borderwidth=1, relief="solid")
List_ans.place(x=450, y=190,height=355, width=310)

#======Reset Answer Icon======
p1 = PhotoImage(file = 'refresh.png')
Text_Speech = Button(newWindow, text="Text Speech",image = p1, bg="#ffffff",bd=0, command=lambda:reset_ans())
Text_Speech.place(x=730, y=200)


#======Evaluated Text Field ======
Evaluation_ans=Text(newWindow,font=('Courier 18'),borderwidth=1, relief="solid")
Evaluation_ans.place(x=765, y=130,height=310, width=300)

#=====Add Record Into Database Form=====


user_name = Label(newWindow,text = "Id Number",font=('Courier 16'),bg = "skyblue").place(x = 765,y = 450) 
Id_Number=Entry(newWindow,font=('Courier 16'),borderwidth=1, relief="solid")
Id_Number.place(x=765, y=480,width=140)



date_name = Label(newWindow,text = "Date",font=('Courier 16'),bg = "skyblue").place(x = 920,y = 450) 
date_t= DateEntry(newWindow, width= 20,font=('Courier 13'),background= "magenta3", foreground= "white",bd=2)
date_t.place(x=920, y=480,width=140)


# exam_list=['mid1','mid2','external exam']
m_exam_name = StringVar(newWindow)
m_exam_name.set("Select an Exam")
exam_menu = OptionMenu(newWindow, m_exam_name, *e_list)
exam_menu.place(x=765, y=530,width=140)

#subject_list = ["all","ee", "ec", "cp", "ce"]
m_sub_name = StringVar(newWindow)
m_sub_name.set("Select an Subject")
question_menu = OptionMenu(newWindow, m_sub_name, *s_list)
question_menu.place(x=920, y=530, width=140)

Add_button = Button(newWindow, text="ADD THE MARKS", bg="#DF2E38",bd=0, padx=10, pady=3, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", command=lambda: saveRes())
Add_button.place(x=770, y=570)

show_result_button = Button(newWindow, text="SHOW THE RESULT", bg="#539165",bd=0, padx=5, pady=3, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", command=lambda: data_ana_visua())
show_result_button.place(x=920, y=570)

#==========Add Subject And Exam Entry Field ======
ex_name = Label(newWindow,font=('Courier 12'), bg = "skyblue",text = "Enter Exam").place(x = 135,y = 550)
add_Exam= Entry(newWindow,font=('Courier 18'),borderwidth=1, relief="solid")
add_Exam.place(x=135, y=570,width=245)
AddExam_button = Button(newWindow, text="ADD", bg="#2E4F4F",bd=0, padx=10, pady=3, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", command=lambda: add_exam())
AddExam_button.place(x=385, y=570)

sub_name = Label(newWindow,font=('Courier 12'),text = "Enter Subject", bg = "skyblue").place(x = 450,y = 550)
add_Sub= Entry(newWindow,font=('Courier 18'),borderwidth=1, relief="solid")
add_Sub.place(x=450, y=570,width=245)
AddSub_button = Button(newWindow, text="A DD", bg="#2E4F4F",bd=0, padx=12, pady=3, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", command=lambda: add_subject())
AddSub_button.place(x=700, y=570)

#==========Showing Result =======
Attendance_Sheet_Button = Button(newWindow, text="Attendance", bg="#FF6D60",bd=0, padx=15, pady=3, font=("calibri", 12),fg="white", cursor="hand2", activebackground='#2c2c2c',activeforeground="white", command=insert_attendence__into_excel)
Attendance_Sheet_Button.place(x=15, y=570)

newWindow.mainloop()