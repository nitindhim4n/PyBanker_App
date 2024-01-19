from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk

import time
import pymysql
import random
import gmail

win=Tk()
win.state("zoomed")
win.resizable(width=False, height=True)
win.configure(bg='#3b4a9f')

lbl_title=Label(win,text="PyBanker App",bg="White",fg="#3b4a9f",font=('arial',40,'bold'),width=50,height=2)
lbl_title.pack()

lbl_name=Label(win,text=f"{datetime.now().date()}",bg="White",font=('arial',16))
lbl_name.place(relx=.9,rely=.1)

lbl_login=Label(win,text="Login Page",bg="#3b4a9f",fg="white",font=('arial',40,'bold'))
lbl_login.place(relx=.17,rely=.5)

def main_screen():
    frm=Frame(win)
    frm.configure(bg="#E4E4E4")
    frm.place(relx=.5,rely=.21,relwidth=.4,relheight=.75)

    def forgot_pass():
        frm.destroy()
        forgotpass_screen()

    def create_new():
        frm.destroy()
        createnew_screen()

    def login():
        global name,acn
        acn=entry_accno.get()
        pwd=entry_pass.get()
        if(acn=="" or pwd==""):
            messagebox.showerror("Login","Acc. no. or password can not be empty")
            return

        con=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
        cur=con.cursor()
        cur.execute("select name from accounts where accn=%s and password=%s",(acn,pwd))
        row=cur.fetchone()
        if(row==None):
            messagebox.showerror("Login","Invalid Acc. no. or Password")
            return
        else:
            name=row[0]
        con.close()

        frm.destroy()
        login_screen()

    lbl_accno=Label(frm,text="Account Number",bg="#E4E4E4",font=('arial',20))
    lbl_accno.place(relx=.15,rely=.1)
    entry_accno=Entry(frm,font=('arial',20))
    entry_accno.place(relx=.15,rely=.18,relwidth=.7,relheight=.085)
    entry_accno.focus()

    lbl_pass=Label(frm,text="Password",bg="#E4E4E4",font=('arial',20))
    lbl_pass.place(relx=.15,rely=.3)
    entry_pass=Entry(frm,font=('arial',20),show='*')
    entry_pass.place(relx=.15,rely=.38,relwidth=.7,relheight=.085)

    btn_login=Button(frm,command=login,text="Login",font=("arial",20,'bold'),fg='white',bg='#3b4a9f')
    btn_login.place(relx=.15,rely=.52,relwidth=.7,relheight=.085)

    btn_createnew=Button(frm,command=create_new,text="Create new account",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_createnew.place(relx=.15,rely=.64,relwidth=.7,relheight=.085)

    btn_forgot=Button(frm,command=forgot_pass,text="Forgot password",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_forgot.place(relx=.15,rely=.76,relwidth=.7,relheight=.085)

def login_screen():
    frm=Frame(win)
    frm.configure(bg="#E4E4E4")
    frm.place(relx=.1,rely=.21,relwidth=.8,relheight=.75)

    def logout():
        frm.destroy()
        main_screen()

    def check_details():
        frm1=Frame(frm)
        frm1.configure(bg="pink")
        frm1.place(relx=.42,rely=.3,relwidth=.5,relheight=.6)

        con=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
        cur=con.cursor()
        cur.execute("select accn, bal, type, opendate from accounts where accn=%s",(acn))
        row=cur.fetchone()
        con.close()

        Label(frm1,text=f"Account no. \t{row[0]}",bg="pink", fg="#3b4a9f",font=('arial',20,'bold')).place(relx=.2,rely=.15)
        Label(frm1,text=f"Balance \t\t{row[1]}",bg="pink", fg="#3b4a9f",font=('arial',20,'bold')).place(relx=.2,rely=.30)
        Label(frm1,text=f"Account Type \t{row[2]}",bg="pink", fg="#3b4a9f",font=('arial',20,'bold')).place(relx=.2,rely=.45)
        Label(frm1,text=f"Open Date \t{row[3]}",bg="pink", fg="#3b4a9f",font=('arial',20,'bold')).place(relx=.2,rely=.60)

    def update():
        frm1=Frame(frm)
        frm1.configure(bg="pink")
        frm1.place(relx=.42,rely=.3,relwidth=.5,relheight=.6)

        def update_acn():
            name=entry_name.get()
            pwd=entry_pass.get()
            email=entry_email.get()
            mob=entry_mob.get()

            conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
            curobj=conobj.cursor()
            curobj.execute("update accounts set name=%s, password=%s, email=%s, mob=%s where accn=%s",(name,pwd,email,mob,acn))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Update Profile","Profile updated")

        lbl_name=Label(frm1,text="Name:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_name.place(relx=.05,rely=.07)
        entry_name=Entry(frm1,font=('arial',16))
        entry_name.place(relx=.05,rely=.17,relwidth=.4,relheight=.12)
        entry_name.focus()
        lbl_pass=Label(frm1,text="Password:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_pass.place(relx=.5,rely=.07)
        entry_pass=Entry(frm1,font=('arial',16))
        entry_pass.place(relx=.5,rely=.17,relwidth=.45,relheight=.12)
        lbl_email=Label(frm1,text="Email:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_email.place(relx=.05,rely=.35)
        entry_email=Entry(frm1,font=('arial',16))
        entry_email.place(relx=.05,rely=.45,relwidth=.9,relheight=.12)
        lbl_mob=Label(frm1,text="Mobile:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_mob.place(relx=.05,rely=.63)
        entry_mob=Entry(frm1,font=('arial',16))
        entry_mob.place(relx=.05,rely=.73,relwidth=.5,relheight=.12)

        btn_update=Button(frm1,command=update_acn,text="Update",font=("arial",20),fg='white',bg='#3b4a9f')
        btn_update.place(relx=.65,rely=.73,relwidth=.26,relheight=.12)

        conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
        curobj=conobj.cursor()
        curobj.execute("select name,password,email,mob from accounts where accn=%s",(acn))
        row=curobj.fetchone()
        conobj.close()

        entry_name.insert(0,row[0])
        entry_pass.insert(0,row[1])
        entry_email.insert(0,row[2])
        entry_mob.insert(0,row[3])

    def deposit():
        frm1=Frame(frm)
        frm1.configure(bg="pink")
        frm1.place(relx=.42,rely=.3,relwidth=.5,relheight=.6)

        def deposit_acn():
            amt=float(entry_deposit.get())
            conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
            curobj=conobj.cursor()
            curobj.execute("select bal from accounts where accn=%s",(acn))
            bal=curobj.fetchone()[0]
            curobj.close()

            curobj=conobj.cursor()
            curobj.execute("update accounts set bal=bal+%s where accn=%s",(amt,acn))
            curobj.execute("insert into txn_history values(%s,%s,%s,%s,%s)",(acn,amt,"cr",time.ctime(),bal+amt))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit",f"Amount {amt} credited to Acc. no: {acn}")

        lbl_deposit=Label(frm1,text="Deposit Amount:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_deposit.place(relx=.17,rely=.15)
        entry_deposit=Entry(frm1,font=('arial',16))
        entry_deposit.place(relx=.17,rely=.30,relwidth=.7,relheight=.12)

        btn_deposit=Button(frm1,command=deposit_acn,text="Deposit",font=("arial",20),fg='white',bg='#3b4a9f')
        btn_deposit.place(relx=.37,rely=.5,relwidth=.26,relheight=.12)

    def withdraw():
        frm1=Frame(frm)
        frm1.configure(bg="pink")
        frm1.place(relx=.42,rely=.3,relwidth=.5,relheight=.6)

        def withdraw_acn():
            amt=float(entry_withdraw.get())
            conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
            curobj=conobj.cursor()
            curobj.execute("select bal from accounts where accn=%s",(acn))
            bal=curobj.fetchone()[0]
            curobj.close()

            if(bal>amt):
                curobj=conobj.cursor()
                curobj.execute("update accounts set bal=bal-%s where accn=%s",(amt,acn))
                curobj.execute("insert into txn_history values(%s,%s,%s,%s,%s)",(acn,amt,"db",time.ctime(),bal-amt))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdraw",f"Amount {amt} debited from Acc. no: {acn}")

            else:
                messagebox.showerror("Withdraw",f"Insufficient balance: {bal}")

        lbl_withdraw=Label(frm1,text="Withdraw Amount:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_withdraw.place(relx=.17,rely=.15)
        entry_withdraw=Entry(frm1,font=('arial',16))
        entry_withdraw.place(relx=.17,rely=.30,relwidth=.7,relheight=.12)

        btn_withdraw=Button(frm1,command=withdraw_acn,text="Withdraw",font=("arial",20),fg='white',bg='#3b4a9f')
        btn_withdraw.place(relx=.37,rely=.5,relwidth=.26,relheight=.12)

    def transfer():
        frm1=Frame(frm)
        frm1.configure(bg="pink")
        frm1.place(relx=.42,rely=.3,relwidth=.5,relheight=.6)

        def transfer_acn():
            to_acn=entry_to.get()
            frm_amt=float(entry_amount.get())

            conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
            curobj=conobj.cursor()
            curobj.execute("select accn,bal from accounts where accn=%s",(to_acn))
            to_row=curobj.fetchone()
            curobj.close()

            if(to_row==None):
                messagebox.showerror("Transfer","To Account does not exist")
            else:
                curobj=conobj.cursor()
                curobj.execute("select bal from accounts where accn=%s",(acn))
                bal=curobj.fetchone()[0]
                curobj.close()
                if(bal>frm_amt):
                    curobj=conobj.cursor()
                    curobj.execute("update accounts set bal=bal+%s where accn=%s",(frm_amt,to_acn))
                    curobj.execute("update accounts set bal=bal-%s where accn=%s",(frm_amt,acn))
                    curobj.execute("Insert into txn_history values(%s,%s,%s,%s,%s)",(acn,frm_amt,"db",time.ctime(),bal-frm_amt))
                    curobj.execute("Insert into txn_history values(%s,%s,%s,%s,%s)",(to_acn,frm_amt,"cr",time.ctime(),to_row[1]+frm_amt))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Transfer","Transaction done")
                else:
                    messagebox.showerror("Transfer",f"Insufficient balance: {bal}")

        lbl_to=Label(frm1,text="To:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_to.place(relx=.17,rely=.12)
        entry_to=Entry(frm1,font=('arial',16))
        entry_to.place(relx=.17,rely=.27,relwidth=.7,relheight=.12)
        lbl_amt=Label(frm1,text="Amount:",bg="pink", fg="#3b4a9f",font=('arial',20,'bold'))
        lbl_amt.place(relx=.17,rely=.42)
        entry_amount=Entry(frm1,font=('arial',16))
        entry_amount.place(relx=.17,rely=.57,relwidth=.7,relheight=.12)

        btn_transfer=Button(frm1,command=transfer_acn,text="Transfer",font=("arial",20),fg='white',bg='#3b4a9f')
        btn_transfer.place(relx=.37,rely=.75,relwidth=.26,relheight=.12)

    def history():
        frm1=Frame(frm)
        frm1.configure(bg="pink")
        frm1.place(relx=.42,rely=.3,relwidth=.5,relheight=.6)

        con = pymysql.connect(host="localhost", port=3306, user="root", password="1234", database="banking")
        cur = con.cursor()
        cur.execute("SELECT txn_amt,txn_type,txn_date,updated_bal FROM txn_history WHERE accn=%s", (acn,))
        rows = cur.fetchall()
        con.close()

        if not rows:
            Label(frm1, text="No transaction history available", bg="pink", fg="#3b4a9f", font=('arial', 20, 'bold')).place(relx=.2, rely=.4)
        else:
            Label(frm1, text="Transaction History", bg="pink", fg="#3b4a9f", font=('arial', 24, 'bold')).place(relx=.3, rely=.05)

            tree = ttk.Treeview(frm1, columns=("Amount", "Transaction Type", "Date", "Balance"), show='headings', height=15)
            tree.heading("Amount", text="Amount")
            tree.heading("Transaction Type", text="Transaction Type")
            tree.heading("Date", text="Date")
            tree.heading("Balance", text="Balance")

            for row in rows:
                tree.insert("", "end", values=row)

            tree.place(relx=.05, rely=.15, relwidth=.9, relheight=.75)

    btn_back=Button(frm,command=logout,text="Logout",font=("arial",16),fg='white',bg='#3b4a9f')
    btn_back.place(relx=.013,rely=.03)
    lbl_login=Label(frm,text="My Account Page",fg="#3b4a9f",bg="#E4E4E4",font=('arial',20,'bold'))
    lbl_login.place(relx=.42,rely=.03)
    lbl_login=Label(frm,text=f"Welcome, {name}",fg="#3b4a9f",bg="#E4E4E4",font=('arial',20,'bold'))
    lbl_login.place(relx=.59,rely=.2)

    btn_check=Button(frm,command=check_details,text="Check Details",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_check.place(relx=.15,rely=.2,relwidth=.2,relheight=.085)
    btn_update=Button(frm,command=update,text="Update Profile",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_update.place(relx=.15,rely=.3,relwidth=.2,relheight=.085)
    btn_deposit=Button(frm,command=deposit,text="Deposit",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_deposit.place(relx=.15,rely=.4,relwidth=.2,relheight=.085)
    btn_withdraw=Button(frm,command=withdraw,text="Withdraw",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_withdraw.place(relx=.15,rely=.5,relwidth=.2,relheight=.085)
    btn_transfer=Button(frm,command=transfer,text="Transfer",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_transfer.place(relx=.15,rely=.6,relwidth=.2,relheight=.085)
    btn_txnhistory=Button(frm,command=history,text="Transaction History",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_txnhistory.place(relx=.15,rely=.7,relwidth=.2,relheight=.085)

def createnew_screen():
    frm=Frame(win)
    frm.configure(bg="#E4E4E4")
    frm.place(relx=.1,rely=.21,relwidth=.8,relheight=.75)

    def reset():
        entry_name.delete(0,"end")
        entry_pass.delete(0,"end")
        entry_email.delete(0,"end")
        entry_mobile.delete(0,"end")
        entry_name.focus()

    def back():
        frm.destroy()
        main_screen()

    def create_acn():
        name=entry_name.get()
        pwd=entry_pass.get()
        email=entry_email.get()
        mob=entry_mobile.get()
        acc_type=combo_acctype.get()
        opendate=datetime.now().date()
        bal=2000

        conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
        curobj=conobj.cursor()
        curobj.execute("insert into accounts(name,password,email,mob,bal,type,opendate) values(%s,%s,%s,%s,%s,%s,%s)",(name,pwd,email,mob,bal,acc_type,opendate))
        conobj.commit()
        conobj.close()

        conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
        curobj=conobj.cursor()
        curobj.execute("select max(accn) from accounts")
        row=curobj.fetchone()
        lbl_acn=Label(frm,text=f"Account opened with Account no.:{row[0]}",bg="#E4E4E4",font=('arial',16))
        lbl_acn.place(relx=.6,rely=.7)
        conobj.close()

        reset()

    btn_back=Button(frm,command=back,text="Back",font=("arial",16),fg='white',bg='#3b4a9f')
    btn_back.place(relx=.013,rely=.03)
    lbl_login=Label(frm,text="Create New Account",fg="#3b4a9f",bg="#E4E4E4",font=('arial',20,'bold'))
    lbl_login.place(relx=.42,rely=.03)

    lbl_name=Label(frm,text="Name",bg="#E4E4E4",font=('arial',16))
    lbl_name.place(relx=.15,rely=.1)
    entry_name=Entry(frm,font=('arial',16))
    entry_name.place(relx=.15,rely=.16,relwidth=.35,relheight=.075)
    entry_name.focus()

    lbl_pass=Label(frm,text="Password",bg="#E4E4E4",font=('arial',16))
    lbl_pass.place(relx=.15,rely=.25)
    entry_pass=Entry(frm,font=('arial',16),show='*')
    entry_pass.place(relx=.15,rely=.31,relwidth=.35,relheight=.075)

    lbl_email=Label(frm,text="Email",bg="#E4E4E4",font=('arial',16))
    lbl_email.place(relx=.15,rely=.4)
    entry_email=Entry(frm,font=('arial',16))
    entry_email.place(relx=.15,rely=.46,relwidth=.35,relheight=.075)

    lbl_mobile=Label(frm,text="Mobile No.",bg="#E4E4E4",font=('arial',16))
    lbl_mobile.place(relx=.15,rely=.55)
    entry_mobile=Entry(frm,font=('arial',16))
    entry_mobile.place(relx=.15,rely=.61,relwidth=.35,relheight=.075)

    lbl_acctype=Label(frm,text="Account Type",bg="#E4E4E4",font=('arial',16))
    lbl_acctype.place(relx=.15,rely=.7)
    combo_acctype=Combobox(frm,font=('arial',16),values=['Savings','Current'])
    combo_acctype.current(0)
    combo_acctype.place(relx=.15,rely=.76,relwidth=.35,relheight=.075)

    btn_createacc=Button(frm,command=create_acn,text="Create",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_createacc.place(relx=.7,rely=.4,relwidth=.1,relheight=.085)
    btn_reset=Button(frm,command=reset,text="Reset",font=("arial",20),fg='white',bg='#3b4a9f')
    btn_reset.place(relx=.7,rely=.55,relwidth=.1,relheight=.085)

def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg="#E4E4E4")
    frm.place(relx=.1,rely=.21,relwidth=.8,relheight=.75)

    def back():
        frm.destroy()
        main_screen()

    def get_otp():
        acn=entry_accno.get()
        email=entry_email.get()

        conobj=pymysql.connect(host="localhost",port=3306,user="root",password="1234",database="banking")
        curobj=conobj.cursor()
        curobj.execute("select email, password from accounts where accn=%s",(acn))
        row=curobj.fetchone()
        if(row==None):
            messagebox.showerror("Password Recovery","Account does not exist")
        else:
            if(row[0]==email):
                otp=random.randint(1000,9999)
                print(otp)

                try:
                    con=gmail.GMail("nitindhiman112780@gmail.com","vpnaryslzutbonhw")
                    mail=gmail.Message(to=email,subject="OTP Verification",text=f"Your OTP is {otp}")
                    con.send(mail)
                    messagebox.showinfo("Password Recovery","OTP sent, check your email")
                except:
                    messagebox.showerror("Password Recovery","Something went wrong")

                lbl_otp=Label(frm,text="Enter OTP",bg="#E4E4E4",font=('arial',16))
                lbl_otp.place(relx=.15,rely=.55)
                entry_otp=Entry(frm,font=('arial',16))
                entry_otp.place(relx=.15,rely=.61,relwidth=.35,relheight=.075)
                entry_otp.focus()

                def getpwd():
                    votp=int(entry_otp.get())
                    if(votp==otp):
                        messagebox.showinfo("Password Recovery",f"Your password:{row[1]}")
                    else:
                        messagebox.showerror("Password Recovery","Incorrect OTP")

                btn_verify=Button(frm,command=getpwd,text="Verify",font=("arial",18),fg='white',bg='#3b4a9f')
                btn_verify.place(relx=.26,rely=.75,relwidth=.1,relheight=.085)

            else:
                messagebox.showerror("Password Recovery","Email is not correct")
        conobj.close()

    btn_back=Button(frm,command=back,text="Back",font=("arial",16),fg='white',bg='#3b4a9f')
    btn_back.place(relx=.013,rely=.03)
    lbl_login=Label(frm,text="Forgot Password",fg="#3b4a9f",bg="#E4E4E4",font=('arial',20,'bold'))
    lbl_login.place(relx=.42,rely=.03)

    lbl_accno=Label(frm,text="Account Number",bg="#E4E4E4",font=('arial',16))
    lbl_accno.place(relx=.15,rely=.1)
    entry_accno=Entry(frm,font=('arial',16))
    entry_accno.place(relx=.15,rely=.16,relwidth=.35,relheight=.075)
    entry_accno.focus()

    lbl_email=Label(frm,text="Email",bg="#E4E4E4",font=('arial',16))
    lbl_email.place(relx=.15,rely=.25)
    entry_email=Entry(frm,font=('arial',16))
    entry_email.place(relx=.15,rely=.31,relwidth=.35,relheight=.075)

    btn_getotp=Button(frm,command=get_otp,text="Get OTP",font=("arial",18),fg='white',bg='#3b4a9f')
    btn_getotp.place(relx=.26,rely=.45,relwidth=.1,relheight=.085)

main_screen()
win.mainloop()
