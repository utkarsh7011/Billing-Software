from tkinter import *
import pymysql as sql
from PIL import Image,ImageTk
from tkinter import messagebox
from time import strftime
from tkinter import Tk, ttk

top=Tk()
top.title("Find Your Basket")
top.state("zoomed") 
top.resizable(False,False)
top.config(bg='White')


def search():
    for i in tv.get_children():
        tv.delete(i)
    k1 = LEBillid.get()
    k3 = LEName.get()
    k4 = LEContact.get()
    if (not k1 or not k3 or not k4 ):
        messagebox.showerror("Error", "All fields are required. Please fill in all the details.")
        return
    db = sql.connect(host='localhost', user='root', password='7011', db='billing')
    cur = db.cursor()
    s= "SELECT * FROM customer WHERE bill_no = %s AND Name = %s AND Contact = %s;"
    value =(k1,k3,k4)
    v=cur.execute(s,value)
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
    else:
        messagebox.showerror("Result","No customer found")

def back1():
    top.destroy()
    import Main

def Checkdb():
    top.destroy()
    import Database

def update_time():
    time_label.config(text=f"{strftime('%H:%M %p')}")
    date_label.after(1000, update_time)

path=r"Assest\login.png"
img = ImageTk.PhotoImage(Image.open(path))
l0 =Label(top,image=img,border=0,bg="white").place(x=900, y=150)

frame =Frame(top,width=850,height=520,bg="white")
frame.place(x=50, y=0)

Heading = Label(frame, text='Your Basket', bg='White', fg='Black', font=('Bookman Old Style', 30, 'bold'))
Heading.place(x=300, y=50)

date_label = Label(top, text= f"{strftime('%d/%m/%y')}" ,font=("Bookman Old Style", 20), fg="black", bg="white")
date_label.place(x=1350,y=20)
time_label = Label(top,font=("Bookman Old Style", 20), fg="black", bg="white")
time_label.place(x=1350,y=50)

Billid=Label(frame, text= "Bill No.", fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
Billid.place(x=100,y=150)

LCname=Label(frame, text= "Name",fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
LCname.place(x=100,y=250)

LCContact=Label(frame, text= "Contact",fg='Black', border=0, bg='white', font=('Bookman Old Style', 20))
LCContact.place(x=100,y=350)


def validate_digit_input(P):
    return P.isdigit() or P == ""

billidentity = (top.register(validate_digit_input), '%P')
LEBillid=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20),validate="key",validatecommand=billidentity)
LEBillid.place(x=250,y=150)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=250, y=182)

def validate_name_input(char, value):
    if value == "":
        return True
    if char.isalpha():
        return True
    return False
Customername = (top.register(validate_name_input), "%S", "%P")
LEName=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20),validate="key",validatecommand=Customername)
LEName.place(x=250,y=250)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=250, y=282)

phone = (top.register(validate_digit_input), '%P')

LEContact=Entry(frame, width=20,fg='Black', border=0, bg='white', font=('Bookman Old Style', 20),validate="key",validatecommand=phone)
LEContact.place(x=250,y=350)
frame3 =Frame(frame,width=342,height=2,bg="black").place(x=250, y=382)

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
tv.place(x=30, y=530, height=300)

style = ttk.Style()
style.configure("Treeview", font=("Bookman Old Style", 10))
style.configure("Treeview.Heading", font=("Bookman Old Style", 12))

b1=Button(frame,cursor="hand2", width=20, pady=7, text='Submit', bg='#57a1f8',fg='Black', border=0, font=('Arial', 20, "bold"), command=search).place(x=250, y=450)
b2=Button(frame,cursor="hand2", width=5, pady=7, text='←', bg="White",fg='Black', border=0, font=('Arial', 15, "bold"), command=back1).place(x=5, y=2)
b1=Button(top,cursor="hand2", pady=7, text='Database', bg='Red',fg='Black', border=0, font=('Arial', 15, "bold"), command=Checkdb).place(x=1410, y=478)

update_time()
top.mainloop()
