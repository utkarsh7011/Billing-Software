from tkinter import *
import pymysql as sql
from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter import Tk, ttk
from time import strftime

top=Tk()
top.title("DataBase")
top.state("zoomed") 
top.resizable(False,False)
top.config(bg='White')

def Database():
    k1 = Email.get()
    k2 = Password.get()
    if (not k1 or not k2 ):
        messagebox.showerror("Error", "All fields are required. Please fill in all the details.")
        return
    db=sql.connect(host='localhost',user='root',password='7011',db='billing')
    cur=db.cursor()
    s = "select * from record WHERE email =%s AND password =%s"
    cur.execute(s, (k1, k2))
    result = cur.fetchone()
    if result:
        s= "select * from record WHERE Email=%s"
        v=cur.execute(s,k1)
        result = cur.fetchall()
        if v > 0:
            for col in result:
                Name=col[1]
        messagebox.showinfo("Welcome", f"Your Welcome {Name}")
        for i in tv.get_children():
            tv.delete(i)
        db = sql.connect(host='localhost', user='root', password='7011', db='billing')
        cur = db.cursor()
        s= "select * from customer;"
        v=cur.execute(s)
        result = cur.fetchall()
        if v > 0:
            for col in result:
                Billno = col[0]
                Name = col[1]
                Lastname = col[2]
                Emai = col[3]
                Contact=col[4]
                Grooming = col[5]
                Food = col[6]
                Essential = col[7]
                Amount = col[8]
                Gst = col[9]
                Discount = col[10]
                Grand_total = col[11]
                tv.insert("", "end", values=(Billno, Name, Lastname, Emai, Contact, Grooming, Food, Essential, Amount, Gst, Discount, Grand_total))
            top.focus_set()
    else:
        messagebox.showerror("Result","No customer found")
def back1():
    top.destroy()
    import Billsearch

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    date_label.after(1000, update_time)

path=r"Assest\login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=0,bg="white").place(x=900, y=100)

frame =Frame(top,width=850,height=420,bg="white")
frame.place(x=50, y=2)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 20), fg="black", bg="white")
date_label.place(x=1350,y=20)
time_label = Label(top,font=("Bookman Old Style", 20), fg="black", bg="white")
time_label.place(x=1350,y=50)

Heading = Label(frame, text='Check DataBase', bg='White', fg='Black', font=('Bookman Old Style', 30, 'bold'))
Heading.place(x=250, y=50)

LEmail = Label(frame, text='E-Mail', bg='White', fg='Black', font=('Bookman Old Style', 20, 'bold'))
LEmail.place(x=100, y=150)
LPassword = Label(frame, text='Password', bg='White', fg='Black', font=('Bookman Old Style', 20, 'bold'))
LPassword.place(x=60, y=220)

Email=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Email.place(x=250,y=150)
frame2 =Frame(frame,width=342,height=2,bg="black").place(x=250, y=182)

Password=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20),show="*")
Password.place(x=250,y=220)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=250, y=252)

tv = ttk.Treeview(top)
tv["column"] = ("Bill No.", "Name","Lastname", "Email", "Contact","Grooming","Food","Essential","Amount","GST","Discount","Grand Total")
tv.column("#0", width=0,stretch=0)
tv.column("Bill No.", anchor=CENTER,width=80)
tv.column("Name", anchor=CENTER, width=125)
tv.column("Lastname", anchor=CENTER, width=125)
tv.column("Email", anchor=CENTER,width=280)
tv.column("Contact", anchor=CENTER,width=130)
tv.column("Grooming", anchor=CENTER,width=110)
tv.column("Food", anchor=CENTER,width=100)
tv.column("Essential", anchor=CENTER,width=110)
tv.column("Amount", anchor=CENTER,width=100)
tv.column("GST", anchor=CENTER,width=100)
tv.column("Discount", anchor=CENTER,width=100)
tv.column("Grand Total", anchor=CENTER,width=120)

tv.heading("Bill No.", text="Bill No. ",anchor=CENTER)
tv.heading("Name", text="Name",anchor=CENTER)
tv.heading("Lastname", text="Lastname",anchor=CENTER)
tv.heading("Email", text="Email",anchor=CENTER)
tv.heading("Contact", text="Contact",anchor=CENTER)
tv.heading("Grooming",text="Grooming", anchor=CENTER)
tv.heading("Food",text="Food", anchor=CENTER)
tv.heading("Essential", text="Essential",anchor=CENTER)
tv.heading("Amount", text="Amount",anchor=CENTER)
tv.heading("GST", text="GST",anchor=CENTER)
tv.heading("Discount", text="Discount",anchor=CENTER)
tv.heading("Grand Total", text="Grand Total",anchor=CENTER)
tv.place(x=30, y=430, height=400)

style = ttk.Style()
style.configure("Treeview", font=("Bookman Old Style", 10))
style.configure("Treeview.Heading", font=("Bookman Old Style", 12))

b1=Button(frame,cursor="hand2", width=20, pady=7, text='Submit', bg='#57a1f8',fg='Black', border=0, font=('Arial', 20, "bold"), command=Database).place(x=250, y=320)
b2=Button(frame,cursor="hand2", width=5, pady=7, text='←', bg="White",fg='Black', border=0, font=('Arial', 15, "bold"), command=back1).place(x=5, y=5)

update_time()
top.mainloop()
