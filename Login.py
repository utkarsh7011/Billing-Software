from tkinter import *
import pymysql as sql
from PIL import Image,ImageTk
from tkinter import messagebox
from time import strftime

top=Tk()
top.title("Login")
top.geometry('1200x700')
top.resizable(False,False)
top.config(bg='White')

def login():
    k1 = Email.get()
    k2 = Password.get()
    if (not k1 or k1 == "Name" or not k2 or k2 == "Password"):
        messagebox.showerror("Error", "All fields are required. Please fill in all the details.")
        return
    db=sql.connect(host='localhost',user='root',password='7011',db='billing')
    cur=db.cursor()
    s = "SELECT * FROM record WHERE email =%s AND password =%s"
    cur.execute(s, (k1, k2))
    result = cur.fetchone()
    if result:
        s= "SELECT * FROM record WHERE Email=%s"
        v=cur.execute(s,k1)
        result = cur.fetchall()
        if v > 0:
            for col in result:
                Name=col[1]
        messagebox.showinfo("Welcome", f"Your Welcome {Name}")
        top.destroy()
        import Main
    else:
        messagebox.showerror("Result", "Incorrect Access")
    db.close()

def register():
    top.destroy()
    import Registration

def forget():
    top.destroy()
    import forget

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    top.after(1000, update_time)

path=r"Assest\login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=0,bg="white").place(x=150, y=200)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 20), fg="black", bg="white")
date_label.place(x=50,y=20)
time_label = Label(top,font=("Bookman Old Style", 20), fg="black", bg="white")
time_label.place(x=50,y=50)

frame =Frame(top,width=450,height=600,bg="white")
frame.place(x=700, y=40)

Heading = Label(frame, text='Sign In', bg='White', fg='Black', font=('Bookman Old Style', 40, 'bold'))
Heading.place(x=130, y=50)

def on_click(e):
    Email.delete(0,"end")

def on_focus_out(e):
    name = Email.get()
    if name == "":
        Email.insert(0,"E-mail")

Email=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Email.place(x=50,y=200)
Email.insert(0,"E-mail")
Email.bind("<FocusIn>", on_click)
Email.bind("<FocusOut>", on_focus_out)
frame2 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=232)

def on_click(e):
    Password.delete(0,"end")

def on_focus_out(e):
    name = Password.get()
    if name == "":
        Password.insert(0,"Password")

Password=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20),show="*")
Password.place(x=50,y=300)
Password.insert(0,"Password")
Password.bind("<FocusIn>", on_click)
Password.bind("<FocusOut>", on_focus_out)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=50, y=332)

b1=Button(frame, cursor="hand2", width=20, pady=7, text='Forget Password', bg='white',fg='Black', border=0, font=('Arial', 10, "bold"), command=forget).place(x=50, y=350)
b2=Button(frame,cursor="hand2", width=20, pady=7, text='Sign In', bg='#57a1f8',fg='Black', border=0, font=('Arial', 20, "bold"), command=login).place(x=50, y=400)
b3=Button(frame,cursor="hand2", width=10, pady=7, text='Sign Up', bg='white',fg='blue', border=0, font=('Arial', 10, "bold"), command=register).place(x=240, y=476)
b4=Label(frame, height=2, text="Don't have an account ?", bg='White', fg='Black', font=('Arial', 10, "bold")).place(x=100,y=475)

update_time()
top.mainloop()
