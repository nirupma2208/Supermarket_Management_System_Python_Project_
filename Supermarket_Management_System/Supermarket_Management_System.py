import os
import sqlite3
from datetime import date
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from threading import Thread
from time import sleep
import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.constants import *
from tkinter import Toplevel
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk
from tkinter import messagebox
from random import randint
from ttkbootstrap.tooltip import ToolTip
from re import compile, match
from fpdf import FPDF


def connect_to_database():
    db = sqlite3.connect('database\\DATABASE.db')
    con = db.cursor()
    return con, db


def connect_to_built_database(DATABASE):
    db = sqlite3.connect(f'database\\{DATABASE}.db')
    con = db.cursor()
    return con, db


def create_database(DATABASE):
    db = sqlite3.connect(f'database\\{DATABASE}.db')
    con = db.cursor()
    con.execute(
        'create table if not exists Inventory_1(productId TEXT,name TEXT, category TEXT,subcategory TEXT,qty TEXT,mrp TEXT,costPrice TEXT,vendorNum TEXT);')
    con.execute('create table if not exists Invoices(biilNum TEXT,date TEXT, name TEXT,contact TEXT);')
    con.execute('create table if not exists productDetails(billNum TEXT,text1 TEXT);')
    con.execute('create table if not exists sending_mail(email TEXT,password TEXT);')
    con.execute(
        'create table if not exists store_details(name TEXT,location TEXT,telephone TEXT,helpline TEXT,email TEXT);')
    db.commit()
    db.close()


def insert_login_cred(desig, admin_email, empid):
    data = connect_to_database()
    cur, db = data[0], data[1]
    try:
        cur.execute('delete from Login')
    except:
        pass
    cur.execute('insert into Login(desig,admin_email,employee_id) values(?,?,?)', (desig, admin_email, empid))
    db.commit()
    db.close()


def fetch_login_cred():
    result = ''
    data = connect_to_database()
    cur, db = data[0], data[1]

    r = cur.execute('select * from Login')
    for i in r:
        result = i
    db.commit()
    db.close()
    return result


data = connect_to_database()
con, db = data[0], data[1]
con.execute(
    'create table if not exists Employee_cred(admin_Id TEXT,empId TEXT,name TEXT, contact TEXT,address TEXT,aadhar TEXT,password TEXT,designation TEXT);')
con.execute('create table if not exists admin_cred(id TEXT,pass TEXT);')
con.execute('create table if not exists Login(desig TEXT,admin_email TEXT,employee_id TEXT);')
db.commit()
db.close()


def GetRandom(string):
    number = randint(1111, 9999)
    return ''.join([string, str(number)])


def send_pdf(sender, password, receiver, body, pdfname):
    pdfname=f'invoices_pdf\\{pdfname}.pdf'
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'Invoice'
    message.attach(MIMEText(body, 'plain'))
    binary_pdf = open(pdfname, 'rb')
    payload = MIMEBase('application', 'octate-stream', Name=pdfname)
    payload.set_payload((binary_pdf).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
    message.attach(payload)
    session = SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()


def PDF_MAKER(PdfName, bill_number, custoName, custoContact, Date, details, name, location, telephone, helpline,
              emailid):
    l2 = []
    for i in details:
        l2.append(i.split("|"))
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=17)
    pdf.cell(200, 10, txt="Invoice",
             ln=1, align='W')
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 6, txt=name, ln=2,
             align='C')
    pdf.cell(200, 6, txt=location,
             ln=2, align='C')
    pdf.cell(200, 6, txt=f'Telephone No. : {telephone}', ln=2,
             align='C')
    pdf.cell(200, 6, txt=f'Help Line No. : {helpline}', ln=2,
             align='C')
    pdf.cell(200, 6, txt=f'Email ID : {emailid}', ln=2,
             align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(100, 6, txt=f'Bill Number : {bill_number} ', ln=2,
             align='W')
    pdf.cell(20, 6, txt=f'Customer Contact No. : {custoContact} ', ln=2,
             align='E')
    pdf.cell(100, 6, txt=f'Customer Name : {custoName} ', ln=2,
             align='W')
    pdf.cell(20, 6, txt=f'Date. : {Date} ', ln=2,
             align='E')
    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, 80, 200, 80)
    pdf.cell(200, 6, txt='', ln=2,
             align='C')
    pdf.cell(40, 10, 'Products Details', ln=2)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(10, 90, 200, 90)
    pdf.cell(200, 10, '', ln=2)
    for i in l2[:-1]:
        pdf.cell(40, 6, f'Products : {i[0]} | Quantity : {i[1]} | Price : {i[2]} ', ln=2)
    else:
        pdf.cell(40, 6, f"{l2[-1][2]}", ln=2)
    pdf.output(f"invoices_pdf\\{PdfName}.pdf")


class Main_Window:
    def on_closing(self):
        self.root.destroy()
        exit()

    def __init__(self, root):
        self.root = root
        self.root.title('Supermarket Management System')
        self.root.resizable(0, 0)
        self.root.configure(bg='#F4F4F4')
        self.root.geometry('570x400+600+200')
        self.root.iconbitmap('icon\\main.ico')
        self.Employee_Admin_Buttons()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def Employee_Admin_Buttons(self):
        self.main_image = ttk.PhotoImage(file='images\\Main_Page.png')
        self.main_img_label = ttk.Label(self.root, image=self.main_image, background='#F4F4F4')
        self.main_img_label.place(x=0, y=30)

        self.Employee_Button = ttk.Button(self.root, text='EMPLOYEE', width=20, bootstyle=(DARK, OUTLINE),
                                          cursor='hand2', takefocus=0, command=self.command_for_employee_button)
        self.Employee_Button.place(x=350, y=130)

        self.Admin_Button = ttk.Button(self.root, text='ADMIN', width=20, bootstyle=(DARK, OUTLINE), cursor='hand2',
                                       takefocus=0, command=self.command_for_admin_button)
        self.Admin_Button.place(x=350, y=190)

    def command_for_employee_button(self):
        self.employee_root = Toplevel()
        self.employee_root.title('EMPLOYEE')
        self.employee_root.resizable(0, 0)
        self.employee_root.configure(bg='white')
        self.employee_root.geometry('700x420+600+200')
        self.employee_root.iconbitmap('icon\\main.ico')
        self.employee_image = ttk.PhotoImage(file='images\\Employee_Root.png')
        self.employee_image_label = ttk.Label(self.employee_root, image=self.employee_image, background='#F4F4F4',
                                              border=0)

        self.Emplyee_text_label = ttk.Label(self.employee_root, text='Employee Login', font=('calibri', 12, 'bold'))
        self.Emplyee_text_label.place(x=350, y=30)

        self.separator = ttk.Separator(self.employee_root, orient=HORIZONTAL, bootstyle=SUCCESS)
        self.separator.place(x=353, y=60)

        self.Emplyee_username_label = ttk.Label(self.employee_root, text='UserID', font=('calibri', 9, 'bold'),
                                                foreground='gray')
        self.Emplyee_username_label.place(x=380, y=120)

        self.employee_usernam_entry = ttk.Entry(self.employee_root, bootstyle="dark", width=30)
        self.employee_usernam_entry.place(x=380, y=145)

        self.Emplyee_pass_label = ttk.Label(self.employee_root, text='Password', font=('calibri', 9, 'bold'),
                                            foreground='gray')
        self.Emplyee_pass_label.place(x=380, y=185)

        self.employee_pass_entry = ttk.Entry(self.employee_root, bootstyle="dark", width=30, show='*')
        self.employee_pass_entry.place(x=380, y=210)

        self.employee_login_button = ttk.Button(self.employee_root, text='LOGIN', width=15, bootstyle=(SUCCESS),
                                                cursor='hand2',
                                                takefocus=0, command=self.command_for_emp_login_button)
        self.employee_login_button.place(x=440, y=280)

        self.employee_image_label.place(x=0, y=0)

    def command_for_emp_login_button(self):
        if self.employee_usernam_entry.get() == '' or self.employee_pass_entry.get() == '':
            Messagebox.show_warning('Empty fields', '', self.employee_root)
        else:
            result = self.fetch_emp_cred()
            if result!='':
                insert_login_cred('E', result[0], '')
                self.employee_root.withdraw()
                self.root.withdraw()
                top = tk.Toplevel()
                Employee_Panel(result[0], top)
            else:
                Messagebox.show_error('Invalid Id password','',self.employee_root)

    def fetch_emp_cred(self):
        data = connect_to_database()
        con, db = data[0], data[1]
        result = ''
        r = con.execute('select * from Employee_cred where empId=? and password=?',
                        (self.employee_usernam_entry.get(), self.employee_pass_entry.get()))
        for i in r:
            result = i
        db.commit()
        db.close()
        return result

    def command_for_admin_button(self):
        self.admin_root = Toplevel()
        self.admin_root.title('admin')
        self.admin_root.resizable(0, 0)
        self.admin_root.configure(bg='white')
        self.admin_root.geometry('700x420+600+200')
        self.admin_root.iconbitmap('icon\\main.ico')
        self.admin_image = ttk.PhotoImage(file='images\\Employee_Root.png')
        self.admin_image_label = ttk.Label(self.admin_root, image=self.admin_image, background='#F4F4F4', border=0)

        self.admin_text_label = ttk.Label(self.admin_root, text='Admin Login', font=('calibri', 12, 'bold'))
        self.admin_text_label.place(x=350, y=30)

        self.separator = ttk.Separator(self.admin_root, orient=HORIZONTAL, bootstyle=SUCCESS)
        self.separator.place(x=353, y=60)

        self.admin_username_label = ttk.Label(self.admin_root, text='UserID', font=('calibri', 9, 'bold'),
                                              foreground='gray')
        self.admin_username_label.place(x=380, y=120)

        self.admin_usernam_entry = ttk.Entry(self.admin_root, bootstyle="dark", width=30)
        self.admin_usernam_entry.place(x=380, y=145)

        self.admin_pass_label = ttk.Label(self.admin_root, text='Password', font=('calibri', 9, 'bold'),
                                          foreground='gray')
        self.admin_pass_label.place(x=380, y=185)

        self.admin_pass_entry = ttk.Entry(self.admin_root, bootstyle="dark", width=30, show='*')
        self.admin_pass_entry.place(x=380, y=210)

        self.admin_login_button = ttk.Button(self.admin_root, text='LOGIN', width=15, bootstyle=(SUCCESS),
                                             cursor='hand2',
                                             takefocus=0, command=self.command_for_admin_login_button)
        self.admin_login_button.place(x=440, y=280)

        self.ID_link_button = ttk.Button(self.admin_root, text='To Get ID / Password', bootstyle='info-link',
                                         cursor='hand2',
                                         takefocus=0, underline=0, command=self.Get_ID_Password)
        self.ID_link_button.place(x=520, y=370)

        self.admin_image_label.place(x=0, y=0)

    def command_for_admin_login_button(self):
        if self.admin_usernam_entry.get() == '' or self.admin_pass_entry.get() == '':
            Messagebox.show_warning('Empty Fields', '', self.admin_root)
        else:
            result = self.fetch_id_pass_from_database(self.admin_usernam_entry.get(), self.admin_pass_entry.get())
            if result == '':
                Messagebox.show_error('Invalid ID / Password', '', self.admin_root)
            else:
                insert_login_cred('A', result[0], '')
                create_database(result[0])
                self.admin_root.withdraw()
                self.root.withdraw()

                top = tk.Toplevel()
                Admin_panel().Main(result[0], top)


    def fetch_id_pass_from_database(self, id, passs):
        result = ''
        data = connect_to_database()
        cur, db = data[0], data[1]
        r = cur.execute('select id,pass from admin_cred where id=? and pass=?', (id, passs))
        for i in r:
            result = i
        db.commit()
        db.close()
        return result

    def Get_ID_Password(self):
        utility.enable_high_dpi_awareness()
        self.result = Querybox.get_string("Enter Your Email ID", initialvalue='',
                                          parent=self.admin_root)


        if self.result != None:
            Thread(target=self.check_if_login_id_is_used, daemon=True).start()
            Messagebox.show_info('Wait...click on OK', '', self.admin_root)

            if self.isTrue:
                r = GetRandom('ID@')
                data = connect_to_database()
                cur, db = data[0], data[1]
                cur.execute('insert into admin_cred(id,pass) values(?,?)', (self.result, r))
                db.commit()
                db.close()
                self.send_id_pass(self.result, r)
                Messagebox.show_info('Check your email for UserID and Password', '', self.admin_root)

            else:

                # data = connect_to_database()
                # cur, db = data[0], data[1]
                # cur.execute('delete from admin_cred')
                # db.commit()
                # db.close()
                Messagebox.show_error('Someone is already used this email as login ID', '', self.admin_root)

    def check_if_login_id_is_used(self):
        self.isTrue = True
        data = connect_to_database()
        cur, db = data[0], data[1]
        r1 = cur.execute('select id from admin_cred where id=?', (self.result,))
        for i in r1:
            result = i
            if result[0] == self.result:
                self.isTrue = False
                break
            else:
                self.isTrue = True
                break
        db.commit()
        db.close()

    def send_id_pass(self, receiver, pas):
        body = f'''Hello,
        This is your Id, Password
        User ID : {receiver},
        Password : {pas}
        Don't share with anyone
        Thank you !!!
        '''
        sender = 'aruniru2208@gmail.com'
        password = 'Nirupma@123'
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = 'SMS'
        message.attach(MIMEText(body, 'plain'))
        session = SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender, password)
        text = message.as_string()
        session.sendmail(sender, receiver, text)
        session.quit()


