from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import pymysql as sql
import re
from time import strftime

top=Tk()
top.title("Registration Form")
top.geometry('1200x700')
top.resizable(False,False)
top.config(bg='white')

def insert():
    k1 = Name.get()
    k2 = Lastname.get()
    k3 = Email.get()
    k4 = Contact.get()
    k5 = Password.get()
    if (not k1 or k1 == "Name" or not k2 or k2 == "Lastname" or not k3 or k3 == "Email" or not k4 or k4 == "Contact" or not k5 or k5 == "Password"):
        messagebox.showerror("Error", "All fields are required. Please fill in all the details.")
        return
    if len(k5) < 8:
        messagebox.showerror("Invalid Password", "Password must be at least 8 characters long.")
        return
    elif not re.search(r"[A-Z]", k5):
        messagebox.showerror("Invalid Password", "Password must contain at least one uppercase letter.")
        return
    elif not re.search(r"\d", k5):
        messagebox.showerror("Invalid Password", "Password must contain at least one digit.")
        return
    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", k5):
        messagebox.showerror("Invalid Password", "Password must contain at least one special character.")
        return
    db=sql.connect(host='localhost',user='root',password='7011',db='billing')
    cur=db.cursor()
    s = "INSERT INTO record (Name, Lastname, Email, Contact, Password) VALUES (%s,%s,%s,%s,%s)"
    values = (k1, k2, k3, k4, k5)
    result = cur.execute(s,values)
    if result > 0:
        messagebox.showinfo("Complete", "Your sign-up is complete.")
    else:
        messagebox.showerror("Failed", "Sign-up failed.")
    db.commit()
    

def check():
    k1 = Name.get()
    k2 = Lastname.get()
    k3 = Email.get()
    k4 = int(Contact.get())
    k5 = Password.get()
    db = sql.connect(host='localhost', user='root', password='7011', db='billing')
    cur = db.cursor()
    s= "SELECT * FROM record WHERE Name=%s AND Lastname=%s AND Email=%s AND Contact=%s AND Password=%s"

    value =(k1,k2,k3,k4,k5)
    v=cur.execute(s,value)
    result = cur.fetchall()
    if v > 0:
        for col in result:
            id=col[0]
            messagebox.showinfo("Your ID", f"Your ID is: {id}")
    else:
        messagebox.showerror("Result","No record found")

def Back2():
    top.destroy()
    import Login

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    date_label.after(1000, update_time)

path=r"Assest\login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=0,bg="white").place(x=150, y=200)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 20), fg="black", bg="white")
date_label.place(x=50,y=20)
time_label = Label(top,font=("Bookman Old Style", 20), fg="black", bg="white")
time_label.place(x=50,y=50)

frame =Frame(top,width=450,height=600,bg="white")
frame.place(x=700, y=40)

Heading = Label(frame, text='Sign UP', bg='White', fg='Black', font=('Bookman Old Style', 40, 'bold'))
Heading.place(x=130, y=50)

def on_click(e):
    Name.delete(0,"end")
    Name.config(validate="key",validatecommand=Customername)

def on_focus_out(e):
    name = Name.get()
    if name == "":
        Name.config(validate="none")
        Name.insert(0,"Name")

def validate_name_input(char, value):
    if value == "":
        return True
    if char.isalpha():
        return True
    return False
Customername = (top.register(validate_name_input), "%S", "%P")

Name=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Name.place(x=50,y=150)
Name.insert(0,"Name")
Name.bind("<FocusIn>", on_click)
Name.bind("<FocusOut>", on_focus_out)
frame2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=182)

def on_click(e):
    Lastname.delete(0,"end")
    Lastname.config(validate="key",validatecommand=Customername)

def on_focus_out(e):
    lastname = Lastname.get()
    if lastname == "":
        Lastname.config(validate="none")
        Lastname.insert(0,"Lastname")

Lastname=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Lastname.place(x=50,y=200)
Lastname.insert(0,"Lastname")
Lastname.bind("<FocusIn>", on_click)
Lastname.bind("<FocusOut>", on_focus_out)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=232)

def on_click(e):
    Email.delete(0,"end")

def on_focus_out(e):
    email = Email.get()
    if email == "":
        Email.insert(0,"Email")

Email=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Email.place(x=50,y=250)
Email.insert(0,"Email")
Email.bind("<FocusIn>", on_click)
Email.bind("<FocusOut>", on_focus_out)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=282)

def on_click(e):
    Contact.delete(0,"end")
    Contact.config(validate="key", validatecommand=phone)

def on_focus_out(e):
    contact = Contact.get()
    if contact == "":
        Contact.config(validate="none")
        Contact.insert(0,"Contact")

def validate_digit_input(P):
    return P.isdigit() or P == ""

phone = (top.register(validate_digit_input), '%P')

Contact=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Contact.place(x=50,y=300)
Contact.insert(0,"Contact")
Contact.bind("<FocusIn>", on_click)
Contact.bind("<FocusOut>", on_focus_out)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=332)

def on_click(e):
    Password.delete(0,"end")

def on_focus_out(e):
    name = Password.get()
    if name == "":
        Password.insert(0,"Password")

Password=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20),show="*")
Password.place(x=50,y=350)
Password.insert(0,"Password")
Password.bind("<FocusIn>", on_click)
Password.bind("<FocusOut>", on_focus_out)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=382)

b1=Button(frame,cursor="hand2", width=10, pady=7, text='click here', bg='white',fg='blue', border=0, font=('Arial', 10, "bold"),command=check).place(x=220, y=516)
b2=Label(frame, height=2, text="Check your ID ?", bg='White', fg='Black', font=('Arial', 10, "bold")).place(x=120,y=515)
b3=Button(frame,cursor="hand2", width=20, pady=7, text='Submit', bg='#57a1f8',fg='Black', border=0, font=('Arial', 20, "bold"), command=insert).place(x=50, y=450)
b4=Button(frame,cursor="hand2", width=5, pady=7, text='←', bg="White",fg='Black', border=0, font=('Arial', 15, "bold"), command=Back2).place(x=5, y=2)

update_time()
top.mainloop()
