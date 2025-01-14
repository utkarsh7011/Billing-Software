from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Tk
import random
import pymysql as sql

top=Tk()
top.title("Billing Software")
top.state("zoomed") 
top.resizable(False, False)
top.config(bg="black")

tv1 = ttk.Treeview(top)
tv1["columns"] = ("Details")#,"Amount")
tv1.column("#0", width=0, stretch=0)
tv1.column("Details", anchor="w", width=300)
# tv1.column("Amount", anchor="w", width=300)
tv1.heading("Details", text="Bill Details", anchor="center")
# tv1.heading("Amount", text="Amount", anchor="center")
tv1.place(x=930, y=240, width=600, height=400)

def searchbill():
    top.destroy()
    import Billsearch

def add():
    global billno
    k1, k2, k3, k4 = CName.get(), CLastname.get(), CEmail.get(), CContact.get()
    
    if any(val in ["", "Name", "Lastname", "Email", "Contact"] for val in [k1, k2, k3, k4]):
        messagebox.showerror("Error", "All fields must be filled properly")
        return
    # Check if the totals are defined and assign values, default to 0 if not defined
    k5, k6, k7, k8, k9, k10, k11 = (
        globals().get('grooming_total', 0.0),
        globals().get('food_total', 0.0),
        globals().get('essential_total', 0.0),
        globals().get('all_total', 0.0),
        globals().get('total_gst', 0.0),
        globals().get('TDiscount', 0.0),
        globals().get('final', 0.0)
    )
    
    if k8 == 0.0:
        messagebox.showerror("Error", "Bill can't be 0.")
        return
    
    if k9 == 0.0:
        messagebox.showerror("Error", "GST can't be 0.")
        return
    
    if k11 == 0.0:
        messagebox.showerror("Error", "Grand Total can't be 0.")
        return

    k5, k6, k7, k8, k9, k10, k11 = [
        0.0 if x in ["Grooming", "Food", "Essential", "Amount", "GST", "Discount", "Grand Total"] else x 
        for x in [k5, k6, k7, k8, k9, k10, k11]
    ]
    discount_text = TDiscount.get().replace("%","").strip()
    if discount_text.isdigit():
        discount_text = float(discount_text)
    else:
        discount_text = 0.0

    db=sql.connect(host='localhost',user='root',password='7011',db='billing')
    cur=db.cursor()
    s = "INSERT INTO customer (Name, Lastname, Email, Contact, Grooming, Food, Essential, Amount, GST, Discount, Grand_total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    values = (k1,k2,k3,k4,k5,k6,k7,k8,k9,discount_text,k11)
    result = cur.execute(s, values)
    if result > 0:
        s= "SELECT * FROM customer WHERE Name=%s AND Lastname=%s AND Email=%s AND Contact=%s"
        value =(k1, k2, k3, k4)
        v=cur.execute(s,value)
        result = cur.fetchall()
        if v > 0:
            for col in result:
                billno=col[0]
                printbill()
        else:
            messagebox.showerror("Error","No record found")
    else:
        messagebox.showerror("Error", "Billing failed.")
    db.commit()