class Admin_panel:
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.Admin_panel.destroy()
            exit()
    def Main(self, name, top):
        self.database_name = name
        self.Admin_panel = top
        self.Admin_panel.title('Admin Panel')
        self.Admin_panel.configure(bg='#F4F4F4')
        self.Admin_panel.geometry('1400x800+200+50')
        self.Admin_panel.iconbitmap('icon\\main.ico')
        self.define_frame()
        self.username_(name)
        self.ALL_Buttons()
        self.inveventory_management()
        self.Admin_panel.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.Admin_panel.mainloop()

    def define_frame(self):
        self.frame = ttk.Frame(self.Admin_panel, bootstyle="info")
        self.frame.pack(side=TOP, fill=BOTH, expand=True)

        self.frame1 = ttk.Frame(self.frame, bootstyle="primary", width=260)
        self.frame1.pack(side=LEFT, fill=Y)

        self.frame2 = tk.Frame(self.frame, background='white', highlightthickness=20, highlightbackground='white',
                               highlightcolor='white')
        self.frame2.pack(side=RIGHT, fill=BOTH, expand=True)

        self.frame3 = tk.Frame(self.frame2, background='white', highlightthickness=0, highlightbackground='white',
                               highlightcolor='white')
        self.frame3.pack(side=RIGHT, fill=BOTH, expand=True)

    def ALL_Buttons(self):
        self.sep1 = ttk.Label(self.frame1, text='', width=15, bootstyle="inverse-primary")
        self.sep1.pack(side=TOP, fill=X, ipadx=10, ipady=5)
        self.sep2 = ttk.Label(self.frame1, text='', width=15, bootstyle="inverse-primary")
        self.sep2.pack(side=TOP, fill=X, ipadx=10, ipady=5)
        self.invt_image1 = ttk.PhotoImage(file='images\\invt.png')

        self.inventory_button = ttk.Button(self.frame1, text='Inventory', width=15,
                                           cursor='hand2',
                                           takefocus=0, padding=15, command=self.command_for_inventory_button,
                                           bootstyle=INFO, image=self.invt_image1, compound=LEFT)
        self.inventory_button.pack(side=TOP, fill=X)
        self.emp_image1 = ttk.PhotoImage(file='images\\emp.png')

        self.emp_button = ttk.Button(self.frame1, text='Employee', width=15,
                                     cursor='hand2',
                                     takefocus=0, padding=15, command=self.command_for_emp_button,
                                     image=self.emp_image1, compound=LEFT)
        self.emp_button.pack(side=TOP, fill=X)
        self.invoice_image1 = ttk.PhotoImage(file='images\\paper.png')

        self.invoice_button = ttk.Button(self.frame1, text='Invoices', width=15,
                                         cursor='hand2',
                                         takefocus=0, padding=15, command=self.command_for_invoice_button,
                                         image=self.invoice_image1, compound=LEFT)
        self.invoice_button.pack(side=TOP, fill=X)
        self.setting_image1 = ttk.PhotoImage(file='images\\settings.png')

        self.setting_button = ttk.Button(self.frame1, text='Settings', width=15, bootstyle=PRIMARY,
                                         cursor='hand2',
                                         takefocus=0, padding=15, image=self.setting_image1, compound=LEFT,
                                         command=self.command_for_setting_button)
        self.setting_button.pack(side=TOP, fill=X)

        self.logout_image1 = ttk.PhotoImage(file='images\\logout.png')

        self.logout_button = ttk.Button(self.frame1, text='Logout', width=15, bootstyle=PRIMARY,
                                        cursor='hand2',
                                        takefocus=0, padding=15, image=self.logout_image1, compound=LEFT,
                                        command=self.command_for_logout_button)
        self.logout_button.pack(side=TOP, fill=X)

    def command_for_logout_button(self):
        d = messagebox.askyesno('', 'Do you want to logout')
        if d:
            insert_login_cred('N', '', '')
            self.Admin_panel.withdraw()
            self.main_window = tk.Toplevel()
            Main_Window(self.main_window)


    def delete_pre_frame(self):
        self.frame2_1.pack_forget()
        self.label.pack_forget()
        self.frame2_2.pack_forget()
        self.frame2_3.pack_forget()

    # Inventory
    def inveventory_management(self):
        self.frame2_1 = tk.Frame(self.frame3, background='white')
        self.frame2_1.pack(side=TOP, fill=X)

        self.label = tk.Label(self.frame3, height=2)
        self.label.pack(side=TOP, fill=X)

        self.frame2_2 = tk.Frame(self.frame3, background='white')
        self.frame2_2.pack(side=TOP, fill=X)

        self.frame2_3 = tk.Frame(self.frame3, background='white', highlightthickness=20, highlightbackground='white',
                                 highlightcolor='white')
        self.frame2_3.pack(side=TOP, fill=BOTH, expand=True)

        self.label1 = tk.Label(self.frame2_1, text='Inventory Managment', bg='white', font=('calibri', 17, 'bold'))
        self.label1.pack(side=TOP, fill=X)

        self.sep1 = tk.Label(self.frame2_2, text='', width=2)
        self.sep1.pack(side=LEFT, fill=Y)

        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback_treeview_1(sv))

        self.search_box1 = ttk.Entry(self.frame2_2, bootstyle=DARK, width=30, textvariable=sv)
        self.search_box1.pack(side=LEFT, fill=Y)

        self.searchBar_image1 = ttk.PhotoImage(file='images\\searchBar.png')
        self.searchBar_img_label1 = ttk.Label(self.frame2_2, image=self.searchBar_image1, background='white')
        self.searchBar_img_label1.pack(side=LEFT, fill=Y)

        ToolTip(
            self.searchBar_img_label1,
            text="Search the Data.",
        )

        self.sep1_1 = tk.Label(self.frame2_2, text='', width=2)
        self.sep1_1.pack(side=RIGHT, fill=Y)

        self.add_image1 = ttk.PhotoImage(file='images\\add.png')
        self.add_img_label1 = ttk.Button(self.frame2_2, image=self.add_image1, bootstyle=LIGHT, padding=0,
                                         cursor='hand2', takefocus=0, command=self.add_new_product)
        self.add_img_label1.pack(side=RIGHT, fill=Y)
        ToolTip(
            self.add_img_label1,
            text="Add Data to the Table.",
        )

        self.sep1_2 = tk.Label(self.frame2_2, text='', width=1)
        self.sep1_2.pack(side=RIGHT, fill=Y)

        self.minus_image1 = ttk.PhotoImage(file='images\\minus.png')
        self.minus_img_label1 = ttk.Button(self.frame2_2, image=self.minus_image1, bootstyle=LIGHT, padding=0,
                                           cursor='hand2', takefocus=0, command=self.delete_treeview_1_row)
        self.minus_img_label1.pack(side=RIGHT, fill=Y)

        ToolTip(
            self.minus_img_label1,
            text="Delete selected data from the table.",
        )

        self.sep1_3 = tk.Label(self.frame2_2, text='', width=2)
        self.sep1_3.pack(side=RIGHT, fill=Y)

        self.update_image1 = ttk.PhotoImage(file='images\\update.png')
        self.update_img_label1 = ttk.Button(self.frame2_2, image=self.update_image1, bootstyle=LIGHT, padding=0,
                                            cursor='hand2', takefocus=0, command=self.update_treeview_1_row)
        self.update_img_label1.pack(side=RIGHT, fill=Y)

        ToolTip(
            self.update_img_label1,
            text="Update selected Data",
        )

        self.sep1_4 = tk.Label(self.frame2_2, text='', width=1)
        self.sep1_4.pack(side=RIGHT, fill=Y)

        self.delete_all_image1 = ttk.PhotoImage(file='images\\delete.png')
        self.delete_all_img_label1 = ttk.Button(self.frame2_2, image=self.delete_all_image1, bootstyle=LIGHT, padding=0,
                                                cursor='hand2', takefocus=0, command=self.delete_all_treeview_1_data)
        self.delete_all_img_label1.pack(side=RIGHT, fill=Y)

        ToolTip(
            self.delete_all_img_label1,
            text="Delete All Data from the Table.",
        )

        self.treeview_for_inventory()

    def treeview_for_inventory(self):
        self.scroll = ttk.Scrollbar(self.frame2_3, bootstyle="round", orient=VERTICAL)
        self.scroll.pack(side=RIGHT, fill=Y)
        columns = [1, 2, 3, 4, 5, 6, 7, 8]
        headings = ['Product ID', 'Name', 'Category', 'Sub category', 'In stock', 'MRP', 'Cost Price', 'Vendor Number']
        self.treeview_1 = ttk.Treeview(self.frame2_3, bootstyle='info', columns=columns, show='headings',
                                       xscrollcommand=self.scroll)

        self.treeview_1.column(1, anchor=CENTER, width=100)
        self.treeview_1.column(2, anchor=CENTER, width=100)
        self.treeview_1.column(3, anchor=CENTER, width=100)
        self.treeview_1.column(4, anchor=CENTER, width=100)
        self.treeview_1.column(5, anchor=CENTER, width=100)
        self.treeview_1.column(6, anchor=CENTER, width=100)
        self.treeview_1.column(7, anchor=CENTER, width=100)
        self.treeview_1.column(8, anchor=CENTER, width=100)

        self.treeview_1.heading(columns[0], text=headings[0])
        self.treeview_1.heading(columns[1], text=headings[1])
        self.treeview_1.heading(columns[2], text=headings[2])
        self.treeview_1.heading(columns[3], text=headings[3])
        self.treeview_1.heading(columns[4], text=headings[4])
        self.treeview_1.heading(columns[5], text=headings[5])
        self.treeview_1.heading(columns[6], text=headings[6])
        self.treeview_1.heading(columns[7], text=headings[7])

        self.treeview_1.pack(side=LEFT, fill=BOTH, expand=True)
        self.Data_inserted_into_treeview_1()

    def command_for_inventory_button(self):
        self.inventory_button.configure(bootstyle=INFO)
        self.invoice_button.configure(bootstyle=PRIMARY)
        self.emp_button.configure(bootstyle=PRIMARY)
        self.setting_button.configure(bootstyle=PRIMARY)
        self.delete_pre_frame()
        self.inveventory_management()

    def add_new_product(self):
        self.add_ProductTk = ttk.Toplevel()
        self.add_ProductTk.title('Add Product')
        self.add_ProductTk.geometry('700x500+200+50')
        self.add_ProductTk.iconbitmap('icon\\main.ico')

        self.F1 = ttk.Frame(self.add_ProductTk)
        self.F1.pack(side=TOP, fill=BOTH, expand=True)

        x = 100
        y = 50
        DiffX = 100
        DiffY = 50
        width = 40
        EntryX = 250

        self.ProductName_Label = ttk.Label(self.F1, text='Product Name', takefocus=0)
        self.ProductName_Label.place(x=x, y=y)
        self.ProductName_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.ProductName_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.Category_Label = ttk.Label(self.F1, text='Category', takefocus=0)
        self.Category_Label.place(x=x, y=y)
        self.Category_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.Category_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.SubCategory_Label = ttk.Label(self.F1, text='Sub Category', takefocus=0)
        self.SubCategory_Label.place(x=x, y=y)
        self.SubCategory_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.SubCategory_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.Quantity_Label = ttk.Label(self.F1, text='Quantity', takefocus=0)
        self.Quantity_Label.place(x=x, y=y)
        self.Quantity_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.Quantity_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.MRP_Label = ttk.Label(self.F1, text='MRP', takefocus=0)
        self.MRP_Label.place(x=x, y=y)
        self.MRP_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.MRP_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.CostPrice_Label = ttk.Label(self.F1, text='Cost Price', takefocus=0)
        self.CostPrice_Label.place(x=x, y=y)
        self.CostPrice_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.CostPrice_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.VendorNum_Label = ttk.Label(self.F1, text='Vendor Number', takefocus=0)
        self.VendorNum_Label.place(x=x, y=y)
        self.VendorNum_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.VendorNum_Entry.place(x=EntryX, y=y)

        self.add_Buttn = ttk.Button(self.F1, bootstyle=SUCCESS, padding=8,
                                    cursor='hand2', takefocus=0, text='ADD', width=15,
                                    command=self.command_for_addProduct_button)
        self.add_Buttn.place(x=250, y=y + 70)

        self.add_ProductTk.resizable(0, 0)
        self.add_ProductTk.mainloop()

    def update_new_product(self, ProductName, Category, SubCategory, Quantity, MRP, CostPrice, VendorNum):
        self.Updateadd_ProductTk = ttk.Toplevel()
        self.Updateadd_ProductTk.title('Update Product')
        self.Updateadd_ProductTk.geometry('700x500+200+50')
        self.Updateadd_ProductTk.iconbitmap('icon\\main.ico')

        self.UpdateF1 = ttk.Frame(self.Updateadd_ProductTk)
        self.UpdateF1.pack(side=TOP, fill=BOTH, expand=True)

        x = 100
        y = 50
        DiffX = 100
        DiffY = 50
        width = 40
        EntryX = 250

        self.UpdateProductName_Label = ttk.Label(self.UpdateF1, text='Product Name', takefocus=0)
        self.UpdateProductName_Label.place(x=x, y=y)
        self.UpdateProductName_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateProductName_Entry.place(x=EntryX, y=y)
        self.UpdateProductName_Entry.insert(0, ProductName)

        x = DiffX
        y += DiffY
        self.UpdateCategory_Label = ttk.Label(self.UpdateF1, text='Category', takefocus=0)
        self.UpdateCategory_Label.place(x=x, y=y)
        self.UpdateCategory_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateCategory_Entry.place(x=EntryX, y=y)
        self.UpdateCategory_Entry.insert(0, Category)

        x = DiffX
        y += DiffY
        self.UpdateSubCategory_Label = ttk.Label(self.UpdateF1, text='Sub Category', takefocus=0)
        self.UpdateSubCategory_Label.place(x=x, y=y)
        self.UpdateSubCategory_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateSubCategory_Entry.place(x=EntryX, y=y)
        self.UpdateSubCategory_Entry.insert(0, SubCategory)

        x = DiffX
        y += DiffY
        self.UpdateQuantity_Label = ttk.Label(self.UpdateF1, text='Quantity', takefocus=0)
        self.UpdateQuantity_Label.place(x=x, y=y)
        self.UpdateQuantity_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateQuantity_Entry.place(x=EntryX, y=y)
        self.UpdateQuantity_Entry.insert(0, Quantity)

        x = DiffX
        y += DiffY
        self.UpdateMRP_Label = ttk.Label(self.UpdateF1, text='MRP', takefocus=0)
        self.UpdateMRP_Label.place(x=x, y=y)
        self.UpdateMRP_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateMRP_Entry.place(x=EntryX, y=y)
        self.UpdateMRP_Entry.insert(0, MRP)

        x = DiffX
        y += DiffY
        self.UpdateCostPrice_Label = ttk.Label(self.UpdateF1, text='Cost Price', takefocus=0)
        self.UpdateCostPrice_Label.place(x=x, y=y)
        self.UpdateCostPrice_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateCostPrice_Entry.place(x=EntryX, y=y)
        self.UpdateCostPrice_Entry.insert(0, CostPrice)

        x = DiffX
        y += DiffY
        self.UpdateVendorNum_Label = ttk.Label(self.UpdateF1, text='Vendor Number', takefocus=0)
        self.UpdateVendorNum_Label.place(x=x, y=y)
        self.UpdateVendorNum_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateVendorNum_Entry.place(x=EntryX, y=y)
        self.UpdateVendorNum_Entry.insert(0, VendorNum)

        self.Update_Buttn = ttk.Button(self.UpdateF1, bootstyle=SUCCESS, padding=8,
                                       cursor='hand2', takefocus=0, text='UPDATE', width=15,
                                       command=self.command_for_updateProduct_button)
        self.Update_Buttn.place(x=250, y=y + 70)

        self.Updateadd_ProductTk.resizable(0, 0)
        self.Updateadd_ProductTk.mainloop()

    def command_for_updateProduct_button(self):
        if self.UpdateProductName_Entry.get() == '' or self.UpdateCategory_Entry.get() == '' \
                or self.UpdateSubCategory_Entry.get() == '' or self.UpdateQuantity_Entry.get() == '' \
                or self.UpdateMRP_Entry.get() == '' or self.UpdateCostPrice_Entry.get() == '' or self.UpdateVendorNum_Entry.get() == '':
            Messagebox.show_warning('Empty Box', '', self.UpdateF1)
        else:
            val = (self.productID, self.UpdateProductName_Entry.get(), self.UpdateCategory_Entry.get(),
                   self.UpdateSubCategory_Entry.get(), self.UpdateQuantity_Entry.get(), self.UpdateMRP_Entry.get(),
                   self.UpdateCostPrice_Entry.get(), self.UpdateVendorNum_Entry.get())
            self.treeview_1.item(self.selected_item, values=val)
            self.update_treeview_1_database(ProductID=val[0], name=val[1], category=val[2], subcategory=val[3],
                                            qty=val[4], mrp=val[5], costPrice=val[6], vendorNum=val[7])
            Messagebox.show_info('Updated', '', self.Updateadd_ProductTk)

    def command_for_addProduct_button(self):
        if self.ProductName_Entry.get() == '' or self.Category_Entry.get() == '' or self.SubCategory_Entry.get() == '' or self.Quantity_Entry.get() == '' or self.MRP_Entry.get() == '' or self.CostPrice_Entry.get() == '' or self.VendorNum_Entry.get() == '':
            Messagebox.show_warning('Empty Box', '', self.F1)
        else:
            data = self.ADD_inventory_to_database()

            self.treeview_1.insert('', 0, values=(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], 'UPDATE', 'DEL'))
            Messagebox.show_info('Added', '', self.F1)

    def ADD_inventory_to_database(self):
        responce = connect_to_built_database(self.database_name)
        con, db = responce[0], responce[1]
        productId = GetRandom('PDT')
        con.execute(
            'insert into Inventory_1(productId,name, category,subcategory,qty,mrp,costPrice,vendorNum) values(?,?,?,?,?,?,?,?)',
            (productId, self.ProductName_Entry.get(),
             self.Category_Entry.get(),
             self.SubCategory_Entry.get(),
             self.Quantity_Entry.get(),
             self.MRP_Entry.get(),
             self.CostPrice_Entry.get(),
             self.VendorNum_Entry.get()))
        db.commit()
        db.close()
        return productId, self.ProductName_Entry.get(), self.Category_Entry.get(), self.SubCategory_Entry.get(), self.Quantity_Entry.get(), self.MRP_Entry.get(), self.CostPrice_Entry.get(), self.VendorNum_Entry.get()

    def Data_inserted_into_treeview_1(self):
        data = self.Fetch_data_by_database('Inventory_1')
        if data != []:
            for i in data:
                self.treeview_1.insert('', 0, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

    def delete_treeview_1_row(self):
        self.delete_selected_row(self.treeview_1, 'Inventory_1')

    def update_treeview_1_row(self):
        try:
            self.selected_item = self.treeview_1.selection()[0]

            val = self.treeview_1.item(self.selected_item)['values']
            self.productID = val[0]
            self.update_new_product(ProductName=val[1], Category=val[2], SubCategory=val[3], Quantity=val[4],
                                    MRP=val[5], CostPrice=val[6], VendorNum=val[7])
        except:
            Messagebox.show_warning('Select a row', '', self.Admin_panel)

    def delete_all_treeview_1_data(self):

        g = Messagebox.show_question('Do you want to delete all data ?', '', self.Admin_panel)
        if g == 'Yes':
            self.delete_all_treeview_data(self.treeview_1)
            self.delete_all_data_from_database('Inventory_1')

    def callback_treeview_1(self, sv):
        self.search(sv.get(), self.treeview_1)

    def update_treeview_1_database(self, ProductID, name, category, subcategory, qty, mrp, costPrice, vendorNum):
        data = connect_to_built_database(self.database_name)
        con, db = data[0], data[1]
        val = tuple(map(str, [ProductID, name, category, subcategory, qty, mrp, costPrice, vendorNum, ProductID]))
        con.execute(
            f'UPDATE Inventory_1 SET productId=?,name=?, category=?,subcategory=?,qty=?,mrp=?,costPrice=?,vendorNum=? where productId=?;',
            val)
        db.commit()
        db.close()

    # employee
    def treeview_for_employee(self):
        self.scroll = ttk.Scrollbar(self.frame2_3, bootstyle="round", orient=VERTICAL)
        self.scroll.pack(side=RIGHT, fill=Y)
        headings = ['Employee ID', 'Name', 'Contect No.', 'Address', 'Aadhar No.', 'Password', 'Designation']
        columns = [1, 2, 3, 4, 5, 6, 7]
        self.treeview_2 = ttk.Treeview(self.frame2_3, columns=columns, show='headings', bootstyle=INFO,
                                       xscrollcommand=self.scroll)

        self.treeview_2.column(1, anchor=CENTER, width=100)
        self.treeview_2.column(2, anchor=CENTER, width=100)
        self.treeview_2.column(3, anchor=CENTER, width=100)
        self.treeview_2.column(4, anchor=CENTER, width=100)
        self.treeview_2.column(5, anchor=CENTER, width=100)
        self.treeview_2.column(6, anchor=CENTER, width=100)
        self.treeview_2.column(7, anchor=CENTER, width=100)

        self.treeview_2.heading(columns[0], text=headings[0])
        self.treeview_2.heading(columns[1], text=headings[1])
        self.treeview_2.heading(columns[2], text=headings[2])
        self.treeview_2.heading(columns[3], text=headings[3])
        self.treeview_2.heading(columns[4], text=headings[4])
        self.treeview_2.heading(columns[5], text=headings[5])
        self.treeview_2.heading(columns[6], text=headings[6])
        self.treeview_2.pack(side=TOP, fill=BOTH, expand=True)
        self.Data_inserted_into_treeview_2()

    def command_for_emp_button(self):
        self.emp_button.configure(bootstyle=INFO)
        self.invoice_button.configure(bootstyle=PRIMARY)
        self.inventory_button.configure(bootstyle=PRIMARY)
        self.setting_button.configure(bootstyle=PRIMARY)
        self.delete_pre_frame()
        self.employee_management()

    def add_new_employee(self):
        self.add_employeeTk = ttk.Toplevel()
        self.add_employeeTk.title('Add Employee')
        self.add_employeeTk.geometry('700x500+200+50')
        self.add_employeeTk.iconbitmap('icon\\main.ico')

        self.F1 = ttk.Frame(self.add_employeeTk)
        self.F1.pack(side=TOP, fill=BOTH, expand=True)

        x = 100
        y = 50
        DiffX = 100
        DiffY = 50
        width = 40
        EntryX = 250

        self.EmployeeName_Label = ttk.Label(self.F1, text='Employee Name', takefocus=0)
        self.EmployeeName_Label.place(x=x, y=y)
        self.EmployeeName_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.EmployeeName_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.Contact_Label = ttk.Label(self.F1, text='Contact No.', takefocus=0)
        self.Contact_Label.place(x=x, y=y)
        self.Contact_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.Contact_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.Address_Label = ttk.Label(self.F1, text='Address', takefocus=0)
        self.Address_Label.place(x=x, y=y)
        self.Address_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.Address_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.Aadhaar_Label = ttk.Label(self.F1, text='Aadhaar No.', takefocus=0)
        self.Aadhaar_Label.place(x=x, y=y)
        self.Aadhaar_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.Aadhaar_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.Password_Label = ttk.Label(self.F1, text='Password', takefocus=0)
        self.Password_Label.place(x=x, y=y)
        self.Password_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.Password_Entry.place(x=EntryX, y=y)

        x = DiffX
        y += DiffY
        self.Designation_Label = ttk.Label(self.F1, text='Designation', takefocus=0)
        self.Designation_Label.place(x=x, y=y)
        self.Designation_Entry = ttk.Entry(self.F1, bootstyle=DARK, width=width)
        self.Designation_Entry.place(x=EntryX, y=y)

        self.add_Buttn = ttk.Button(self.F1, bootstyle=SUCCESS, padding=8,
                                    cursor='hand2', takefocus=0, text='ADD', width=15,
                                    command=self.command_for_addEmployee_button)
        self.add_Buttn.place(x=250, y=y + 70)

        self.add_employeeTk.resizable(0, 0)
        self.add_employeeTk.mainloop()

    def update_new_employee(self, EmployeeName, Contact, Address, Aadhar, Password, Designation):
        self.Updateadd_employeeTk = ttk.Toplevel()
        self.Updateadd_employeeTk.title('Update Employee')
        self.Updateadd_employeeTk.geometry('700x500+200+50')
        self.Updateadd_employeeTk.iconbitmap('icon\\main.ico')

        self.UpdateF1 = ttk.Frame(self.Updateadd_employeeTk)
        self.UpdateF1.pack(side=TOP, fill=BOTH, expand=True)

        x = 100
        y = 50
        DiffX = 100
        DiffY = 50
        width = 40
        EntryX = 250

        self.UpdateEmployeeName_Label = ttk.Label(self.UpdateF1, text='Employee Name', takefocus=0)
        self.UpdateEmployeeName_Label.place(x=x, y=y)
        self.UpdateEmployeeName_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateEmployeeName_Entry.place(x=EntryX, y=y)
        self.UpdateEmployeeName_Entry.insert(0, EmployeeName)

        x = DiffX
        y += DiffY
        self.UpdateContact_Label = ttk.Label(self.UpdateF1, text='Contact No.', takefocus=0)
        self.UpdateContact_Label.place(x=x, y=y)
        self.UpdateContact_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateContact_Entry.place(x=EntryX, y=y)
        self.UpdateContact_Entry.insert(0, Contact)

        x = DiffX
        y += DiffY
        self.UpdateAddress_Label = ttk.Label(self.UpdateF1, text='Address', takefocus=0)
        self.UpdateAddress_Label.place(x=x, y=y)
        self.UpdateAddress_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateAddress_Entry.place(x=EntryX, y=y)
        self.UpdateAddress_Entry.insert(0, Address)

        x = DiffX
        y += DiffY
        self.UpdateAadhaar_Label = ttk.Label(self.UpdateF1, text='Aadhaar No.', takefocus=0)
        self.UpdateAadhaar_Label.place(x=x, y=y)
        self.UpdateAadhaar_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateAadhaar_Entry.place(x=EntryX, y=y)
        self.UpdateAadhaar_Entry.insert(0, Aadhar)

        x = DiffX
        y += DiffY
        self.UpdatePassword_Label = ttk.Label(self.UpdateF1, text='Password', takefocus=0)
        self.UpdatePassword_Label.place(x=x, y=y)
        self.UpdatePassword_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdatePassword_Entry.place(x=EntryX, y=y)
        self.UpdatePassword_Entry.insert(0, Password)

        x = DiffX
        y += DiffY
        self.UpdateDesignation_Label = ttk.Label(self.UpdateF1, text='Designation', takefocus=0)
        self.UpdateDesignation_Label.place(x=x, y=y)
        self.UpdateDesignation_Entry = ttk.Entry(self.UpdateF1, bootstyle=DARK, width=width)
        self.UpdateDesignation_Entry.place(x=EntryX, y=y)
        self.UpdateDesignation_Entry.insert(0, Designation)

        self.Update_Buttn = ttk.Button(self.UpdateF1, bootstyle=SUCCESS, padding=8,
                                       cursor='hand2', takefocus=0, text='UPDATE', width=15,
                                       command=self.command_for_updateEmployee_button)
        self.Update_Buttn.place(x=250, y=y + 70)

        self.Updateadd_employeeTk.resizable(0, 0)
        self.Updateadd_employeeTk.mainloop()

    def ADD_employee_to_database(self):
        responce = connect_to_database()
        con, db = responce[0], responce[1]
        EmpID = GetRandom('EMP')
        con.execute(
            'insert into Employee_cred(admin_Id,empId,name, contact,address,aadhar,password ,designation) values(?,?,?,?,?,?,?,?)',
            (self.database_name, EmpID, self.EmployeeName_Entry.get(),
             self.Contact_Entry.get(),
             self.Address_Entry.get(),
             self.Aadhaar_Entry.get(),
             self.Password_Entry.get(),
             self.Designation_Entry.get()))
        db.commit()
        db.close()
        return EmpID, self.EmployeeName_Entry.get(), self.Contact_Entry.get(), self.Address_Entry.get(), self.Aadhaar_Entry.get(), self.Password_Entry.get(), self.Designation_Entry.get()

    def command_for_updateEmployee_button(self):
        if self.UpdateEmployeeName_Entry.get() == '' or self.UpdateContact_Entry.get() == '' or self.UpdateAddress_Entry.get() == '' \
                or self.UpdateAadhaar_Entry.get() == '' or self.UpdatePassword_Entry.get() == '' or self.UpdateDesignation_Entry.get() == '':
            Messagebox.show_warning('Empty Box', '', self.UpdateF1)
        else:
            val = (self.emp_TD, self.UpdateEmployeeName_Entry.get(), self.UpdateContact_Entry.get(),
                   self.UpdateAddress_Entry.get(), self.UpdateAadhaar_Entry.get(), self.UpdatePassword_Entry.get(),
                   self.UpdateDesignation_Entry.get())
            self.treeview_2.item(self.selected_item, values=val)
            self.update_treeview_2_database(empId=val[0], name=val[1], contact=val[2], address=val[3], aadhar=val[4],
                                            password=val[5], designation=val[6])
            Messagebox.show_info('Updated', '', self.Updateadd_employeeTk)

    def command_for_addEmployee_button(self):
        if self.EmployeeName_Entry.get() == '' or self.Contact_Entry.get() == '' or self.Address_Entry.get() == '' or self.Aadhaar_Entry.get() == '' or self.Password_Entry.get() == '' or self.Designation_Entry.get() == '':
            Messagebox.show_warning('Empty Box', '', self.F1)
        else:
            data = self.ADD_employee_to_database()
            self.treeview_2.insert('', 0, values=(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

    def employee_management(self):
        self.frame2_1 = tk.Frame(self.frame3, background='white')
        self.frame2_1.pack(side=TOP, fill=X)

        self.label = tk.Label(self.frame3, height=2)
        self.label.pack(side=TOP, fill=X)

        self.frame2_2 = tk.Frame(self.frame3, background='white')
        self.frame2_2.pack(side=TOP, fill=X)

        self.frame2_3 = tk.Frame(self.frame3, background='white', highlightthickness=20, highlightbackground='white',
                                 highlightcolor='white')
        self.frame2_3.pack(side=TOP, fill=BOTH, expand=True)
        self.label2 = tk.Label(self.frame2_1, text='Employee Managment', bg='white', font=('calibri', 17, 'bold'))
        self.label2.pack(side=TOP, fill=X)

        self.sep2 = tk.Label(self.frame2_2, text='', width=2)
        self.sep2.pack(side=LEFT, fill=Y)

        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback_treeview_2(sv))

        self.search_box2 = ttk.Entry(self.frame2_2, bootstyle=DARK, width=30, textvariable=sv)
        self.search_box2.pack(side=LEFT, fill=Y)

        self.searchBar_image2 = ttk.PhotoImage(file='images\\searchBar.png')
        self.searchBar_img_label2 = ttk.Label(self.frame2_2, image=self.searchBar_image2, background='white')
        self.searchBar_img_label2.pack(side=LEFT, fill=Y)
        ToolTip(
            self.searchBar_img_label2,
            text="Search the Data.",
        )

        self.sep2_1 = tk.Label(self.frame2_2, text='', width=2)
        self.sep2_1.pack(side=RIGHT, fill=Y)

        self.add_image2 = ttk.PhotoImage(file='images\\add.png')
        self.add_img_label2 = ttk.Button(self.frame2_2, image=self.add_image2, bootstyle=LIGHT, padding=0,
                                         cursor='hand2', takefocus=0, command=self.add_new_employee)
        self.add_img_label2.pack(side=RIGHT, fill=Y)
        ToolTip(
            self.add_img_label2,
            text="Add Data to the Table.",
        )

        self.sep2_2 = tk.Label(self.frame2_2, text='', width=1)
        self.sep2_2.pack(side=RIGHT, fill=Y)

        self.minus_image2 = ttk.PhotoImage(file='images\\minus.png')
        self.minus_img_label2 = ttk.Button(self.frame2_2, image=self.minus_image2, bootstyle=LIGHT, padding=0,
                                           cursor='hand2', takefocus=0, command=self.delete_treeview_2_row)
        self.minus_img_label2.pack(side=RIGHT, fill=Y)
        ToolTip(
            self.minus_img_label2,
            text="Delete selected data from the table.",
        )

        self.sep2_3 = tk.Label(self.frame2_2, text='', width=2)
        self.sep2_3.pack(side=RIGHT, fill=Y)

        self.update_image2 = ttk.PhotoImage(file='images\\update.png')
        self.update_img_label2 = ttk.Button(self.frame2_2, image=self.update_image2, bootstyle=LIGHT, padding=0,
                                            cursor='hand2', takefocus=0, command=self.update_treeview_2_row)
        self.update_img_label2.pack(side=RIGHT, fill=Y)
        ToolTip(
            self.update_img_label2,
            text="Update selected data.",
        )

        self.sep2_4 = tk.Label(self.frame2_2, text='', width=1)
        self.sep2_4.pack(side=RIGHT, fill=Y)

        self.delete_all_image2 = ttk.PhotoImage(file='images\\delete.png')
        self.delete_all_img_label2 = ttk.Button(self.frame2_2, image=self.delete_all_image2, bootstyle=LIGHT, padding=0,
                                                cursor='hand2', takefocus=0, command=self.delete_all_treeview_2_data)
        self.delete_all_img_label2.pack(side=RIGHT, fill=Y)
        ToolTip(
            self.delete_all_img_label2,
            text="Delete All data from the table.",
        )
        self.treeview_for_employee()

    def callback_treeview_2(self, sv):
        self.search(sv.get(), self.treeview_2)

    def delete_treeview_2_row(self):
        self.delete_selected_row(self.treeview_2, 'Employee')

    def update_treeview_2_row(self):
        try:
            self.selected_item = self.treeview_2.selection()[0]

            val = self.treeview_2.item(self.selected_item)['values']
            self.emp_TD = val[0]
            self.update_new_employee(EmployeeName=val[1], Contact=val[2], Address=val[3], Aadhar=val[4],
                                     Password=val[5], Designation=val[6])
        except:
            Messagebox.show_warning('Select a row', '', self.Admin_panel)

    def delete_all_treeview_2_data(self):

        g = Messagebox.show_question('Do you want to delete all data ?', '', self.Admin_panel)
        if g == 'Yes':
            self.delete_all_treeview_data(self.treeview_2)
            self.delete_all_data_from_database('Employee')

    def Data_inserted_into_treeview_2(self):
        data = self.Fetch_data_by_database('Employee')
        if data != []:
            for i in data:
                self.treeview_2.insert('', 0, values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

    def update_treeview_2_database(self, empId, name, contact, address, aadhar, password, designation):
        data = connect_to_built_database(self.database_name)
        con, db = data[0], data[1]
        val = tuple(map(str, [empId, name, contact, address, aadhar, password, designation, empId, self.database_name]))
        con.execute(
            f'UPDATE Employee_cred SET empId=?,name=?,contact=?,address=?,aadhar=?,password=?,designation=? where empId=? and admin_Id=?;',
            val)
        db.commit()
        db.close()

    # invoices
    def invoices_management(self):
        self.frame2_1 = tk.Frame(self.frame3, background='white')
        self.frame2_1.pack(side=TOP, fill=X)

        self.label = tk.Label(self.frame3, height=2)
        self.label.pack(side=TOP, fill=X)

        self.frame2_2 = tk.Frame(self.frame3, background='white')
        self.frame2_2.pack(side=TOP, fill=X)

        self.frame2_3 = tk.Frame(self.frame3, background='white', highlightthickness=20, highlightbackground='white',
                                 highlightcolor='white')
        self.frame2_3.pack(side=TOP, fill=BOTH, expand=True)
        self.label3 = tk.Label(self.frame2_1, text='Invoices', bg='white', font=('calibri', 17, 'bold'))
        self.label3.pack(side=TOP, fill=X)

        self.sep3 = tk.Label(self.frame2_2, text='', width=2)
        self.sep3.pack(side=LEFT, fill=Y)

        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback_treeview_3(sv))

        self.search_box3 = ttk.Entry(self.frame2_2, bootstyle=DARK, width=30, textvariable=sv)
        self.search_box3.pack(side=LEFT, fill=Y)

        self.searchBar_image3 = ttk.PhotoImage(file='images\\searchBar.png')
        self.searchBar_img_label3 = ttk.Label(self.frame2_2, image=self.searchBar_image3, background='white')
        self.searchBar_img_label3.pack(side=LEFT, fill=Y)
        ToolTip(
            self.searchBar_img_label3,
            text="Search the Data.",
        )

        self.sep3_1 = tk.Label(self.frame2_2, text='', width=1)
        self.sep3_1.pack(side=RIGHT, fill=Y)

        self.minus_image3 = ttk.PhotoImage(file='images\\minus.png')
        self.minus_img_label3 = ttk.Button(self.frame2_2, image=self.minus_image3, bootstyle=LIGHT, padding=0,
                                           cursor='hand2', takefocus=0, command=self.delete_treeview_3_row)
        self.minus_img_label3.pack(side=RIGHT, fill=Y)
        ToolTip(
            self.minus_img_label3,
            text="Delete selected data.",
        )

        self.sep3_2 = tk.Label(self.frame2_2, text='', width=1)
        self.sep3_2.pack(side=RIGHT, fill=Y)

        self.delete_all_image3 = ttk.PhotoImage(file='images\\delete.png')
        self.delete_all_img_label3 = ttk.Button(self.frame2_2, image=self.delete_all_image3, bootstyle=LIGHT, padding=0,
                                                cursor='hand2', takefocus=0, command=self.delete_all_treeview_3_data)
        self.delete_all_img_label3.pack(side=RIGHT, fill=Y)
        ToolTip(
            self.delete_all_img_label3,
            text="Delete All data from the table.",
        )
        self.treeview_for_invoices()

    def command_for_invoice_button(self):
        self.invoice_button.configure(bootstyle=INFO)
        self.inventory_button.configure(bootstyle=PRIMARY)
        self.emp_button.configure(bootstyle=PRIMARY)
        self.setting_button.configure(bootstyle=PRIMARY)
        self.delete_pre_frame()
        self.invoices_management()

    def treeview_for_invoices(self):
        self.scroll = ttk.Scrollbar(self.frame2_3, bootstyle="round", orient=VERTICAL)
        self.scroll.pack(side=RIGHT, fill=Y)
        headings = ['Bill Number', 'Date', 'Customer Name', 'Contact Number']
        columns = [1, 2, 3, 4]
        self.treeview_3 = ttk.Treeview(self.frame2_3, columns=columns, show='headings', bootstyle=INFO,
                                       xscrollcommand=self.scroll)

        self.treeview_3.column(1, anchor=CENTER, width=100)
        self.treeview_3.column(2, anchor=CENTER, width=100)
        self.treeview_3.column(3, anchor=CENTER, width=100)
        self.treeview_3.column(4, anchor=CENTER, width=100)

        self.treeview_3.heading(columns[0], text=headings[0])
        self.treeview_3.heading(columns[1], text=headings[1])
        self.treeview_3.heading(columns[2], text=headings[2])
        self.treeview_3.heading(columns[3], text=headings[3])
        self.treeview_3.pack(side=LEFT, fill=BOTH, expand=True)
        self.treeview_3.bind('<Double-1>', self.open_invoice)
        self.Data_inserted_into_treeview_3()

    def callback_treeview_3(self, sv):
        self.search(sv.get(), self.treeview_3)

    def delete_treeview_3_row(self):
        self.delete_selected_row(self.treeview_3, 'Invoices')

    def delete_all_treeview_3_data(self):

        g = Messagebox.show_question('Do you want to delete all data ?', '', self.Admin_panel)
        if g == 'Yes':
            self.delete_all_treeview_data(self.treeview_3)
            self.delete_all_data_from_database('Invoices')

    def Data_inserted_into_treeview_3(self):
        data = self.Fetch_data_by_database('Invoices')
        if data != []:
            for i in data:
                self.treeview_3.insert('', 0, values=(i[0], i[1], i[2], i[3]))

    def open_invoice(self, event):
        self.open_invoiceTk = tk.Toplevel(self.frame2_3)
        self.open_invoiceTk.title('Invoice')
        self.open_invoiceTk.configure(bg='#F4F4F4')
        self.open_invoiceTk.geometry('600x500+200+50')
        self.open_invoiceTk.iconbitmap('icon\\main.ico')
        item = self.treeview_3.selection()[0]
        result = self.treeview_3.item(item)['values']
        data = self.fetch_productDetails_by_id(str(result[0]))
        self.Openbill_window()
        self.data_add_to_bill(data, result[0], result[1], result[2], result[3])
        self.open_invoiceTk.mainloop()

    def Openbill_window(self):
        self.Frame = tk.Frame(self.open_invoiceTk, highlightthickness=20, highlightbackground='white',
                              highlightcolor='white')
        self.Frame.pack(side=TOP, fill=BOTH, expand=True)
        res = self.fetch_stor_details()
        if res != '':
            name = res[0]
            location = res[1]
            telephon = res[2]
            helpline = res[3]
            emailid = res[4]
        else:
            name = 'XYZ Retail Ltd.'
            location = 'Ghaziabad-201002'
            telephon = '022-298766986'
            helpline = '1800-200-255'
            emailid = 'niru@gmail.com'

        self.label1 = ttk.Label(self.Frame, text=name, anchor=CENTER)
        self.label1.pack(side=TOP, fill=X)
        self.label2 = ttk.Label(self.Frame, text=location, anchor=CENTER)
        self.label2.pack(side=TOP, fill=X)
        self.label3 = ttk.Label(self.Frame, text=f'Telephone No. : {telephon}', anchor=CENTER)
        self.label3.pack(side=TOP, fill=X)
        self.label4 = ttk.Label(self.Frame, text=f'Help Line No. : {helpline}', anchor=CENTER)
        self.label4.pack(side=TOP, fill=X)
        self.label5 = ttk.Label(self.Frame, text=f'Email ID : {emailid}', anchor=CENTER)
        self.label5.pack(side=TOP, fill=X)

        self.sep = tk.Label(self.Frame, text='', height=1)
        self.sep.pack(side=TOP, fill=X)

        self.Frame1 = tk.Frame(self.Frame, bg='red')
        self.Frame1.pack(side=TOP, fill=X)
        width = 15

        self.label6 = ttk.Label(self.Frame1, text='Bill Number : ', width=width)
        self.label6.pack(side=LEFT, fill=X)
        self.label7 = ttk.Label(self.Frame1, text='')
        self.label7.pack(side=LEFT, fill=X)
        self.label9 = ttk.Label(self.Frame1, text='')
        self.label9.pack(side=RIGHT, fill=X)
        self.label10 = ttk.Label(self.Frame1, text='Phone Number : ', width=width)
        self.label10.pack(side=RIGHT, fill=X)

        self.Frame2 = tk.Frame(self.Frame)
        self.Frame2.pack(side=TOP, fill=X)
        self.label11 = ttk.Label(self.Frame2, text='Customer Name : ', width=width)
        self.label11.pack(side=LEFT, fill=X)
        self.label12 = ttk.Label(self.Frame2, text='')
        self.label12.pack(side=LEFT, fill=X)
        self.label13 = ttk.Label(self.Frame2, text='')
        self.label13.pack(side=RIGHT, fill=X)
        self.label14 = ttk.Label(self.Frame2, text='Date : ', width=width)
        self.label14.pack(side=RIGHT, fill=X)
        self.Frame3 = tk.Frame(self.Frame)
        self.Frame3.pack(side=TOP, fill=BOTH, expand=True)
        self.Openbill_treeview(self.Frame3)
        self.Frame4 = tk.Frame(self.Frame)
        self.Frame4.pack(side=TOP, fill=BOTH, expand=True)
        self.open_btn = ttk.Button(self.Frame4, bootstyle=(SUCCESS), padding=5,
                                   cursor='hand2', takefocus=0, text='Open as pdf', width=14,command=self.open_pdf_)
        self.open_btn.pack(side=LEFT, fill=X)

    def open_pdf_(self):
        if self.bill_id != '':
            path = rf'invoices_pdf\{self.bill_id + ".pdf"}'
            os.system(path)

    def fetch_stor_details(self):
        result = ''
        data = connect_to_built_database(self.database_name)
        cur, db = data[0], data[1]
        r = cur.execute('select * from store_details')
        for i in r:
            result = i
        db.commit()
        db.close()
        return result

    def Openbill_treeview(self, frame):
        self.sep = tk.Label(frame, text='', height=0)
        self.sep.pack(side=TOP, fill=X)
        self.se = ttk.Separator(frame, bootstyle="info")
        self.se.pack(side=TOP, fill=X)
        self.sep = tk.Label(frame, text='', height=0)
        self.sep.pack(side=TOP, fill=X)
        headings = ['Product Name', 'Quantity', 'Price']
        columns = [1, 2, 3]
        self.scroll___ = ttk.Scrollbar(frame, bootstyle="round", orient=VERTICAL)
        self.scroll___.pack(side=RIGHT, fill=Y)
        self.treeview = ttk.Treeview(frame, columns=columns, show='headings', bootstyle=LIGHT,
                                     yscrollcommand=self.scroll___)
        self.treeview.column(1, anchor='w', width=100)
        self.treeview.column(2, anchor='center', width=100)
        self.treeview.column(3, anchor='center', width=100)
        self.treeview.heading(columns[0], text=headings[0], anchor='w')
        self.treeview.heading(columns[1], text=headings[1], anchor='center')
        self.treeview.heading(columns[2], text=headings[2], anchor='center')
        self.treeview.pack(side=LEFT, fill=BOTH, expand=True)

    def data_add_to_bill(self, data, bill_id, date, Name, Contact):
        for i in data:
            val = i[1].split('|')
            self.treeview.insert('', END, values=(val[0], val[1], val[2]))
        self.label7.configure(text=str(bill_id))
        self.label9.configure(text=str(Contact))
        self.label12.configure(text=Name)
        self.label13.configure(text=date)
        self.bill_id=str(bill_id)

    def fetch_productDetails_by_id(self, id):
        responce = connect_to_built_database(self.database_name)
        con, db = responce[0], responce[1]
        data = con.execute('select * from productDetails where billNum=?', (id,))
        result = []
        for i in data:
            result.append(i)
        db.commit()
        db.close()
        return result

    def search(self, query, tree):

        selections = []
        for child in tree.get_children():
            if query in list(map(str, tree.item(child)['values'])):  # compare strings in  lower cases.
                selections.append(child)
        tree.selection_set(selections)

    def username_(self, name):
        self.username_label = ttk.Label(self.frame1, text=name, width=28, bootstyle="inverse", compound='center')
        self.username_label.pack(side=TOP, fill=X, ipadx=15, ipady=5)

    def Fetch_data_by_database(self, tableName):
        if tableName != 'Employee':
            responce = connect_to_built_database(self.database_name)
            con, db = responce[0], responce[1]
            data = con.execute(f'select * from {tableName}')
            result = []
            for i in data:
                result.append(i)
            db.commit()
            db.close()
            return result
        elif tableName == 'Employee':
            responce = connect_to_database()
            con, db = responce[0], responce[1]
            data = con.execute(f'select * from Employee_cred where admin_Id=?', (self.database_name,))
            result = []
            for i in data:
                result.append(i)
            db.commit()
            db.close()
            return result

    def Delete_Data_from_database(self, tableName):
        responce = connect_to_built_database(self.database_name)
        con, db = responce[0], responce[1]
        con.execute(f'delete from {tableName}')
        db.commit()
        db.close()

    def delete_selected_row(self, tree, con1):
        try:
            selected_item = tree.selection()[0]
            con2 = tree.item(selected_item)['values'][0]
            tree.delete(selected_item)
            self.delete_selected_row_from_database(con1, con2)
        except:
            Messagebox.show_warning('Select a row', '', self.Admin_panel)

    def delete_all_treeview_data(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def delete_selected_row_from_database(self, con1, con2):
        if con1 != 'Employee':
            data = connect_to_built_database(self.database_name)
            cur, db = data[0], data[1]
            if con1 == 'Inventory_1':
                cur.execute(f'delete from Inventory_1 where productId=?;', (str(con2),))

            elif con1 == 'Invoices':
                cur.execute(f'delete from Invoices where biilNum=?;', (str(con2),))
            db.commit()
            db.close()
        elif con1 == 'Employee':
            data = connect_to_database()
            cur, db = data[0], data[1]
            cur.execute(f'delete from Employee_cred where empId=? and admin_Id=?;',
                        (str(con2), str(self.database_name)))
            db.commit()
            db.close()

    def delete_all_data_from_database(self, con1):
        if con1 != 'Employee':
            data = connect_to_built_database(self.database_name)
            cur, db = data[0], data[1]
            if con1 == 'Inventory_1':
                cur.execute(f'delete from Inventory_1;')

            elif con1 == 'Invoices':
                cur.execute(f'delete from Invoices;')
            db.commit()
            db.close()
        elif con1 == 'Employee':
            data = connect_to_database()
            cur, db = data[0], data[1]
            cur.execute(f'delete from Employee_cred;')
            db.commit()
            db.close()

    # setting
    def setting(self):
        self.frame2_1 = tk.Frame(self.frame3, background='white')
        self.frame2_1.pack(side=TOP, fill=X)

        self.label = tk.Label(self.frame3, height=2)
        self.label.pack(side=TOP, fill=X)

        self.frame2_2 = tk.Frame(self.frame3, background='white')
        self.frame2_2.pack(side=TOP, fill=X)

        self.frame2_3 = tk.Frame(self.frame3, background='white', highlightthickness=20, highlightbackground='white',
                                 highlightcolor='white')
        self.frame2_3.pack(side=TOP, fill=BOTH, expand=True)
        self.label4 = tk.Label(self.frame2_1, text='Settings', bg='gray', font=('calibri', 17, 'bold'))
        self.label4.pack(side=TOP, fill=X)

        self.F1 = ttk.Frame(self.frame2_2, bootstyle=DEFAULT)
        self.F1.pack(side=TOP, fill=BOTH, expand=True)

        self.F3 = ttk.Frame(self.F1, bootstyle=LIGHT)
        self.F3.pack(side=TOP, fill=BOTH, expand=True)

        self.F3_1 = ttk.Frame(self.F3, bootstyle=LIGHT)
        self.F3_1.pack(side=LEFT, fill=X, expand=True)

        self.change_your_password = ttk.Label(self.F3_1, text='Change Your Password', compound=LEFT,
                                              background='#F8F9FA')
        self.change_your_password.pack(side=TOP, fill=X, padx=30, pady=10)

        self.sep__1 = ttk.Frame(self.F3_1, bootstyle=INFO)
        self.sep__1.pack(side=TOP, fill=X, padx=30)
        self.sep_l1 = ttk.Label(self.F3_1, text='', compound=LEFT, background='#F8F9FA')
        self.sep_l1.pack(side=TOP, fill=X, padx=30)

        self.F3_1_1 = ttk.Frame(self.F3_1, bootstyle=LIGHT)
        self.F3_1_1.pack(side=TOP, fill=X)
        self.F3_1_2 = ttk.Frame(self.F3_1, bootstyle=LIGHT)
        self.F3_1_2.pack(side=TOP, fill=X)
        self.F3_1_3 = ttk.Frame(self.F3_1, bootstyle=LIGHT)
        self.F3_1_3.pack(side=TOP, fill=X)
        self.F3_1_4 = ttk.Frame(self.F3_1, bootstyle=LIGHT)
        self.F3_1_4.pack(side=TOP, fill=X)

        self.C_password = ttk.Label(self.F3_1_1, text='Current Password  ', compound=LEFT, background='#F8F9FA')
        self.C_password.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.N_password = ttk.Label(self.F3_1_2, text='New Password      ', compound=LEFT, background='#F8F9FA')
        self.N_password.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.Con_password = ttk.Label(self.F3_1_3, text='Confirm Password', compound=LEFT, background='#F8F9FA')
        self.Con_password.pack(side=LEFT, fill=X, padx=30, pady=11)

        self.C_password_entry = ttk.Entry(self.F3_1_1, bootstyle=DARK, width=30)
        self.C_password_entry.pack(side=LEFT, fill=X)
        self.N_password_entry = ttk.Entry(self.F3_1_2, bootstyle=DARK, width=30)
        self.N_password_entry.pack(side=LEFT, fill=X)
        self.Con_password_entry = ttk.Entry(self.F3_1_3, bootstyle=DARK, width=30)
        self.Con_password_entry.pack(side=LEFT, fill=X)

        self.pass_save = ttk.Button(self.F3_1_4, bootstyle=(INFO), padding=0,
                                    cursor='hand2', takefocus=0, text='CHANGE',
                                    command=self.command_for_save_chang_pass)
        self.pass_save.pack(side=LEFT, fill=Y, padx=30, ipady=4, ipadx=10, pady=20)

        self.F3_2 = ttk.Frame(self.F3, bootstyle=LIGHT)
        self.F3_2.pack(side=RIGHT, fill=BOTH, expand=True)

        self.change_your_email = ttk.Label(self.F3_2, text='Set your email', compound=LEFT, background='#F8F9FA')
        self.change_your_email.pack(side=TOP, fill=X, padx=30, pady=10)
        ToolTip(
            self.change_your_email,
            text="Used to send Invoice on customer mail.",
        )
        self.sep__2 = ttk.Frame(self.F3_2, bootstyle=INFO)
        self.sep__2.pack(side=TOP, fill=X, padx=30)
        self.sep_l2 = ttk.Label(self.F3_2, text='', compound=LEFT, background='#F8F9FA')
        self.sep_l2.pack(side=TOP, fill=X, padx=30)
        self.F3_2_1 = ttk.Frame(self.F3_2, bootstyle=LIGHT)
        self.F3_2_1.pack(side=TOP, fill=X)
        self.F3_2_2 = ttk.Frame(self.F3_2, bootstyle=LIGHT)
        self.F3_2_2.pack(side=TOP, fill=X)
        self.F3_2_3 = ttk.Frame(self.F3_2, bootstyle=LIGHT)
        self.F3_2_3.pack(side=BOTTOM, fill=X)

        self.email_l = ttk.Label(self.F3_2_1, text='Email       ', compound=LEFT, background='#F8F9FA')
        self.email_l.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.email_entry = ttk.Entry(self.F3_2_1, bootstyle=DARK, width=30)
        self.email_entry.pack(side=LEFT, fill=X)

        self.email_pass_l = ttk.Label(self.F3_2_2, text='Password ', compound=LEFT, background='#F8F9FA')
        self.email_pass_l.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.email_pass_entry = ttk.Entry(self.F3_2_2, bootstyle=DARK, width=30)
        self.email_pass_entry.pack(side=LEFT, fill=X)
        self.mail_save = ttk.Button(self.F3_2_3, bootstyle=INFO, padding=0,
                                    cursor='hand2', takefocus=0, text='SAVE', command=self.command_for_save_email_pass)
        self.mail_save.pack(side=LEFT, fill=Y, padx=30, ipady=4, ipadx=20, pady=20)

        self.F4 = ttk.Frame(self.F1, bootstyle=LIGHT)
        self.F4.pack(side=TOP, fill=X)

        self.F4__1 = ttk.Frame(self.F4, bootstyle=LIGHT)
        self.F4__1.pack(side=LEFT, fill=X, expand=True)

        self.change_your_stor = ttk.Label(self.F4__1, text='Change Your Store Details', compound=LEFT,
                                          background='#F8F9FA')
        self.change_your_stor.pack(side=TOP, fill=X, padx=30, pady=10)
        ToolTip(
            self.change_your_stor,
            text="Details will be shown in invoice.",
        )

        self.sep__3 = ttk.Frame(self.F4__1, bootstyle=INFO)
        self.sep__3.pack(side=TOP, fill=X, padx=30)
        self.sep_l3 = ttk.Label(self.F4__1, text='', compound=LEFT, background='#F8F9FA')
        self.sep_l3.pack(side=TOP, fill=X, padx=30)

        self.F4_1 = ttk.Frame(self.F4__1, bootstyle=LIGHT)
        self.F4_1.pack(side=TOP, fill=X)
        self.F4_2 = ttk.Frame(self.F4__1, bootstyle=LIGHT)
        self.F4_2.pack(side=TOP, fill=X)
        self.F4_3 = ttk.Frame(self.F4__1, bootstyle=LIGHT)
        self.F4_3.pack(side=TOP, fill=X)
        self.F4_4 = ttk.Frame(self.F4__1, bootstyle=LIGHT)
        self.F4_4.pack(side=TOP, fill=X)
        self.F4_5 = ttk.Frame(self.F4__1, bootstyle=LIGHT)
        self.F4_5.pack(side=TOP, fill=X)
        self.F4_6 = ttk.Frame(self.F4__1, bootstyle=LIGHT)
        self.F4_6.pack(side=BOTTOM, fill=X)

        self.stor_name_l = ttk.Label(self.F4_1, text='Name               ', compound=LEFT, background='#F8F9FA')
        self.stor_name_l.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.stor_name_entry = ttk.Entry(self.F4_1, bootstyle=DARK, width=30)
        self.stor_name_entry.pack(side=LEFT, fill=X)

        self.location_l = ttk.Label(self.F4_2, text='Location           ', compound=LEFT, background='#F8F9FA')
        self.location_l.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.location_entry = ttk.Entry(self.F4_2, bootstyle=DARK, width=30)
        self.location_entry.pack(side=LEFT, fill=X)

        self.Telephone_l = ttk.Label(self.F4_3, text='Telephone No. ', compound=LEFT, background='#F8F9FA')
        self.Telephone_l.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.Telephone_entry = ttk.Entry(self.F4_3, bootstyle=DARK, width=30)
        self.Telephone_entry.pack(side=LEFT, fill=X)

        self.helpline_l = ttk.Label(self.F4_4, text='Help Line No.   ', compound=LEFT, background='#F8F9FA')
        self.helpline_l.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.helpline_entry = ttk.Entry(self.F4_4, bootstyle=DARK, width=30)
        self.helpline_entry.pack(side=LEFT, fill=X)

        self.mailid_l = ttk.Label(self.F4_5, text='Email ID           ', compound=LEFT, background='#F8F9FA')
        self.mailid_l.pack(side=LEFT, fill=X, padx=30, pady=11)
        self.mail_entry = ttk.Entry(self.F4_5, bootstyle=DARK, width=30)
        self.mail_entry.pack(side=LEFT, fill=X)
        self.stor_save = ttk.Button(self.F4_6, bootstyle=INFO, padding=0,
                                    cursor='hand2', takefocus=0, text='CHANGE',
                                    command=self.command_for_save_stor_details)
        self.stor_save.pack(side=LEFT, fill=Y, padx=30, ipady=4, ipadx=20, pady=20)
        self.F4__2 = ttk.Frame(self.F4, bootstyle=LIGHT)
        self.F4__2.pack(side=RIGHT, fill=BOTH, expand=True)
        self.delete_accnt = ttk.Label(self.F4__2, text='Delete your account permanently', compound=LEFT,
                                      background='#F8F9FA')
        self.delete_accnt.pack(side=TOP, fill=X, padx=40, pady=10)
        self.sep__4 = ttk.Frame(self.F4__2, bootstyle=INFO)
        self.sep__4.pack(side=TOP, fill=X, padx=40)
        self.sep_l5 = ttk.Label(self.F4__2, text='', compound=LEFT, background='#F8F9FA')
        self.sep_l5.pack(side=TOP, fill=X, padx=40)

        self.F4__1_1 = ttk.Frame(self.F4__2, bootstyle=LIGHT)
        self.F4__1_1.pack(side=TOP, fill=X)
        self.F4__1_2 = ttk.Frame(self.F4__2, bootstyle=LIGHT)
        self.F4__1_2.pack(side=TOP, fill=X)
        self.email_delete_l = ttk.Label(self.F4__1_1, text='Email            ', compound=LEFT, background='#F8F9FA')
        self.email_delete_l.pack(side=LEFT, fill=X, padx=40, pady=11)
        self.email_delete_entry = ttk.Entry(self.F4__1_1, bootstyle=DARK, width=30)
        self.email_delete_entry.pack(side=LEFT, fill=X)
        self.delete_accnt_btn = ttk.Button(self.F4__1_2, bootstyle=DANGER, padding=0,
                                           cursor='hand2', takefocus=0, text='DELETE',
                                           command=self.command_for_delete_accnt)
        self.delete_accnt_btn.pack(side=RIGHT, fill=Y, padx=30, ipady=4, ipadx=20, pady=20)

    def command_for_delete_accnt(self):
        if self.email_delete_entry.get() == '':
            Messagebox.show_warning('Empty fields', '', self.Admin_panel)
        elif self.email_delete_entry.get() != self.database_name:
            Messagebox.show_error('Invalid Email ID', '', self.Admin_panel)
        else:
            info = Messagebox.okcancel('Your all data will be delete permanently', '', self.Admin_panel)
            if info == 'OK':
                utility.enable_high_dpi_awareness()
                self.result = Querybox.get_string("Enter your password", initialvalue='')
                if self.result != '':
                    try:
                        self.msg.pack_forget()
                    except:
                        pass
                    self.msg = ttk.Label(self.F4__1_2, text='Wait few seconds', compound=LEFT,
                                         background='#F8F9FA', bootstyle=DANGER)
                    self.msg.pack(side=RIGHT, fill=X, padx=40, pady=11)
                    res = self.check_admin_cred(self.database_name, self.result)
                    if res == '':
                        Messagebox.show_error('Incorrect Password', '', self.Admin_panel)
                    else:
                        self.delete_admin_cred_by_id_pass()
                        self.delete_all_admin_data()
                        insert_login_cred('N', '', '')
                        Messagebox.show_info('Successfully Deleted','',self.Admin_panel)
                        self.Admin_panel.destroy()
    def delete_all_admin_data(self):
        data = connect_to_built_database(self.database_name)
        cur, db = data[0], data[1]
        cur.execute('delete from Invoices')
        cur.execute('delete from productDetails')
        cur.execute('delete from sending_mail')
        cur.execute('delete from store_details')
        db.commit()
        db.close()

    def delete_admin_cred_by_id_pass(self):
        data = connect_to_database()
        cur, db = data[0], data[1]
        cur.execute('delete from admin_cred where id=? and pass=?', (self.database_name, self.result))
        db.commit()
        db.close()

    def check_admin_cred(self, id, passs):
        result = ''
        data = connect_to_database()
        cur, db = data[0], data[1]
        r = cur.execute('select id from admin_cred where id=? and pass=?', (id, passs))
        for i in r:
            result = i
        db.commit()
        db.close()
        return result

    def command_for_save_chang_pass(self):
        if self.C_password_entry.get() == '' or self.N_password_entry.get() == "" or self.Con_password_entry.get() == '':
            Messagebox.show_warning('Empty Fields', '', self.Admin_panel)
        elif self.N_password_entry.get() != self.Con_password_entry.get() and self.C_password_entry.get() != '':
            Messagebox.show_warning('New password and confirm password must be same.', '', self.Admin_panel)
        else:
            res = self.fetch_current_pass(self.database_name, self.C_password_entry.get())
            if res == '':
                Messagebox.show_error('Current password is incorrect', '', self.Admin_panel)
            else:
                self.update_password(self.Con_password_entry.get())
                Messagebox.show_info('Password changed successfully', '', self.Admin_panel)
                self.C_password_entry.insert(0, '')
                self.Con_password_entry.insert(0, '')
                self.N_password_entry.insert(0, '')

    def command_for_save_email_pass(self):

        if self.email_entry.get() == '' or self.email_pass_entry.get() == "":
            Messagebox.show_warning('Empty Fields', '', self.Admin_panel)
        else:
            self.save_changing_email_for_invoice_chng(self.email_entry.get(), self.email_pass_entry.get())
            Messagebox.show_info('Saved successfully', '', self.Admin_panel)
            self.email_entry.insert(0, '')
            self.email_pass_entry.insert(0, '')

    def update_password(self, passs):
        data = connect_to_database()
        cur, db = data[0], data[1]
        cur.execute('UPDATE admin_cred SET pass=? where id=?', (passs, self.database_name))
        db.commit()
        db.close()

    def fetch_current_pass(self, id, passs):
        result = ''
        data = connect_to_database()
        cur, db = data[0], data[1]
        r = cur.execute('select * from admin_cred where id=? and pass=?', (id, passs))
        for i in r:
            result = i
        db.commit()
        db.close()
        return result

    def save_changing_email_for_invoice_chng(self, email, password):
        data = connect_to_built_database(self.database_name)
        cur, db = data[0], data[1]
        try:
            cur.execute('delete from sending_mail')
        except:
            pass
        cur.execute('insert into sending_mail(email,password) values(?,?)', (email, password))
        db.commit()
        db.close()

    def save_stor_details(self, name, location, telephone, helpline, email):
        data = connect_to_built_database(self.database_name)
        cur, db = data[0], data[1]
        try:
            cur.execute('delete from store_details')
        except:
            pass
        cur.execute('insert into store_details(name,location,telephone,helpline,email) values(?,?,?,?,?)',
                    (name, location, telephone, helpline, email))
        db.commit()
        db.close()

    def command_for_save_stor_details(self):

        if self.stor_name_entry.get() == '' or self.location_entry.get() == "" or self.Telephone_entry.get() == '' or self.helpline_entry.get() == "" or self.mail_entry.get() == '':
            Messagebox.show_warning('Empty Fields', '', self.Admin_panel)
        else:
            self.save_stor_details(self.stor_name_entry.get(), self.location_entry.get(), self.Telephone_entry.get(),
                                   self.helpline_entry.get(), self.mail_entry.get())
            Messagebox.show_info('Changed successfully', '', self.Admin_panel)
            self.stor_name_entry.insert(0, '')
            self.location_entry.insert(0, '')
            self.Telephone_entry.insert(0, '')
            self.helpline_entry.insert(0, '')
            self.mail_entry.insert(0, '')

    def command_for_setting_button(self):
        self.setting_button.configure(bootstyle=INFO)
        self.inventory_button.configure(bootstyle=PRIMARY)
        self.invoice_button.configure(bootstyle=PRIMARY)
        self.emp_button.configure(bootstyle=PRIMARY)
        self.delete_pre_frame()
        self.setting()


class Employee_Panel:
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.emp_panelTk.destroy()
            exit()
    def __init__(self, name, top):
        self.databaseName = name
        self.emp_panelTk = top
        self.emp_panelTk.title('Billing System')
        self.emp_panelTk.configure(bg='#F4F4F4')
        self.emp_panelTk.geometry('1400x800+200+50')
        self.emp_panelTk.iconbitmap('icon\\main.ico')
        self.define_frames()
        self.Search_logout()
        self.customer_details()
        self.Product_details()
        self.BillOptions()
        self.bill_window()
        self.emp_panelTk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.emp_panelTk.mainloop()

    def define_frames(self):
        self.eframe = ttk.Frame(self.emp_panelTk)
        self.eframe.pack(side=TOP, fill=BOTH, expand=True)

        self.eframe1 = ttk.Frame(self.eframe)
        self.eframe1.pack(side=TOP, fill=X)

        self.eframe2 = tk.Frame(self.eframe, bg='white', highlightthickness=20, highlightbackground='white',
                                highlightcolor='white')
        self.eframe2.pack(side=TOP, fill=BOTH, expand=True)

        self.eframe3 = ttk.Frame(self.eframe2)
        self.eframe3.pack(side=TOP, fill=X)

        self.eframe4 = ttk.Frame(self.eframe2, bootstyle=INFO)
        self.eframe4.pack(side=TOP, fill=X)

        self.eframe5 = ttk.Frame(self.eframe2, bootstyle=INFO)
        self.eframe5.pack(side=TOP, fill=BOTH, expand=True)

        self.eframe5_1 = ttk.Frame(self.eframe5, bootstyle=SUCCESS)
        self.eframe5_1.pack(side=LEFT, fill=BOTH)

        self.eframe5_1_1 = ttk.Frame(self.eframe5_1, bootstyle=SUCCESS, width=30)
        self.eframe5_1_1.pack(side=TOP, fill=BOTH, expand=True)

        self.eframe5_1_2 = ttk.Frame(self.eframe5_1, bootstyle=INFO)
        self.eframe5_1_2.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.eframe5_2 = ttk.Frame(self.eframe5, bootstyle=INFO)
        self.eframe5_2.pack(side=RIGHT, fill=BOTH, expand=True)

        self.eframe5_3 = ttk.Label(self.eframe5, bootstyle=INFO, width=2)
        self.eframe5_3.pack(side=LEFT, fill=Y)

    def command_for_bill_search_bnt(self):
        if self.esearch_box.get() == '':
            Messagebox.show_warning('Enter Bill Number.', '', self.emp_panelTk)
        else:

            Pdct = self.fetch_productDetails_by_id_empp(self.esearch_box.get())
            if Pdct != []:
                self.search_bill_by_id_and_display_it(self.esearch_box.get(), Pdct)
            else:
                Messagebox.show_error('Bill number is not found.', '', self.emp_panelTk)

    def fetch_productDetails_by_id_empp(self, id):
        responce = connect_to_built_database(self.databaseName)
        con, db = responce[0], responce[1]
        data = con.execute('select * from productDetails where billNum=?', (id,))
        result = []
        for i in data:
            result.append(i)
        db.commit()
        db.close()
        return result

    def search_bill_by_id_and_display_it(self, Id, Pdct):
        invoice = self.fetch_invoices_details_by_ID(Id)
        self.label7.configure(text='')
        self.label9.configure(text='')
        self.label12.configure(text='')
        self.label13.configure(text='')
        self.delete_all_treeview_data(self.treeview)
        self.label7.configure(text=str(Id))
        self.label9.configure(text=str(invoice[3]))
        self.label12.configure(text=invoice[2])
        self.label13.configure(text=invoice[1])
        for i in Pdct:
            self.treeview.insert('', END, values=tuple(i[1].split('|')))

    def Search_logout(self):
        self.billing_label = tk.Label(self.eframe1, text='Billing System', font=('calibri', 15, 'bold'))
        self.billing_label.pack(side=TOP, fill=X)

        self.serach_btn = ttk.Button(self.eframe3, bootstyle=(SUCCESS), padding=0,
                                     cursor='hand2', takefocus=0, text='Search', width=9,
                                     command=self.command_for_bill_search_bnt)
        self.serach_btn.pack(side=RIGHT, fill=Y)

        self.sep3 = tk.Label(self.eframe3, text='', width=1)
        self.sep3.pack(side=RIGHT, fill=Y)

        self.esearch_box = ttk.Entry(self.eframe3, bootstyle=DARK, width=30)
        self.esearch_box.pack(side=RIGHT, fill=Y)

        self.sep3 = tk.Label(self.eframe3, text='', width=2)
        self.sep3.pack(side=RIGHT, fill=Y)

        self.bill_n = ttk.Label(self.eframe3, text='Bill Number')
        self.bill_n.pack(side=RIGHT, fill=X)

        self.logout_btn = ttk.Button(self.eframe3, bootstyle=(INFO), padding=0,
                                     cursor='hand2', takefocus=0, text='LOGOUT', width=9,
                                     command=self.command_for_logout_for_emp)
        self.logout_btn.pack(side=LEFT, fill=Y)

    def command_for_logout_for_emp(self):
        d = messagebox.askyesno('', 'Do you want to logout')

        if d:
            insert_login_cred('N', '', '')
            self.emp_panelTk.withdraw()
            self.main_window = tk.Toplevel()
            Main_Window(self.main_window)

    def customer_details(self):
        self.sep = tk.Label(self.eframe4, text='', height=0)
        self.sep.pack(side=TOP, fill=X)

        self.pand_window = ttk.Labelframe(self.eframe4, bootstyle=DARK, text='Customer Details', padding=15)
        self.pand_window.pack(side=TOP, fill=X)

        self.customer_label = ttk.Label(self.pand_window, text='Name')
        self.customer_label.pack(side=LEFT, fill=Y)

        self.sep = tk.Label(self.pand_window, text='', width=1)
        self.sep.pack(side=LEFT, fill=X)

        self.cName_box = ttk.Entry(self.pand_window, bootstyle=DARK, width=30)
        self.cName_box.pack(side=LEFT, fill=Y)

        self.sep = tk.Label(self.pand_window, text='', width=4)
        self.sep.pack(side=LEFT, fill=X)

        self.cAddress_label = ttk.Label(self.pand_window, text='Address')
        self.cAddress_label.pack(side=LEFT, fill=Y)

        self.sep = tk.Label(self.pand_window, text='', width=1)
        self.sep.pack(side=LEFT, fill=X)

        self.cAddress_box = ttk.Entry(self.pand_window, bootstyle=DARK, width=30)
        self.cAddress_box.pack(side=LEFT, fill=Y)

        self.sep = tk.Label(self.pand_window, text='', width=4)
        self.sep.pack(side=LEFT, fill=X)

        self.cemail_label = ttk.Label(self.pand_window, text='Email')
        self.cemail_label.pack(side=LEFT, fill=Y)

        self.sep = tk.Label(self.pand_window, text='', width=1)
        self.sep.pack(side=LEFT, fill=X)

        self.cemail_box = ttk.Entry(self.pand_window, bootstyle=DARK, width=30)
        self.cemail_box.pack(side=LEFT, fill=Y)

        self.sep = tk.Label(self.pand_window, text='', width=4)
        self.sep.pack(side=LEFT, fill=X)

        self.cContact_label = ttk.Label(self.pand_window, text='Contact No.')
        self.cContact_label.pack(side=LEFT, fill=Y)

        self.sep = tk.Label(self.pand_window, text='', width=1)
        self.sep.pack(side=LEFT, fill=X)

        self.cContact_box = ttk.Entry(self.pand_window, bootstyle=DARK, width=30)
        self.cContact_box.pack(side=LEFT, fill=Y)

    def Product_details(self):
        self.sep = tk.Label(self.eframe5_1_1, text='', height=0)
        self.sep.pack(side=TOP, fill=X)

        self.pand_window = ttk.Labelframe(self.eframe5_1_1, bootstyle=DARK, text='Products Details', padding=15)
        self.pand_window.pack(side=TOP, fill=BOTH, expand=True)
        self.product_pand_window = self.pand_window

        self.Frame = tk.Frame(self.pand_window)
        self.Frame.pack(side=TOP, fill=X)
        self.sep = tk.Label(self.Frame, text='Select Category', height=0)
        self.sep.pack(side=LEFT, fill=Y)

        self.p_v1 = tk.StringVar()
        self.p_v2 = tk.StringVar()
        self.p_v3 = tk.StringVar()
        self.cal1()
        self.category_combo = ttk.Combobox(self.pand_window, bootstyle=(SUCCESS), width=70, cursor='hand2',
                                           textvariable=self.p_v1, values=self.l5, state="readonly")
        self.category_combo.pack(side=TOP, fill=Y)
        self.category_combo.bind("<<ComboboxSelected>>", self.Category_values)

        self.Frame = tk.Frame(self.pand_window)
        self.Frame.pack(side=TOP, fill=X)
        self.sep = tk.Label(self.Frame, text='Select Sub Category', height=0)
        self.sep.pack(side=LEFT, fill=Y)

        self.subcategory_combo = ttk.Combobox(self.pand_window, bootstyle=(SUCCESS), width=70, cursor='hand2',
                                              textvariable=self.p_v2, state="readonly")
        self.subcategory_combo.pack(side=TOP, fill=Y)
        self.subcategory_combo.bind("<<ComboboxSelected>>", self.define_p_values)

        self.Frame = tk.Frame(self.pand_window)
        self.Frame.pack(side=TOP, fill=X)
        self.sep = tk.Label(self.Frame, text='Select Product', height=0)
        self.sep.pack(side=LEFT, fill=Y)

        self.product_combo = ttk.Combobox(self.pand_window, bootstyle=(SUCCESS),
                                          width=70, cursor='hand2', textvariable=self.p_v3, state="readonly")
        self.product_combo.pack(side=TOP, fill=Y)
        self.product_combo.bind("<<ComboboxSelected>>", self.show_stock)

        self.Frame = tk.Frame(self.pand_window)
        self.Frame.pack(side=TOP, fill=X)
        self.sep = tk.Label(self.Frame, text='Quantity', height=0)
        self.sep.pack(side=LEFT, fill=Y)

        self.quantity_box = ttk.Entry(self.pand_window, bootstyle=SUCCESS, width=30)
        self.quantity_box.pack(side=TOP, fill=X)

        self.Frame = tk.Frame(self.pand_window, highlightthickness=15, highlightbackground='white',
                              highlightcolor='white')
        self.Frame.pack(side=BOTTOM, fill=X)

        self.sep = tk.Label(self.Frame, text='', width=5)
        self.sep.pack(side=LEFT, fill=Y)

        self.add_to_cart_btn = ttk.Button(self.Frame, bootstyle=(SUCCESS), padding=5,
                                          cursor='hand2', takefocus=0, text='Add to Bill', width=15,
                                          command=self.command_for_add_to_bill)
        self.add_to_cart_btn.pack(side=LEFT, fill=Y)

        ToolTip(
            self.add_to_cart_btn,
            text="Add Products to the Bill.",
        )

        self.sep = tk.Label(self.Frame, text='', width=2)
        self.sep.pack(side=LEFT, fill=Y)

        self.remove_cart_btn = ttk.Button(self.Frame, bootstyle=(SUCCESS), padding=5,
                                          cursor='hand2', takefocus=0, text='Remove From Bill', width=20,
                                          command=self.command_for_remove_from_bill)
        self.remove_cart_btn.pack(side=LEFT, fill=Y)
        ToolTip(
            self.remove_cart_btn,
            text="Remove Added Products From the Bill.",
        )

        self.sep = tk.Label(self.Frame, text='', width=2)
        self.sep.pack(side=LEFT, fill=Y)

        self.clear_btn = ttk.Button(self.Frame, bootstyle=(SUCCESS), padding=5,
                                    cursor='hand2', takefocus=0, text='Clear', width=15,
                                    command=self.command_clear_for_product)
        self.clear_btn.pack(side=LEFT, fill=Y)
        ToolTip(
            self.clear_btn,
            text="Clear All the Entries of Product Details Block.",
        )

    def cal1(self):
        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        r = cur.execute("select category from Inventory_1")
        self.l4 = []
        for i5 in r:
            self.l4.append(i5[0])
        self.l5 = list(set(self.l4))
        db.commit()
        db.close()

    def Category_values(self, event):
        l7 = []
        for i in self.l5:
            data = connect_to_built_database(self.databaseName)
            cur, db = data[0], data[1]
            r = cur.execute("select subcategory from Inventory_1 where category='" + i + "'")
            l6 = []
            for j in r:
                l6.append(j[0])
            l7.append(list(set(l6)))
            db.commit()
            db.close()
        for i in zip(self.l5, l7):
            r = list(i)
            if self.p_v1.get() == r[0]:
                self.subcategory_combo['values'] = r[1]

    def define_p_values(self, event):
        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        r = cur.execute("select subcategory from Inventory_1")
        l1 = []
        for i in r:
            for j in i:
                l1.append(j)
        l2 = list(set(l1))
        db.commit()
        db.close()

        l4 = []
        for j in l2:
            data = connect_to_built_database(self.databaseName)
            cur, db = data[0], data[1]

            r1 = cur.execute("select name from Inventory_1 where subcategory=?", (j,))
            l3 = []
            for i in r1:
                for i1 in i:
                    l3.append(i1)

            l4.append(l3)
            db.commit()
            db.close()

        for i in zip(l2, l4):
            r = list(i)
            if self.p_v2.get() == r[0]:
                self.product_combo['values'] = r[1]

    def show_stock(self, event):

        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        r = cur.execute("select qty from Inventory_1 where name=?", (self.p_v3.get(),))
        for i in r:
            self.s = i[0]
        try:
            self.Frame_____.pack_forget()
        except:
            pass
        self.Frame_____ = tk.Frame(self.product_pand_window)
        self.Frame_____.pack(side=TOP, fill=X)
        self.sep = ttk.Label(self.Frame_____, text=f"In Stock {self.s}", bootstyle=INFO)
        self.sep.pack(side=LEFT, fill=Y)
        db.commit()
        db.close()

    def BillOptions(self):
        self.billId = ''
        self.sep = tk.Label(self.eframe5_1_2, text='', height=0)
        self.sep.pack(side=TOP, fill=X)

        self.pand_window = ttk.Labelframe(self.eframe5_1_2, bootstyle=DARK, text='Bill Options', padding=15)
        self.pand_window.pack(side=TOP, fill=BOTH, expand=True)

        self.sep = tk.Label(self.pand_window, text='', width=2)
        self.sep.pack(side=LEFT, fill=Y)

        self.total_btn = ttk.Button(self.pand_window, bootstyle=(SUCCESS), padding=5,
                                    cursor='hand2', takefocus=0, text='Cal Total Price', width=14,
                                    command=self.billoption_total_check)
        self.total_btn.pack(side=LEFT, fill=X)
        ToolTip(
            self.total_btn,
            text="Calculate the Prices of Added Products in Bill",
        )

        self.sep = tk.Label(self.pand_window, text='', width=2)
        self.sep.pack(side=LEFT, fill=Y)

        self.generate_btn = ttk.Button(self.pand_window, bootstyle=(SUCCESS), padding=5,
                                       cursor='hand2', takefocus=0, text='Generate Bill', width=14,
                                       command=self.billoption_generate_check)
        self.generate_btn.pack(side=LEFT, fill=X)

        ToolTip(
            self.generate_btn,
            text="Generate Bill ID",
        )

        self.sep = tk.Label(self.pand_window, text='', width=2)
        self.sep.pack(side=LEFT, fill=Y)

        self.clear_btn = ttk.Button(self.pand_window, bootstyle=(SUCCESS), padding=5,
                                    cursor='hand2', takefocus=0, text='Clear', width=10,
                                    command=self.command_for_clear_for_bill)
        self.clear_btn.pack(side=LEFT, fill=X)

        ToolTip(
            self.clear_btn,
            text="Clear Generated Bill",
        )

        self.sep = tk.Label(self.pand_window, text='', width=2)
        self.sep.pack(side=LEFT, fill=Y)

        self.open_btn = ttk.Button(self.pand_window, bootstyle=(SUCCESS), padding=5,
                                   cursor='hand2', takefocus=0, text='Open pdf', width=14, command=self.open_pdf)
        self.open_btn.pack(side=LEFT, fill=X)
        ToolTip(
            self.open_btn,
            text="Open Pdf file of Invoice",
        )

    def open_pdf(self):
        if self.billId != '':
            path = rf'invoices_pdf\{self.billId + ".pdf"}'
            os.system(path)
        elif self.esearch_box.get() != '':
            path = rf'invoices_pdf\{self.esearch_box.get() + ".pdf"}'
            os.system(path)
        elif self.billId == '':
            Messagebox.show_warning('First Generate the Bill', self.emp_panelTk)

    def fetch_stor_details(self):
        result = ''
        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        r = cur.execute('select * from store_details')
        for i in r:
            result = i
        db.commit()
        db.close()
        return result

    def bill_window(self):
        self.sep = tk.Label(self.eframe5_2, text='', height=1)
        self.sep.pack(side=TOP, fill=X)

        self.pand_window = ttk.Labelframe(self.eframe5_2, bootstyle=DARK, text='Bill Window', padding=15)
        self.pand_window.pack(side=TOP, fill=BOTH, expand=True)

        self.Frame = tk.Frame(self.pand_window)
        self.Frame.pack(side=TOP, fill=BOTH, expand=True)
        res = self.fetch_stor_details()
        if res != '':
            name = res[0]
            location = res[1]
            telephon = res[2]
            helpline = res[3]
            emailid = res[4]
        else:
            name = 'XYZ Retail Ltd.'
            location = 'Ghaziabad-201002'
            telephon = '022-298766986'
            helpline = '1800-200-255'
            emailid = 'niru@gmail.com'

        self.label1 = ttk.Label(self.Frame, text=name, anchor=CENTER)
        self.label1.pack(side=TOP, fill=X)
        self.label2 = ttk.Label(self.Frame, text=location, anchor=CENTER)
        self.label2.pack(side=TOP, fill=X)
        self.label3 = ttk.Label(self.Frame, text=f'Telephone No. : {telephon}', anchor=CENTER)
        self.label3.pack(side=TOP, fill=X)
        self.label4 = ttk.Label(self.Frame, text=f'Help Line No. : {helpline}', anchor=CENTER)
        self.label4.pack(side=TOP, fill=X)
        self.label5 = ttk.Label(self.Frame, text=f'Email ID : {emailid}', anchor=CENTER)
        self.label5.pack(side=TOP, fill=X)

        self.sep = tk.Label(self.Frame, text='', height=1)
        self.sep.pack(side=TOP, fill=X)

        self.Frame1 = tk.Frame(self.Frame, bg='red')
        self.Frame1.pack(side=TOP, fill=X)
        width = 15

        self.label6 = ttk.Label(self.Frame1, text='Bill Number : ', width=width)
        self.label6.pack(side=LEFT, fill=X)
        self.label7 = ttk.Label(self.Frame1, text='')
        self.label7.pack(side=LEFT, fill=X)
        self.label9 = ttk.Label(self.Frame1, text='')
        self.label9.pack(side=RIGHT, fill=X)
        self.label10 = ttk.Label(self.Frame1, text='Phone Number : ', width=width)
        self.label10.pack(side=RIGHT, fill=X)

        self.Frame2 = tk.Frame(self.Frame)
        self.Frame2.pack(side=TOP, fill=X)
        self.label11 = ttk.Label(self.Frame2, text='Customer Name : ', width=width)
        self.label11.pack(side=LEFT, fill=X)
        self.label12 = ttk.Label(self.Frame2, text='')
        self.label12.pack(side=LEFT, fill=X)
        self.label13 = ttk.Label(self.Frame2, text='')
        self.label13.pack(side=RIGHT, fill=X)
        self.label14 = ttk.Label(self.Frame2, text='Date : ', width=width)
        self.label14.pack(side=RIGHT, fill=X)
        self.Frame3 = tk.Frame(self.Frame)
        self.Frame3.pack(side=TOP, fill=BOTH, expand=True)
        self.bill_treeview(self.Frame3)

    def bill_treeview(self, frame):
        self.sep = tk.Label(frame, text='', height=0)
        self.sep.pack(side=TOP, fill=X)
        self.se = ttk.Separator(frame, bootstyle="info")
        self.se.pack(side=TOP, fill=X)
        self.sep = tk.Label(frame, text='', height=0)
        self.sep.pack(side=TOP, fill=X)
        headings = ['Product Name', 'Quantity', 'Price']
        columns = [1, 2, 3]
        self.scroll = ttk.Scrollbar(frame, bootstyle="round", orient=VERTICAL)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.treeview = ttk.Treeview(frame, columns=columns, show='headings', bootstyle=LIGHT,
                                     yscrollcommand=self.scroll)
        self.treeview.column(1, anchor='w', width=100)
        self.treeview.column(2, anchor='center', width=100)
        self.treeview.column(3, anchor='center', width=100)
        self.treeview.heading(columns[0], text=headings[0], anchor='w')
        self.treeview.heading(columns[1], text=headings[1], anchor='center')
        self.treeview.heading(columns[2], text=headings[2], anchor='center')
        self.treeview.pack(side=LEFT, fill=BOTH, expand=True)

    def command_for_add_to_bill(self):
        self.bill_add_cart()
        self.treeview.insert('', 0, values=(self.p_v3.get(), self.quantity_box.get(), self.price))

    def bill_add_cart(self):
        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        r2 = cur.execute("select mrp from Inventory_1 where name=?", (self.p_v3.get(),))
        for i in r2:
            self.price = float(self.quantity_box.get()) * float(i[0])
            break
        db.commit()
        db.close()

    def command_for_remove_from_bill(self):
        try:
            self.treeview.delete(self.treeview.get_children()[0])
        except:
            pass

    def command_clear_for_product(self):
        self.p_v1.set("")
        self.p_v2.set("")
        self.p_v3.set("")
        self.quantity_box.delete(0, END)
        try:
            self.Frame_____.pack_forget()
        except:
            pass

    def billoption_total_check(self):
        if self.p_v2.get() == "":
            Messagebox.show_warning("Add a Product", self.emp_panelTk)
        else:
            price = []
            item = self.treeview.get_children()
            for i in item:
                if 'Total Price' in self.treeview.item(i)['values'][2]:
                    self.treeview.delete(i)
                    p = 0
                else:
                    p = self.treeview.item(i)['values'][2]
                price.append(float(p))
            self.treeview.insert('', END, values=('', '', 'Total Price : ' + str(sum(price)) + " Rs."))

        # ---------------------check validity of phone number-------------

    def isvalid_num(self, s):
        Pattern = compile("(0/91)?[7-9][0-9]{9}")
        return Pattern.match(s)

    def isValidEmail(self, email):

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return match(regex, email)

    def billoption_generate_check(self):
        s = str(self.cContact_box.get())
        if self.cName_box.get() == "" or self.cAddress_box.get() == "" or self.cemail_box.get() == '' or self.cContact_box.get() == '':
            Messagebox.show_warning("Fill all the entries in Customer Details Block", "", self.emp_panelTk)
        elif not self.isValidEmail(self.cemail_box.get()):
            Messagebox.show_error('Invalid Email', '', self.emp_panelTk)
        elif self.isvalid_num(s):
            data = self.bill_generate()
            billId, Date = data[0], data[1]
            data1 = (billId, Date, self.cName_box.get(), self.cContact_box.get())
            details = []
            # qnt=[]
            # name=''
            for i in self.treeview.get_children():
                dat=self.treeview.item(i)['values']
                # qnt.append(dat[1])
                msg = '|'.join(map(str, dat))
                details.append(msg)
                self.save_products_details(billId, msg)
                name=dat[0]
            self.save_bill_details(data1)
            # qnt.pop()
            # sum_=sum(qnt)
            # self.update_qyt(sum_,name)

            res = self.fetch_stor_details()
            if res != '':
                name = res[0]
                location = res[1]
                telephon = res[2]
                helpline = res[3]
                emailid = res[4]
            else:
                name = 'XYZ Retail Ltd.'
                location = 'Ghaziabad-201002'
                telephon = '022-298766986'
                helpline = '1800-200-255'
                emailid = 'niru@gmail.com'
            PDF_MAKER(billId, billId, self.cName_box.get(), self.cContact_box.get(), Date, details, name, location,
                      telephon, helpline, emailid)
            self.billId = billId
            Messagebox.show_info("Bill Generated", "", self.emp_panelTk)
            res = self.fetch_email_to_send_invoice_file()
            if res != '':
                Thread(target=send_pdf,daemon=True,args=(res[0], res[1], self.cemail_box.get(), """Hi !! Download your invoice file.""", billId)).start()
        else:
            Messagebox.show_error('Invalid Contact Number', '', self.emp_panelTk)
    def update_qyt(self,qyt,name):
        data=connect_to_built_database(self.databaseName)
        cur,db=data[0],data[1]
        cur.execute('UPDATE Inventory_1 SET qty=? where name=?;',(qyt,name))
        db.commit()
        db.close()


    def bill_generate(self):
        self.bill_id = randint(1000, 5000)
        today = date.today()
        d = today.strftime(" %d-%m-%Y ")
        self.label7.configure(text='')
        self.label9.configure(text='')
        self.label12.configure(text='')
        self.label13.configure(text='')
        self.label7.configure(text=str(self.bill_id))
        self.label9.configure(text=str(self.cContact_box.get()))
        self.label12.configure(text=self.cName_box.get())
        self.label13.configure(text=d)
        return str(self.bill_id), d

    def command_for_clear_for_bill(self):
        self.cName_box.delete(0, END)
        self.cAddress_box.delete(0, END)
        self.cContact_box.delete(0, END)
        self.cemail_box.delete(0, END)
        self.label7.configure(text='')
        self.label9.configure(text='')
        self.label12.configure(text='')
        self.label13.configure(text='')
        self.billId = ''
        self.delete_all_treeview_data(self.treeview)

    def delete_all_treeview_data(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def save_bill_details(self, data_):
        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        cur.execute('insert into Invoices(biilNum,date, name,contact) values(?,?,?,?)', data_)
        db.commit()
        db.close()

    def fetch_invoices_details_by_ID(self, id):
        responce = connect_to_built_database(self.databaseName)
        con, db = responce[0], responce[1]
        data = con.execute(f'select * from Invoices where biilNum=?', (id,))
        result = ''
        for i in data:
            result = i
        db.commit()
        db.close()
        return result

    def save_products_details(self, billnum, list):
        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        cur.execute('insert into productDetails(billNum,text1) values(?,?)', (billnum, list))
        db.commit()
        db.close()

    def fetch_email_to_send_invoice_file(self):
        result = ''
        data = connect_to_built_database(self.databaseName)
        cur, db = data[0], data[1]
        r = cur.execute('select * from sending_mail')
        for i in r:
            result = i
        db.commit()
        db.close()
        return result


result = fetch_login_cred()
if result == '':
    top = ttk.Window()
    Main_Window(top)
elif result[0] == 'N':
    top = ttk.Window()
    Main_Window(top)

elif result[0] == 'A':
    top = ttk.Window()
    Admin_panel().Main(result[1], top)
elif result[0] == 'E':
    top = ttk.Window()
    Employee_Panel(result[1], top)
