from tkinter import *
from customtkinter import *
import cv2
import pyqrcode
from PIL import ImageTk,Image
import os
from tkinter import messagebox,filedialog
import webbrowser

mw=CTk()
mw.title('QRCode')
mw.geometry('1000x500')

set_appearance_mode('Dark')

cam=cv2.VideoCapture(0)

decoder=cv2.QRCodeDetector()

def buttons():
    btn1=CTkButton(mw,text='Open Camera',font=CTkFont('arial',30),command=open_camera)
    btn1.place(relx=0.25,rely=0.15,anchor='center')


    btn2=CTkButton(mw,text='Upload File',font=CTkFont('arial',30),command=upload_file)
    btn2.place(relx=0.5,rely=0.15,anchor='center')

    btn3=CTkButton(mw,text='Generate QR',font=CTkFont('arial',30),command=generate_qr)
    btn3.place(relx=0.75,rely=0.15,anchor='center')

def destroy_widgets():
    for widgets in mw.winfo_children():
        widgets.destroy()

def upload_file():
    destroy_widgets()
    buttons()

    qrlabel=CTkTextbox(mw,font=CTkFont('arial',30),width=600,height=200)
    qrlabel.place(relx=0.3,rely=0.5,anchor='center')

    label2=CTkLabel(mw,text='',font=CTkFont('arial',30))
    label2.place(relx=0.65,rely=0.5,anchor='center')

    f=filedialog.askopenfilename()
    img1=Image.open(f)
    img2=img1.resize((450,450))
    img=ImageTk.PhotoImage(img2)
    
    label2.configure(image=img)

    img=cv2.imread(f)
    detect=cv2.QRCodeDetector()
    data,var1,var2=detect.detectAndDecode(img)
    if data:
        qrlabel.insert(INSERT,data)
        qrlabel.configure(state='disabled')

    def open_web():
        webbrowser.open_new(data)
    if '.com' or '.in' or 'https://' in data:
        btn1=CTkButton(mw,text='Open Website',font=CTkFont('arial',30),command=open_web)
        btn1.place(relx=0.25,rely=0.75,anchor='center')

def open_camera():
    destroy_widgets()
    buttons()

    label=Label(mw,text='')
    label.place(relx=0.7,rely=0.5,anchor='center')

    qrlabel=CTkTextbox(mw,font=CTkFont('arial',30),width=600,height=200)
    qrlabel.place(relx=0.3,rely=0.5,anchor='center')
    try:
        def show_frame():
            v,frame=cam.read()
            data,array,x=decoder.detectAndDecode(frame)
            correctedimg=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            img=Image.fromarray(correctedimg)
            imagetk=ImageTk.PhotoImage(image=img)
            label.imagetk=imagetk
            label.configure(image=imagetk)
            def open_web():
                webbrowser.open_new(data)
            if data:
                qrlabel.insert(INSERT,data)
                qrlabel.configure(state='disabled')
                btn1=CTkButton(mw,text='Open Website',font=CTkFont('arial',30),command=open_web)
                btn1.place(relx=0.3,rely=0.7,anchor='center')
            label.after(10,show_frame)
        show_frame()
    except:
        messagebox.showerror('Cannot open webcam','Please try again')
    cv2.destroyAllWindows()

def generate_qr():  
    destroy_widgets()
    buttons()  

    inp_user=CTkEntry(mw,placeholder_text='Enter Your Text',font=CTkFont('arial',30),width=500)
    inp_user.place(relx=0.3,rely=0.25,anchor='center')

    def save_qr(var):
        messagebox.showinfo('QR Code Download','Select the directory to download')
        dir=filedialog.askdirectory()
        print(dir)
        qr_name=CTkEntry(mw,placeholder_text='Enter file name',font=CTkFont('arial',15),width=150)
        qr_name.place(relx=0.85,rely=0.35,anchor='center')
        os.chdir(dir)
        def save_dir():
            name=qr_name.get()
            url=pyqrcode.create(var)
            if name=='':
                ans=messagebox.askokcancel('File name','File name will be same as text entered')
                if ans==True:
                    name=var
                elif ans==False:
                    messagebox.showinfo('File name','Enter file name')  
            if name!='':
                img=name+'.png'           
                url.png(img,scale=10)
                messagebox.showinfo('QR Code Download','Your QR Code is saved in the given directory')
        save=CTkButton(mw,text='Save',font=CTkFont('arial',30),command=save_dir)
        save.place(relx=0.85,rely=0.45,anchor='center')

    def submit_function():
        var=inp_user.get()
        url=pyqrcode.create(var)
        img=var+'.png'
        url.png(img,scale=10)
        img1=Image.open(img)
        img2=img1.resize((450,450))
        img_qrcode=ImageTk.PhotoImage(img2)
        out_label=CTkLabel(mw,image=img_qrcode,text='')
        out_label.place(rely=0.6,relx=0.5,anchor='center')
        os.remove(img)
        save=CTkButton(mw,text='Download QR',font=CTkFont('arial',30),command=lambda :save_qr(var))
        save.place(relx=0.8,rely=0.25,anchor='center')

    submit=CTkButton(mw,text='Submit',font=CTkFont('arial',30),command=submit_function)
    submit.place(relx=0.6,rely=0.25,anchor='center')

buttons()
mw.mainloop()