def printbill():
    for item in tv1.get_children():
        tv1.delete(item)
    global all_total, sgst, cgst, total_gst,TDiscount, final, billno
    g0, g1, g2, g3, g4 = billno, CName.get(), CLastname.get(), CEmail.get(), CContact.get()
    g5, g6, g7, g8 , g9 , g10 = (all_total, sgst, cgst,  total_gst, TDiscount, final)
    g5, g6, g7, g8 , g9 , g10 = [0.0 if x in ["Amount", "SGST", "CGST", "Total GST", "Discount", "Grand Total"] else x for x in [g5, g6, g7, g8, g9, g10]]

    items = [(PBodySoap, "Body Soap"), (PFacewash, "Face Wash"), (PFaceCream, "Face Cream"), (PHairOil, "Hair Oil"), (PShampoo, "Shampoo"), (PLotion, "Lotion"),(PRice, "Rice"), (PWheat, "Wheat"), (PSugar, "Sugar"), (PTea, "Tea"), (PCoffee, "Coffee"), (PFoodOil, "Food Oil"), (PColdDrink, "Cold Drink"),(PSnacks, "Snacks"), (PStationery, "Stationery"), (PLighting, "Lighting"), (PCleaning, "Cleaning"), (PTobacco, "Tobacco")]
    prices = {"Body Soap": {"Dove": 50, "Lifebuoy": 20, "Dettol": 35, "Medimix": 10, "Cinthol": 45, "Pears": 60},
        "Face Wash": {"Beardo": 450, "Mamaearth": 235, "Garnier": 139, "Clean & Clear": 150, "Himalaya": 200, "NIVEA": 199},
        "Face Cream": {"Ponds": 50, "Olay": 20, "L'Oréal Paris": 95, "Biotiqu": 150, "Lakmé": 650, "Cetaphil": 200},
        "Hair Oil": {"Parachute": 91, "Dabur Amla": 64, "Kesh King": 46, "Himalaya Herbals": 79, "Scalpe Plus": 95, "Indulekha Bringha": 56},
        "Shampoo": {"Tresemme": 290, "Schwarzkopf": 250, "Nizoral": 101, "Pantene": 35, "Kerastase": 65, "Head & Shoulders": 25},
        "Lotion": {"Vaseline": 100, "Eucerin": 150, "Aveeno": 173, "Johnson's Baby": 59, "Neutrogena": 109, "Bio Oil": 98},
        "Rice": {"Tilda": 59, "Daawat": 29, "India Gate": 43, "Kohinoor": 47, "Patanjali": 51, "Shree Lal Mahal": 54},
        "Wheat": {"Shakti Bhog": 310, "Aashirvaad": 390, "Pillsbury": 350, "Nature Fresh": 360, "Annapurna": 320, "Fortune Whole Wheat": 420},
        "Sugar": {"Tata": 52, "Dharmani": 59, "Shree Hari": 65, "Dharani": 50, "Rathna": 45, "Madhur": 55},
        "Tea": {"Tata Tea": 168, "Brooke Bond": 349, "Wagh Bakri": 280, "Tetley": 340, "Lipton": 540, "Taj Mahal": 650},
        "Coffee": {"Nescafé": 120, "Bru": 100, "Tata Coffee": 149, "Lavazza": 259, "Mountain Trail": 300, "Blue Tokai": 250},
        "Food Oil": {"Saffola": 499, "Tata Sampann": 520, "Dalda": 150, "Mahakosh": 650, "Patanjali": 440, "Fortune": 480},
        "Cold Drink": {"Frooti": 10, "Pepsi": 80, "Sprite": 50, "Mountain Dew": 40, "7UP": 20, "Red Bull": 125},
        "Snacks": {"Lay's": 10, "Pringles": 90, "Cheetos": 5, "Doritos": 20, "Haldiram": 15, "Bicano": 25},
        "Stationery": {"Pencils": 5, "Markers": 25, "Erasers": 4, "Rulers": 10, "Folders": 30, "Notebooks": 20},
        "Lighting": {"LED Bulbs": 150, "CFL Bulbs": 230, "Smart Bulbs": 440, "Table Lamps": 140, "Floor Lamps": 260, "Night Lights": 100},
        "Cleaning": {"Laundry Detergent": 135, "Air Freshener": 220, "Floor Cleaner": 80, "Vacuum Cleaner": 650, "Broom and Dustpan": 150, "Microfiber Cloths": 350},
        "Tobacco": {"Cigarettes": 120, "E-cigarettes (Vapes)": 200, "Rolling Papers": 5, "Nicotine Pouches": 85, "Chewing Tobacco": 20, "Hookah Tobacco": 180}
    }
    tv1.insert("", "end", values=(f"Bill No :- {g0}","",""))
    tv1.insert("", "end", values=(f"Name of Customer :- {g1} {g2}","",""))
    tv1.insert("", "end", values=(f"Email:- {g3}","",""))
    tv1.insert("", "end", values=(f"Contact:- {g4}","",""))

    tv1.insert("", "end", values=("----------------------------------------------------- Bill Details -----------------------------------------------------","",""))
    for item, default in items:
        value = item.get().strip()
    for item, default in items:
        value = item.get().strip()
        
        if value != default and value != "":
            price = prices.get(default, {}).get(value, 0)
            tv1.insert("", "end", values=(f"{value} :- {price}","",""))
    tv1.insert("", "end", values=(f"Amount :- {g5:.2f}","",""))
    tv1.insert("", "end", values=(f"SGST :- {g6:.2f}","",""))
    tv1.insert("", "end", values=(f"CGST :- {g7:.2f}","",""))
    tv1.insert("", "end", values=(f"Total GST :- {g8:.2f}","",""))
    
    
    discount_text = TDiscount.get().replace("%","").strip()
    if discount_text != "0" and discount_text != "Discount":
        tv1.insert("", "end", values=(f"Discount :- {discount_text}","",""))
    tv1.insert("", "end", values=(f"Grand Total :- {g10:.2f}","",""))
    tv1.insert("", "end", values=("----------------------------------------------------- End of Bill -----------------------------------------------------","",""))
    tv1.insert("", "end", values=("---------------------------------------------- Thank you for Shopping ---------------------------------------------","",""))
    messagebox.showinfo("Complete", "Billing is complete.")
    

