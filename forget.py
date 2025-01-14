from tkinter import *
import pymysql as sql
from PIL import Image,ImageTk
from tkinter import messagebox
from time import strftime

top=Tk()
top.title("Forget Password")
top.geometry('1200x700')
top.resizable(False,False)
top.config(bg='White')

def search():
    k1 = id.get()
    k3 = Email.get()
    k4 = Contact.get()
    if (not k1 or k1 == "ID" or not k3 or k3 == "Email" or not k4 or k4 == "Contact"):
        messagebox.showerror("Error", "All fields are required. Please fill in all the details.")
        return
    db = sql.connect(host='localhost', user='root', password='7011', db='billing')
    cur = db.cursor()
    s= "SELECT * FROM record WHERE ID=%s AND Email=%s AND Contact=%s"
    value =(k1,k3,k4)
    v=cur.execute(s,value)
    result = cur.fetchall()
    if v > 0:
        for col in result:
            password=col[5]
            messagebox.showinfo("Password", f"Your Password is: {password}")
            top.destroy()
            import Login
    else:
        messagebox.showerror("Result","No record found")
        
def back1():
    top.destroy()
    import Login

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    date_label.after(1000, update_time)

path=r"Assest\login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=0,bg="white").place(x=150, y=250)

frame =Frame(top,width=450,height=600,bg="white")
frame.place(x=700, y=40)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 20), fg="black", bg="white")
date_label.place(x=50,y=20)
time_label = Label(top, font=("Bookman Old Style", 20), fg="black", bg="white")
time_label.place(x=50,y=50)

Heading = Label(frame, text='Find Your Account', bg='White', fg='Black', font=('Bookman Old Style', 30, 'bold'))
Heading.place(x=30, y=50)

def on_click(e):
    id.delete(0,"end")
    id.config(validate="key", validatecommand=customeridentity)

def on_focus_out(e):
    name = id.get()
    if name == "":
        id.config(validate="none")
        id.insert(0,"ID")

def validate_digit_input(P):
    return P.isdigit() or P == ""

customeridentity = (top.register(validate_digit_input), '%P')

id=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
id.place(x=50,y=150)
id.insert(0,"ID")
id.bind("<FocusIn>", on_click)
id.bind("<FocusOut>", on_focus_out)
frame2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=182)

def on_click(e):
    Email.delete(0,"end")

def on_focus_out(e):
    name = Email.get()
    if name == "":
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
    name = Contact.get()
    if name == "":
        Contact.config(validate="none")
        Contact.insert(0,"Contact")

phone = (top.register(validate_digit_input), '%P')

Contact=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Contact.place(x=50,y=350)
Contact.insert(0,"Contact")
Contact.bind("<FocusIn>", on_click)
Contact.bind("<FocusOut>", on_focus_out)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=382)

b1=Button(frame,cursor="hand2", width=20, pady=7, text='Submit', bg='#57a1f8',fg='Black', border=0, font=('Arial', 20, "bold"), command=search).place(x=50, y=450)
b2=Button(frame,cursor="hand2", width=5, pady=7, text='←', bg="White",fg='Black', border=0, font=('Arial', 15, "bold"), command=back1).place(x=5, y=2)

update_time()
top.mainloop()
