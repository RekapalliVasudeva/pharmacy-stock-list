from tkinter import *
from tkinter import messagebox, ttk
import os

f=open("database_proj",'a+')
root = Tk()
root.title("Simple Pharmacy Management System")
root.configure(width=1500,height=600,bg='BLACK')
var=-1

# ✅ Refresh categories from file
def get_categories():
    categories = set()
    with open("database_proj","r") as fcat:
        for line in fcat:
            values = line.strip().split(" ")
            if len(values) == 5:
                categories.add(values[3])
    return sorted(list(categories))

def additem():
    global var
    num_lines = 0
    with open("database_proj", 'r') as f10:
        for line in f10:
            num_lines += 1
    var=num_lines-1
    e1= entry1.get()
    e2=entry2.get()
    e3=entry3.get()
    e4=entry4.get()
    e5=entry5.get()
    f.write('{0} {1} {2} {3} {4}\n'.format(str(e1),e2,e3,str(e4),e5))
    f.flush()
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)

    # ✅ Auto-refresh categories if "VIEW ALL ITEMS" is open
    try:
        refresh_categories()
    except:
        pass

def deleteitem():
    e1=entry1.get()
    with open(r"database_proj") as f, open(r"database_proj1", "w") as working:
        for line in f:
            if str(e1) not in line:
                working.write(line)
    os.remove(r"database_proj")
    os.rename(r"database_proj1", r"database_proj")

    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)

def firstitem():
    global var
    var=0
    f.seek(var)
    c=f.readline()
    v=list(c.split(" "))
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry1.insert(0,str(v[0]))
    entry2.insert(0,str(v[1]))
    entry3.insert(0,str(v[2]))
    entry4.insert(0,str(v[3]))
    entry5.insert(0,str(v[4]))

def nextitem():
    global var
    var = var + 1
    f.seek(0)
    try:
        c=f.readlines()
        xyz = c[var]
        v = list(xyz.split(" "))
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)
        entry1.insert(0, str(v[0]))
        entry2.insert(0, str(v[1]))
        entry3.insert(0, str(v[2]))
        entry4.insert(0, str(v[3]))
        entry5.insert(0, str(v[4]))
    except:
        messagebox.showinfo("Title", "SORRY!...NO MORE RECORDS")

def previousitem():
    global var
    var=var-1
    f.seek(0)
    try:
        z = f.readlines()
        xyz=z[var]
        v = list(xyz.split(" "))
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)

        entry1.insert(0, str(v[0]))
        entry2.insert(0, str(v[1]))
        entry3.insert(0, str(v[2]))
        entry4.insert(0, str(v[3]))
        entry5.insert(0, str(v[4]))
    except:
        messagebox.showinfo("Title", "SORRY!...NO MORE RECORDS")

def lastitem():
    global var
    f4=open("database_proj",'r')
    x=f4.read().splitlines()
    last_line= x[-1]
    num_lines = 0
    with open("database_proj", 'r') as f8:
        for line in f8:
            num_lines += 1
    var=num_lines-1
    try:
        v = list(last_line.split(" "))
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
        entry4.delete(0, END)
        entry5.delete(0, END)

        entry1.insert(0, str(v[0]))
        entry2.insert(0, str(v[1]))
        entry3.insert(0, str(v[2]))
        entry4.insert(0, str(v[3]))
        entry5.insert(0, str(v[4]))
    except:
        messagebox.showinfo("Title", "SORRY!...NO MORE RECORDS")

def updateitem():
    e1 = entry1.get()
    e2 = entry2.get()
    e3 = entry3.get()
    e4 = entry4.get()
    e5 = entry5.get()
    with open(r"database_proj") as f1, open(r"database_proj1", "w") as working:
        for line in f1:
            if str(e1) not in line:
                working.write(line)
            else:
                working.write('{0} {1} {2} {3} {4}\n'.format(str(e1), e2, e3, str(e4), e5))
    os.remove(r"database_proj")
    os.rename(r"database_proj1", r"database_proj")

def searchitem():
    e11 = entry1.get()
    with open(r"database_proj") as working:
        for line in working:
            if str(e11) in line:
                v = list(line.split(" "))
                entry1.delete(0, END)
                entry2.delete(0, END)
                entry3.delete(0, END)
                entry4.delete(0, END)
                entry5.delete(0, END)
                entry1.insert(0, str(v[0]))
                entry2.insert(0, str(v[1]))
                entry3.insert(0, str(v[2]))
                entry4.insert(0, str(v[3]))
                entry5.insert(0, str(v[4]))
                break
        else:
            messagebox.showinfo("Title", "Item not found")

def clearitem():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)