def calculate_totals():
    global grooming_total, food_total, essential_total, all_total
    grooming_total = 0
    food_total = 0
    essential_total = 0
    all_total = 0
    grooming_total += on_bodysoap_select(PBodySoap.get())
    grooming_total += on_Facewash_select(PFacewash.get())
    grooming_total += on_FaceCream_select(PFaceCream.get())
    grooming_total += on_HairOil_select(PHairOil.get())
    grooming_total += on_Shampoo_select(PShampoo.get())
    grooming_total += on_Lotion_select(PLotion.get())
    if grooming_total == 0:
        pass
    else:
        CGrooming.config(state="normal",readonlybackground="#074463")
        CGrooming.delete(0, "end")
        CGrooming.insert(0, str(f"{grooming_total:.2f} "))
        CGrooming.config(state="readonly",readonlybackground="#074463")


    food_total += on_Rice_select(PRice.get())
    food_total += on_Wheat_select(PWheat.get())
    food_total += on_Sugar_select(PSugar.get())
    food_total += on_Tea_select(PTea.get())
    food_total += on_Coffee_select(PCoffee.get())
    food_total += on_FoodOil_select(PFoodOil.get())
    if food_total == 0:
        pass
    else:
        CFood.config(state="normal",readonlybackground="#074463")
        CFood.delete(0, "end")
        CFood.insert(0, str(f"{food_total:.2f} "))
        CFood.config(state="readonly",readonlybackground="#074463")


    essential_total += on_ColdDrink_select(PColdDrink.get())
    essential_total += on_Snacks_select(PSnacks.get())
    essential_total += on_Stationery_select(PStationery.get())
    essential_total += on_Lighting_select(PLighting.get())
    essential_total += on_Cleaning_select(PCleaning.get())
    essential_total += on_Tobacco_select(PTobacco.get())
    if essential_total == 0:
        pass
    else:
        CEssential.config(state="normal",readonlybackground="#074463")
        CEssential.delete(0, "end")
        CEssential.insert(0, str(f"{essential_total:.2f} "))
        CEssential.config(state="readonly",readonlybackground="#074463")

    all_total += grooming_total
    all_total += food_total
    all_total += essential_total
    if all_total == 0:
        messagebox.showerror("Error", "Select an item")
    else:
        Amount.config(state="normal",readonlybackground="#074463")
        Amount.delete(0, "end")
        Amount.insert(0, str(f"{all_total:.2f} "))
        Amount.config(state="readonly",readonlybackground="#074463")

def GST():
    global total_gst, sgst, cgst
    amount_text = Amount.get().replace("", "").strip()
    if amount_text == 0 or amount_text == "Amount":
        messagebox.showerror("Error", "Select an item")
    else:
        amount = float(Amount.get().replace("",""))
        cgst = amount * 0.09
        sgst = amount * 0.09
        total_gst = amount * 0.18
        Tgst.config(state="normal", readonlybackground="#074463")
        Tgst.delete(0, "end")
        Tgst.insert(0, f"{total_gst:.2f}")
        Tgst.config(state="readonly", readonlybackground="#074463")

        CCgst.config(state="normal", readonlybackground="#074463")
        CCgst.delete(0, "end")
        CCgst.insert(0, f"{cgst:.2f}")
        CCgst.config(state="readonly", readonlybackground="#074463")

        CSgst.config(state="normal", readonlybackground="#074463")
        CSgst.delete(0, "end")
        CSgst.insert(0, f"{sgst:.2f}")
        CSgst.config(state="readonly", readonlybackground="#074463")

    return total_gst
    
def Discount():
    global discount
    amount_text = Amount.get().replace("", "").strip()
    if amount_text == 0 or amount_text == "Amount":
        messagebox.showerror("Error", "Select an item")
    else:
        a = (5,10,15,20)
        discount = random.choice(a)
        messagebox.showinfo("Lucky", f"You won {discount}% discount")
        TDiscount.config(state="normal",readonlybackground="#074463")
        TDiscount.delete(0, "end")
        TDiscount.insert(0, str(f"{discount}% "))
        TDiscount.config(state="readonly",readonlybackground="#074463")

def Final():
    global final
    amount_text = Amount.get().replace("", "").strip()
    if amount_text == 0 or amount_text == "Amount":
        messagebox.showerror("Error", "Select an item")
    else:
        discount_text = TDiscount.get().replace("%","").strip()
        if discount_text == 0 or discount_text == "Discount":
            amount = float(Amount.get().replace("",""))
            final = amount
            TGrand.config(state="normal", readonlybackground="#074463")
            TGrand.delete(0, "end")
            TGrand.insert(0, f"{final:.2f}")
            TGrand.config(state="readonly", readonlybackground="#074463")
        else:
            amount = float(Amount.get().replace("",""))
            discount = int(TDiscount.get().replace("%",""))
            discount_amount = (discount / 100) * amount
            final = amount - discount_amount
            TGrand.config(state="normal", readonlybackground="#074463")
            TGrand.delete(0, "end")
            TGrand.insert(0, f"{final:.2f}")
            TGrand.config(state="readonly", readonlybackground="#074463")

def Clear():
    for combobox in [
        PBodySoap, PFacewash, PFaceCream, PHairOil, PShampoo, PLotion, PRice, 
        PWheat, PSugar, PTea, PCoffee, PFoodOil, PColdDrink, PSnacks, 
        PStationery, PLighting, PCleaning, PTobacco
    ]:
        combobox.current(0)

    for entry, value in [
        (Amount, "Amount"), (TDiscount, "Discount"), (TGrand, "Grand Total"), 
        (Tgst, "Total GST"), (CCgst, "CGST"), (CSgst, "SGST"),(CGrooming, "Grooming"), (CFood, "Food"), (CEssential, "Essential") 
    ]:
        entry.config(state="normal", readonlybackground="#074463")
        entry.delete(0, "end")
        entry.insert(0, value)
        entry.config(state="readonly", readonlybackground="#074463")
    
def Clear():
    for combobox in [
        PBodySoap, PFacewash, PFaceCream, PHairOil, PShampoo, PLotion, PRice, 
        PWheat, PSugar, PTea, PCoffee, PFoodOil, PColdDrink, PSnacks, 
        PStationery, PLighting, PCleaning, PTobacco
    ]:
        combobox.current(0)

    for entry, value in [
        (Amount, "Amount"), (TDiscount, "Discount"), (TGrand, "Grand Total"), 
        (Tgst, "Total GST"), (CCgst, "CGST"), (CSgst, "SGST"),(CGrooming, "Grooming"), (CFood, "Food"), (CEssential, "Essential") 
    ]:
        entry.config(state="normal", readonlybackground="#074463")
        entry.delete(0, "end")
        entry.insert(0, value)
        entry.config(state="readonly", readonlybackground="#074463")

    for item in tv1.get_children():
        tv1.delete(item)
    
    CName.config(state="normal", readonlybackground="#074463")
    CName.delete(0,"end")
    CName.insert(0,"Name")
    CLastname.config(state="normal", readonlybackground="#074463")
    CLastname.delete(0,"end")
    CLastname.insert(0,"Lastame")
    CEmail.config(state="normal", readonlybackground="#074463")
    CEmail.delete(0,"end")
    CEmail.insert(0,"Email")
    CContact.config(state="normal", readonlybackground="#074463")
    CContact.delete(0,"end")
    CContact.insert(0,"Contact")

LF12=LabelFrame(top,height=100,width=1536,bg="#074463",bd=12,relief=GROOVE)
LF12.place(x=0,y=0)
Title=Label(LF12, text="Billing Software", fg="gold",bg="#074463", font=("Bookman Old Style", 40, "bold"))
Title.place(x=600,y=5)
CDetail=LabelFrame(top,text="Customer",height=130,width=1536,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 20, "bold"))
CDetail.place(x=0,y=105,relwidth=1)
PDetail=LabelFrame(top,text="Product",height=400,width=925,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 20, "bold"))
PDetail.place(x=0,y=240)
Counter=LabelFrame(top,text="Billing Menu",height=195,width=1536,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 20, "bold"))
Counter.place(x=0,y=645)

def on_click(e):
    CName.delete(0,"end")

def on_focus_out(e):
    name = CName.get()
    if name == "" or name == "Name" or name == "name":
        CName.insert(0,"Name")
    else:
        CName.config(state="readonly", readonlybackground="#074463")

def validate_name_input(char, value):
    if value == "":
        return True
    if char.isalpha():
        return True
    return False