# ✅ UPDATED FUNCTION: View All Items in Table with Category Filter
def viewitems():
    win = Toplevel(root)
    win.title("All Items")
    win.geometry("800x500")

    # --- Dropdown for category filter ---
    filter_frame = Frame(win)
    filter_frame.pack(fill=X, pady=5)

    Label(filter_frame, text="Filter by Category: ").pack(side=LEFT, padx=5)

    global category_dropdown, category_var, tree
    category_var = StringVar()
    category_dropdown = ttk.Combobox(filter_frame, textvariable=category_var, state="readonly")
    category_dropdown.pack(side=LEFT, padx=5)

    # --- Treeview (table) ---
    tree = ttk.Treeview(win, columns=("Name","Price","Qty","Category","Discount"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")
    tree.heading("Qty", text="Quantity")
    tree.heading("Category", text="Category")
    tree.heading("Discount", text="Discount")
    tree.pack(fill=BOTH, expand=True)

    # ✅ Function to load items (with optional category filter)
    def load_items(filter_cat=None):
        tree.delete(*tree.get_children())  # Clear table
        with open("database_proj","r") as fview:
            for line in fview:
                values = line.strip().split(" ")
                if len(values) == 5:
                    if filter_cat is None or values[3] == filter_cat:
                        tree.insert("", END, values=values)

    # ✅ Event: When category is selected, refresh table
    def on_category_change(event):
        selected = category_var.get()
        if selected == "All":
            load_items()
        else:
            load_items(selected)

    category_dropdown.bind("<<ComboboxSelected>>", on_category_change)

    # ✅ Refresh function (called from additem too)
    def refresh_categories():
        categories = get_categories()
        category_dropdown["values"] = ["All"] + categories
        if not category_var.get() or category_var.get() not in category_dropdown["values"]:
            category_dropdown.current(0)
        load_items(None if category_var.get()=="All" else category_var.get())

    # Make refresh_categories visible to additem()
    globals()["refresh_categories"] = refresh_categories

    # Initial load
    refresh_categories()

# --- GUI PART ---
label0= Label(root,text="PHARMACY MANAGEMENT SYSTEM ",bg="black",fg="white",font=("Times", 30))
label1=Label(root,text="ENTER ITEM NAME",bg="red",relief="ridge",fg="white",font=("Times", 12),width=25)
entry1=Entry(root , font=("Times", 12))
label2=Label(root, text="ENTER ITEM PRICE",bd="2",relief="ridge",height="1",bg="red",fg="white", font=("Times", 12),width=25)
entry2= Entry(root, font=("Times", 12))
label3=Label(root, text="ENTER ITEM QUANTITY",bd="2",relief="ridge",bg="red",fg="white", font=("Times", 12),width=25)
entry3= Entry(root, font=("Times", 12))
label4=Label(root, text="ENTER ITEM CATEGORY",bd="2",relief="ridge",bg="red",fg="white", font=("Times", 12),width=25)
entry4= Entry(root, font=("Times", 12))
label5=Label(root, text="ENTER ITEM DISCOUNT",bg="red",relief="ridge",fg="white", font=("Times", 12),width=25)
entry5= Entry(root, font=("Times", 12))

button1= Button(root, text="ADD ITEM", width=20, command=additem)
button2= Button(root, text="DELETE ITEM", width=20, command=deleteitem)
button3= Button(root, text="VIEW FIRST ITEM", width=20, command=firstitem)
button4= Button(root, text="VIEW NEXT ITEM", width=20, command=nextitem)
button5= Button(root, text="VIEW PREVIOUS ITEM", width=20, command=previousitem)
button6= Button(root, text="VIEW LAST ITEM", width=20, command=lastitem)
button7= Button(root, text="UPDATE ITEM", width=20, command=updateitem)
button8= Button(root, text="SEARCH ITEM", width=20, command=searchitem)
button9= Button(root, text="CLEAR SCREEN", width=20, command=clearitem)
button10= Button(root, text="VIEW ALL ITEMS", width=20, command=viewitems)

# Placing Widgets
label0.grid(columnspan=6, padx=10, pady=10)
label1.grid(row=1,column=0, sticky=W, padx=10, pady=10)
label2.grid(row=2,column=0, sticky=W, padx=10, pady=10)
label3.grid(row=3,column=0, sticky=W, padx=10, pady=10)
label4.grid(row=4,column=0, sticky=W, padx=10, pady=10)
label5.grid(row=5,column=0, sticky=W, padx=10, pady=10)

entry1.grid(row=1,column=1, padx=40, pady=10)
entry2.grid(row=2,column=1, padx=10, pady=10)
entry3.grid(row=3,column=1, padx=10, pady=10)
entry4.grid(row=4,column=1, padx=10, pady=10)
entry5.grid(row=5,column=1, padx=10, pady=10)

button1.grid(row=1,column=4, padx=40, pady=10)
button2.grid(row=1,column=5, padx=40, pady=10)
button3.grid(row=2,column=4, padx=40, pady=10)
button4.grid(row=2,column=5, padx=40, pady=10)
button5.grid(row=3,column=4, padx=40, pady=10)
button6.grid(row=3,column=5, padx=40, pady=10)
button7.grid(row=4,column=4, padx=40, pady=10)
button8.grid(row=4,column=5, padx=40, pady=10)
button9.grid(row=5,column=5, padx=40, pady=10)
button10.grid(row=5,column=4, padx=40, pady=10)

root.mainloop()