CName=Entry(CDetail, text="Name", fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CName.place(x=50,y=30)
CName.insert(0, "Name")
CName.bind("<FocusIn>", on_click)
CName.bind("<FocusOut>", on_focus_out)
Customername = (CName.register(validate_name_input), "%S", "%P")
CName.config(validate="key", validatecommand=Customername)
frame3 =Frame(CDetail,width=262,height=2,bg="black").place(x=50, y=56)

def on_click(e):
    CLastname.delete(0,"end")

def on_focus_out(e):
    lastname = CLastname.get()
    if lastname == "" or lastname == "Lastname" or lastname == "lastname":
        CLastname.insert(0,"Lastname")
    else:
        CLastname.config(state="readonly", readonlybackground="#074463")

CLastname=Entry(CDetail, text="Lastname", fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CLastname.place(x=370,y=30)
CLastname.insert(0,"Lastname")
CLastname.bind("<FocusIn>", on_click)
CLastname.bind("<FocusOut>", on_focus_out)
Customerlastname = (CLastname.register(validate_name_input), "%S", "%P")
CLastname.config(validate="key", validatecommand=Customerlastname)
frame3 =Frame(CDetail,width=262,height=2,bg="black").place(x=370, y=56)

def on_click(e):
    CEmail.delete(0,"end")

def on_focus_out(e):
    email = CEmail.get()
    if email == "" or email == "Email" or email == "email":
        CEmail.insert(0,"Email")
    else:
        CEmail.config(state="readonly", readonlybackground="#074463")
CEmail=Entry(CDetail, text="Email", fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CEmail.place(x=680,y=30)
CEmail.insert(0,"Email")
CEmail.bind("<FocusIn>", on_click)
CEmail.bind("<FocusOut>", on_focus_out)
frame3 =Frame(CDetail,width=262,height=2,bg="black").place(x=680, y=56)

def on_click(e):
    CContact.delete(0,"end")
    CContact.config(validate="key", validatecommand=phone)

def on_focus_out(e):
    contact = CContact.get()
    if contact == "" or contact == "Contact" or contact == "contact":
        CContact.config(validate="none")
        CContact.insert(0,"Contact")
    else:
        CContact.config(state="readonly", readonlybackground="#074463")

def validate_digit_input(P):
    return P.isdigit() or P == ""

phone = (top.register(validate_digit_input), '%P')
CContact=Entry(CDetail, text="Contact", fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CContact.place(x=1000,y=30)
CContact.insert(0, "Contact")
CContact.bind("<FocusIn>", on_click)
CContact.bind("<FocusOut>", on_focus_out)
frame3 =Frame(CDetail,width=262,height=2,bg="black").place(x=1000, y=56)

Grooming = LabelFrame(PDetail,text="Grooming",height=330,width=270,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 15, "bold"))
Grooming.place(x=10,y=0)

Food = LabelFrame(PDetail,text="Food Supply",height=330,width=270,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 15, "bold"))
Food.place(x=290,y=0)

Essential = LabelFrame(PDetail,text="Daily Essential",height=330,width=300,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 15, "bold"))
Essential.place(x=570,y=0)

BodySoap = ["Body Soap","Dove","Lifebuoy","Dettol","Medimix","Cinthol","Pears"]
PBodySoap=ttk.Combobox(Grooming,values=BodySoap, width=10,font=("Bookman Old Style", 15, "bold"),state="readonly")
PBodySoap.place(x=50,y=8)
PBodySoap.current(0)

def on_bodysoap_select(event):
    prices = {"Dove": 50,"Lifebuoy": 20,"Dettol": 35,"Medimix": 10,"Cinthol": 45,"Pears": 60}
    return prices.get(PBodySoap.get(), 0)
PBodySoap.bind("<<ComboboxSelected>>", on_bodysoap_select)

FaceWash = ["Face Wash","Beardo","Mamaearth","Garnier","Clean & Clear","Himalaya","NIVEA"]
PFacewash=ttk.Combobox(Grooming, width=10,values=FaceWash,font=("Bookman Old Style", 15, "bold"),state="readonly")
PFacewash.place(x=50,y=55)
PFacewash.current(0)

def on_Facewash_select(event):
    prices = {"Beardo": 450,"Mamaearth": 235,"Garnier": 139,"Clean & Clear": 150,"Himalaya": 200,"NIVEA": 199}
    return prices.get(PFacewash.get(), 0)
PFacewash.bind("<<ComboboxSelected>>", on_Facewash_select)

FaceCream = ["Face Cream","Ponds","Olay","L'Oréal Paris","Biotiqu","Lakmé","Cetaphil"]
PFaceCream=ttk.Combobox(Grooming, width=10,values=FaceCream,font=("Bookman Old Style", 15, "bold"),state="readonly")
PFaceCream.place(x=50,y=105)
PFaceCream.current(0)

def on_FaceCream_select(event):
    prices = {"Ponds": 50,"Olay": 20,"L'Oréal Paris": 95,"Biotiqu": 150,"Lakmé": 650,"Cetaphil": 200}
    return prices.get(PFaceCream.get(), 0)
PFaceCream.bind("<<ComboboxSelected>>", on_FaceCream_select)

HairOil = ["Hair Oil","Parachute","Dabur Amla","Kesh King","Himalaya Herbals","Scalpe Plus","Indulekha Bringha"]
PHairOil=ttk.Combobox(Grooming, width=10,values=HairOil,font=("Bookman Old Style", 15, "bold"),state="readonly")
PHairOil.place(x=50,y=155)
PHairOil.current(0)

def on_HairOil_select(event):
    prices = {"Parachute": 91,"Dabur Amla": 64,"Kesh King": 46,"Himalaya Herbals": 79,"Scalpe Plus": 95,"Indulekha Bringha": 56}
    return prices.get(PHairOil.get(), 0)
PHairOil.bind("<<ComboboxSelected>>", on_HairOil_select)

Shampoo = ["Shampoo","Tresemme","Schwarzkopf","Nizoral","Pantene","Kerastase","Head & Shoulders"]
PShampoo=ttk.Combobox(Grooming, width=10,values=Shampoo,font=("Bookman Old Style", 15, "bold"),state="readonly")
PShampoo.place(x=50,y=205)
PShampoo.current(0)

def on_Shampoo_select(event):
    prices = {"Tresemme": 290,"Schwarzkopf": 250,"Nizoral": 101,"Pantene": 35,"Kerastase": 65,"Head & Shoulders": 25}
    return prices.get(PShampoo.get(), 0)
PShampoo.bind("<<ComboboxSelected>>", on_Shampoo_select)

Lotion = ["Lotion","Vaseline","Eucerin","Aveeno","Johnson's Baby","Neutrogena","Bio Oil"]
PLotion=ttk.Combobox(Grooming, width=10,values=Lotion,font=("Bookman Old Style", 15, "bold"),state="readonly")
PLotion.place(x=50,y=250)
PLotion.current(0)

def on_Lotion_select(event):
    prices = {"Vaseline": 100,"Eucerin": 150,"Aveeno": 173,"Johnson's Baby": 59,"Neutrogena": 109,"Bio Oil": 98}
    return prices.get(PLotion.get(), 0)
PLotion.bind("<<ComboboxSelected>>", on_Lotion_select)

Rice = ["Rice","Tilda","Daawat","India Gate","Kohinoor","Patanjali","Shree Lal Mahal"]
PRice=ttk.Combobox(Food, width=10,values=Rice,font=("Bookman Old Style", 15, "bold"),state="readonly")
PRice.place(x=50,y=8)
PRice.current(0)

def on_Rice_select(event):
    prices = {"Tilda": 59,"Daawat": 29,"India Gate": 43,"Kohinoor": 47,"Patanjali": 51,"Shree Lal Mahal": 54}
    return prices.get(PRice.get(), 0)
PRice.bind("<<ComboboxSelected>>", on_Rice_select)

Wheat = ["Wheat","Shakti Bhog","Aashirvaad","Pillsbury","Nature Fresh","Annapurna","Fortune Whole Wheat"]
PWheat=ttk.Combobox(Food, width=10,values=Wheat,font=("Bookman Old Style", 15, "bold"),state="readonly")
PWheat.place(x=50,y=55)
PWheat.current(0)

def on_Wheat_select(event):
    prices = {"Shakti Bhog": 310,"Aashirvaad": 390,"Pillsbury": 350,"Nature Fresh": 360,"Annapurna": 320,"Fortune Whole Wheat": 420}
    return prices.get(PWheat.get(), 0)
PWheat.bind("<<ComboboxSelected>>", on_Wheat_select)

Sugar = ["Sugar","Tata","Dharmani","Shree Hari" ,"Dharani" , "Rathna", "Madhur"]
PSugar=ttk.Combobox(Food, width=10,values=Sugar,font=("Bookman Old Style", 15, "bold"),state="readonly")
PSugar.place(x=50,y=105)
PSugar.current(0)

def on_Sugar_select(event):
    prices = {"Tata": 52,"Dharmani": 59,"Shree Hari": 65,"Dharani": 50,"Rathna": 45,"Madhur": 55}
    return prices.get(PSugar.get(), 0)
PSugar.bind("<<ComboboxSelected>>", on_Sugar_select)

Tea = ["Tea","Tata Tea","Brooke Bond","Wagh Bakri","Tetley","Lipton","Taj Mahal"]
PTea=ttk.Combobox(Food, width=10,values=Tea,font=("Bookman Old Style", 15, "bold"),state="readonly")
PTea.place(x=50,y=155)
PTea.current(0)

def on_Tea_select(event):
    prices = {"Tata Tea": 168,"Brooke Bond": 349,"Wagh Bakri": 280,"Tetley": 340,"Lipton": 540,"Taj Mahal": 650}
    return prices.get(PTea.get(), 0)
PTea.bind("<<ComboboxSelected>>", on_Tea_select)

Coffee = ["Coffee","Nescafé","Bru","Tata Coffee","Lavazza","Mountain Trail","Blue Tokai"]
PCoffee=ttk.Combobox(Food, width=10,values=Coffee,font=("Bookman Old Style", 15, "bold"),state="readonly")
PCoffee.place(x=50,y=205)
PCoffee.current(0)

def on_Coffee_select(event):
    prices = {"Nescafé": 120,"Bru": 100,"Tata Coffee": 149,"Lavazza": 259,"Mountain Trail": 300,"Blue Tokai": 250}
    return prices.get(PCoffee.get(), 0)
PCoffee.bind("<<ComboboxSelected>>", on_Coffee_select)

FoodOil = ["Food Oil","Saffola","Tata Sampann","Dalda","Mahakosh","Patanjali","Fortune"]
PFoodOil=ttk.Combobox(Food, width=10,values=FoodOil,font=("Bookman Old Style", 15, "bold"),state="readonly")
PFoodOil.place(x=50,y=250)
PFoodOil.current(0)

def on_FoodOil_select(event):
    prices = {"Saffola": 499,"Tata Sampann": 520,"Dalda": 150,"Mahakosh": 650,"Patanjali": 440,"Fortune": 480}
    return prices.get(PFoodOil.get(), 0)
PFoodOil.bind("<<ComboboxSelected>>", on_FoodOil_select)

ColdDrink = ["Cold Drink ","Frooti","Pepsi","Sprite","Mountain Dew","7UP","Red Bull"]
PColdDrink=ttk.Combobox(Essential, width=10,values=ColdDrink,font=("Bookman Old Style", 15, "bold"),state="readonly")
PColdDrink.place(x=50,y=8)
PColdDrink.current(0)

def on_ColdDrink_select(event):
    prices = {"Frooti": 10,"Pepsi": 80,"Sprite": 50,"Mountain Dew": 40,"7UP": 20,"Red Bull": 125}
    return prices.get(PColdDrink.get(), 0)
PColdDrink.bind("<<ComboboxSelected>>", on_ColdDrink_select)

Snacks = ["Snacks","Lay's","Pringles","Cheetos","Doritos","Haldiram","Bicano"]
PSnacks=ttk.Combobox(Essential, width=10,values=Snacks,font=("Bookman Old Style", 15, "bold"),state="readonly")
PSnacks.place(x=50,y=55)
PSnacks.current(0)

def on_Snacks_select(event):
    prices = {"Lay's": 10,"Pringles": 90,"Cheetos": 5,"Doritos": 20,"Haldiram": 15,"Bicano": 25}
    return prices.get(PSnacks.get(), 0)
PSnacks.bind("<<ComboboxSelected>>", on_Snacks_select)

Stationery = ["Stationery","Pencils","Markers","Erasers" ,"Rulers" , "Folders", "Notebooks"]
PStationery=ttk.Combobox(Essential, width=10,values=Stationery,font=("Bookman Old Style", 15, "bold"),state="readonly")
PStationery.place(x=50,y=105)
PStationery.current(0)

def on_Stationery_select(event):
    prices = {"Pencils": 5,"Markers": 25,"Erasers": 4,"Rulers": 10,"Folders": 30,"Notebooks": 20}
    return prices.get(PStationery.get(), 0)
PStationery.bind("<<ComboboxSelected>>", on_Stationery_select)

Lighting = ["Lighting","LED Bulbs","CFL Bulbs","Smart Bulbs","Table Lamps","Floor Lamps","Night Lights"]
PLighting=ttk.Combobox(Essential, width=10,values=Lighting,font=("Bookman Old Style", 15, "bold"),state="readonly")
PLighting.place(x=50,y=155)
PLighting.current(0)

def on_Lighting_select(event):
    prices = {"LED Bulbs": 150,"CFL Bulbs": 230,"Smart Bulbs": 440,"Table Lamps": 140,"Floor Lamps": 260,"Night Lights": 100}
    return prices.get(PLighting.get(), 0)
PLighting.bind("<<ComboboxSelected>>", on_Lighting_select)

Cleaning = ["Cleaning","Laundry Detergent","Air Freshener","Floor Cleaner","Vacuum Cleaner","Broom and Dustpan","Microfiber Cloths"]
PCleaning=ttk.Combobox(Essential, width=10,values=Cleaning,font=("Bookman Old Style", 15, "bold"),state="readonly")
PCleaning.place(x=50,y=205)
PCleaning.current(0)

def on_Cleaning_select(event):
    prices = {"Laundry Detergent": 135,"Air Freshener": 220,"Floor Cleaner": 80,"Vacuum Cleaner": 650,"Broom and Dustpan": 150,"Microfiber Cloths": 350}
    return prices.get(PCleaning.get(), 0)
PCleaning.bind("<<ComboboxSelected>>", on_Cleaning_select)

Tobacco = ["Tobacco","Cigarettes","E-cigarettes (Vapes)","Rolling Papers","Nicotine Pouches","Chewing Tobacco","Hookah Tobacco"]
PTobacco=ttk.Combobox(Essential, width=10,values=Tobacco,font=("Bookman Old Style", 15, "bold"),state="readonly")
PTobacco.place(x=50,y=250)
PTobacco.current(0)

def on_Tobacco_select(event):
    prices = {"Cigarettes": 120, "E-cigarettes (Vapes)": 200, "Rolling Papers": 5, "Nicotine Pouches": 85, "Chewing Tobacco": 20, "Hookah Tobacco": 180}
    return prices.get(PTobacco.get(), 0)
PTobacco.bind("<<ComboboxSelected>>", on_Tobacco_select)

Bill1 = LabelFrame(Counter,height=135,width=900,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 25, "bold"))
Bill1.place(x=5,y=0)

Bill2 = LabelFrame(Counter,height=135,width=595,fg="gold",bg="#074463",bd=12, font=("Bookman Old Style", 25, "bold"))
Bill2.place(x=910,y=0)

CGrooming=Entry(Counter,width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CGrooming.insert(0,"Grooming")
CGrooming.config(state="readonly",readonlybackground="#074463")
CGrooming.place(x=50,y=20)
frame3 =Frame(Counter,width=145,height=2,bg="black").place(x=50, y=46)

CFood=Entry(Counter, text="Food",width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CFood.insert(0,"Food")
CFood.config(state="readonly",readonlybackground="#074463")
CFood.place(x=210,y=20)
frame3 =Frame(Counter,width=145,height=2,bg="black").place(x=210, y=46)

CEssential=Entry(Counter,width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CEssential.insert(0,"Essential")
CEssential.config(state="readonly",readonlybackground="#074463")
CEssential.place(x=370,y=20)

frame3 =Frame(Counter,width=145,height=2,bg="black").place(x=370, y=46)

CCgst=Entry(Counter,width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CCgst.insert(0,"CGST")
CCgst.config(state="readonly",readonlybackground="#074463")
CCgst.place(x=570,y=20)
frame3 =Frame(Counter,width=145,height=2,bg="black").place(x=570, y=46)

CSgst=Entry(Counter,width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
CSgst.insert(0,"SGST")
CSgst.config(state="readonly",readonlybackground="#074463")
CSgst.place(x=730,y=20)
frame7 =Frame(Counter,width=145,height=2,bg="black").place(x=730, y=46)

Amount=Entry(Counter,width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
Amount.insert(0,"Amount")
Amount.config(state="readonly",readonlybackground="#074463")
Amount.place(x=50,y=70)
frame3 =Frame(Counter,width=145,height=2,bg="black").place(x=50, y=96)

Tgst=Entry(Counter,width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
Tgst.insert(0,"Total GST")
Tgst.config(state="readonly",readonlybackground="#074463")
Tgst.place(x=210,y=70)
frame3 =Frame(Counter,width=145,height=2,bg="black").place(x=210, y=96)

TDiscount=Entry(Counter,width=11, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
TDiscount.insert(0,"Discount")
TDiscount.config(state="readonly",readonlybackground="#074463")
TDiscount.place(x=370,y=70)
frame3 =Frame(Counter,width=145,height=2,bg="black").place(x=370, y=96)

TGrand=Entry(Counter,width=23, fg="gold",bg="#074463", border=0, font=("Bookman Old Style", 15, "bold"))
TGrand.insert(0,"Grand Total")
TGrand.config(state="readonly",readonlybackground="#074463")
TGrand.place(x=572,y=70)
frame3 =Frame(Counter,width=301,height=2,bg="black").place(x=572, y=96)


b2=Button(CDetail,cursor="hand2", pady=7, text="Search",width=8,border=0, bg="#074463",fg="White", font=("Arial", 20, "bold"), command=searchbill).place(x=1320, y=8)
b3=Button(Bill2,cursor="hand2", pady=7, text="Discount",  width=8,bg="#074463",fg="White", font=("Arial", 15, "bold"),command=Discount).place(x=25, y=30)
b4=Button(Bill2,cursor="hand2", pady=7, text="Total", width=6, bg="#074463",fg="White", font=("Arial", 15, "bold"), command=calculate_totals).place(x=132, y=30)
b5=Button(Bill2,cursor="hand2", pady=7, text="GST", width=6, bg="#074463",fg="White", font=("Arial", 15, "bold"),command=GST).place(x=215, y=30)
b6=Button(Bill2,cursor="hand2", pady=7, text="Grand total",width=9 ,bg="#074463",fg="White", font=("Arial", 15, "bold"),command= Final).place(x=298, y=30)
b7=Button(Bill2,cursor="hand2", pady=7, text="Print",width=5, bg="#074463",fg="White", font=("Arial", 15, "bold"),command=add).place(x=417, y=30)
b8=Button(Bill2,cursor="hand2", pady=7, text="Clear",width=5, bg="#074463",fg="White", font=("Arial", 15, "bold"),command=Clear).place(x=488, y=30)

top.mainloop()
