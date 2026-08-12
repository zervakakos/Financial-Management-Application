import smtplib #for email
from tkinter import * #tkinter library
from tkinter import Tk,Label #tkinter library
import sqlite3 #sqlite library
from tkinter import messagebox #tkinter library
import random #used for generation of random id
from tkinter.ttk import Treeview #tkinter library
from datetime import datetime #https://docs.python.org/3/library/datetime.html
from datetime import timedelta
import hashlib #used for hashing and salting
import base64 #used for hashing and salting
import uuid #used for hashing and salting
from tkinter import simpledialog #used to prompt Bill to enter his email
import re #used to evaluate entered email syntax
import matplotlib.pyplot as plt #used for plotting graph
from googleapiclient.http import MediaFileUpload #used for sending email
from google_service import Create_Service #used for sending emailz


#OAuth Secret json File Here
CLIENT_SECRET_FILE = r'C:\xxxx'
API_NAME = 'drive' #API name
API_VERSION = 'v3' #API version
SCOPES = ['https://www.googleapis.com/auth/drive']


service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


#establishing connection to database
conn = sqlite3.connect(r"C:\xxxx")
cursor = conn.cursor() #anything related to the execution, fetching or general database interaction should be assigned to the cursor


#creates table containing the log-in information of Bill depending on his likening
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT,
    salt TEXT,
    id INTEGER,
    balance REAL)
""")
#creates table containing the budgetary data of Bill's account only if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS budgetdata(
    id INTEGER,
    category TEXT,
    subcategory TEXT,
    date TEXT,
    amount REAL)
    """)

#function to upload database to the drive
def uploadtodrive():
    file_metadata = {
        'name': "Database.db", #what will be uploaded to drive should be named 'Database'
        'parents': ['xxxx'] #part of the URL of my google drive folder
    }
    #uploads actual database by considering its position within the directory
    mediacontent=MediaFileUpload(r"C:xxxx",mimetype='application/x-sqlite3')
    file = service.files().create(
        body=file_metadata,
        media_body=mediacontent
    ).execute() #executes the command


#initialize the GUI Window
GUI=Tk(className="Budget Program")
GUI.geometry("400x500")
GUI.resizable(False, False)

#initialize each frame of the program (aka each screen regarding the program)
mainmenuframe=Frame(GUI)
loginframe=Frame(GUI)
createaccframe=Frame(GUI)
bankframe = Frame(GUI)
depframe = Frame(GUI)
withdrawframe = Frame(GUI)
budgetframe=Frame(GUI)
addframe=Frame(GUI)
removeframe=Frame(GUI)
remainingbalanceframe=Frame(GUI)

#each frame/screen should be of the same width and height->loop used
for frame in [mainmenuframe, loginframe, createaccframe, bankframe, depframe, withdrawframe,budgetframe,addframe,removeframe,
              remainingbalanceframe]:
    frame.place(relwidth=1, relheight=1)


class Main:
    """
    Builds and manages the main menu, create-account, and login screens.
    Owns the widgets for those three frames as well as the logic that used
    to live at module level: password validation / account creation,
    login authentication, and treeview column sorting (the latter is kept
    as a staticmethod since BudgetProgram's treeview also relies on it and
    it holds no instance state).
    """

    def __init__(self, mainmenuframe, createaccframe, loginframe):
        self.mainmenuframe = mainmenuframe
        self.createaccframe = createaccframe
        self.loginframe = loginframe

        self.buildmainmenu()
        self.buildcreateacc()
        self.buildlogin()

    
    def buildmainmenu(self):
        #label holding product title
        self.budgprogramlab = Label(self.mainmenuframe, text="Budget Program", font=("Arial", 12, "bold"), justify="center")
        self.budgprogramlab.place(relx=0.5, rely=0.2, anchor=CENTER)

        #button to move to create account tab
        self.createaccchoice = Button(self.mainmenuframe, text="Create Account", justify="center", width=20,
                                       command=lambda: self.createaccframe.tkraise())
        self.createaccchoice.place(relx=0.5, rely=0.4, anchor=CENTER)

        #button to move to log-in tab
        self.loginchoice = Button(self.mainmenuframe, text="Login", justify="center", width=20,
                                   command=lambda: self.loginframe.tkraise())
        self.loginchoice.place(relx=0.5, rely=0.5, anchor=CENTER)

    
    def buildcreateacc(self):
        #Contains create account title
        self.createacclab = Label(self.createaccframe, text="Create Account", font=("Arial", 12, "bold"), justify="center")
        self.createacclab.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.usernameinput = Entry(self.createaccframe) #obtains input within username field
        self.passinput = Entry(self.createaccframe) #obtains input within password field
        self.confirmpassinput = Entry(self.createaccframe) #obtains input within confirm password field

        self.usernamelabel = Label(self.createaccframe, text="Username: ", font=("Arial", 8, "bold"), justify="center")
        self.usernamelabel.place(relx=0.3, rely=0.3, anchor=CENTER) #Label to contain word "username"

        self.passlabel = Label(self.createaccframe, text="Password: ", font=("Arial", 8, "bold"), justify="center")
        self.passlabel.place(relx=0.3, rely=0.4, anchor=CENTER) #Label to contain word "password"

        self.conpasslabel = Label(self.createaccframe, text="Confirm Password: ", font=("Arial", 8, "bold"), justify="center")
        self.conpasslabel.place(relx=0.3, rely=0.5, anchor=CENTER) #Label to contain word "confirm password"

        #parameters for password creation
        self.infolabel = Label(self.createaccframe, text="Password Must Contain:\n"
                                                          "*At least one uppercase letter\n"
                                                          "*At least one special character\n"
                                                          "*Must be more than 8 characters long ",
                                font=("Arial", 8, "bold"), fg="red", justify="center")
        self.infolabel.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.usernameinput.place(relx=0.6, rely=0.3, anchor=CENTER)
        self.passinput.place(relx=0.6, rely=0.4, anchor=CENTER)
        self.confirmpassinput.place(relx=0.6, rely=0.5, anchor=CENTER)

        self.createaccbutton = Button(self.createaccframe, text="Create Account", justify="center", width=20,
                                       command=lambda: self.createacc())
        self.createaccbutton.place(relx=0.5, rely=0.6, anchor=CENTER) #calls createacc() method

        self.backbuttoncreate = Button(self.createaccframe, text="Back", justify="center", width=10,
                                        command=lambda: self.mainmenuframe.tkraise())
        self.backbuttoncreate.place(relx=0.5, rely=0.9, anchor=CENTER) #shows mainmenu tab

    
    def buildlogin(self):
        self.logacclab = Label(self.loginframe, text="Log In", font=("Arial", 12, "bold"), justify="center")
        self.logacclab.place(relx=0.5, rely=0.2, anchor=CENTER) #Used to hold "login" text

        self.usernameinputlog = Entry(self.loginframe) #accepts input for username in login tab
        self.passinputlog = Entry(self.loginframe) #accepts input for password in login tab

        self.usernameinputlog.place(relx=0.6, rely=0.3, anchor=CENTER)
        self.passinputlog.place(relx=0.6, rely=0.4, anchor=CENTER)

        self.usernamelabellog = Label(self.loginframe, text="Username: ", font=("Arial", 8, "bold"), justify="center")
        self.usernamelabellog.place(relx=0.3, rely=0.3, anchor=CENTER)

        self.passlabellog = Label(self.loginframe, text="Password: ", font=("Arial", 8, "bold"), justify="center")
        self.passlabellog.place(relx=0.3, rely=0.4, anchor=CENTER)

        self.loginbutton = Button(self.loginframe, text="Login", justify="center", width=20,
                                   command=lambda: self.loginacc())
        self.loginbutton.place(relx=0.5, rely=0.6, anchor=CENTER) #calls loginacc() method

        self.backbuttonlog = Button(self.loginframe, text="Back", justify="center", width=10,
                                     command=lambda: self.mainmenuframe.tkraise())
        self.backbuttonlog.place(relx=0.5, rely=0.9, anchor=CENTER) #shows main menu tab

    #treeview sorting (shared with BudgetProgram) 
    @staticmethod
    def treeview_sort_column(tv, col, reverse): #https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
        storetuples = [(tv.set(k, col), k) for k in tv.get_children('')]

        if col == "Amount": #if the column heading="Amount", sort numerically
            storetuples.sort(key=lambda x: float(x[0]), reverse=reverse)
        elif col == "Date": #if the column heading="Date", sort chronologically
            storetuples.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"), reverse=reverse)
        else:
            storetuples.sort(reverse=reverse) #else reverse the order of the list (for category and subcat)

        #rearrange items in sorted positions
        for index, (val, k) in enumerate(storetuples):
            tv.move(k, '', index)

        #reverse sort next time
        tv.heading(col, text=col, command=lambda _col=col: \
                     Main.treeview_sort_column(tv, _col, not reverse))

    
    def createacc(self):
        username = self.usernameinput.get() #get the username entered by Bill in the username entry field
        password = self.passinput.get() #get the password entered by Bill in the password entry field
        confirmpassword = self.confirmpassinput.get() #get the password entered by Bill in the confirmpassword entry field

        specialchar = ("!@#$%^&*()-+?_=,<>/""") #a series of special characters
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        existinguser = cursor.fetchone() #fetch any instance of the same username as the one entered by Bill
        if existinguser: #if Bill attempts multiple accounts with the same username, produce an error
            messagebox.showerror("Error", "Username already exists")
            return
        if not any(c in specialchar for c in password): #if there are no special characters in the password entered, produce an error
            messagebox.showerror("Error", "Password must must contain at least one special character")
        elif not any(c.isupper() for c in password): #if there are no upper-case characters in the password entered, produce an error
            messagebox.showerror("Error", "Password must contain at least one capital letter")
        elif len(password) < 8: #if the length of the password is smaller than 8, produce an error
            messagebox.showerror("Error", "Password must be greater than 8 characters")
        elif password != confirmpassword: #if there password does not equal to the confirmed password, produce an error
            messagebox.showerror("Error", "Passwords are not equal to each other")
        else: #else, create the account
            messagebox.showinfo("Success", "Account Created Successfully")
            salt = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')

            t_sha = hashlib.sha512() #hash password
            t_sha.update(password.encode('utf-8') + salt.encode('utf-8')) #salt the password
            hashedpassword = base64.urlsafe_b64encode(t_sha.digest()).decode('utf-8')
            identity = random.getrandbits(50) #produce a random id
            balance = 0.00 #set initial balance to 0
            cursor.execute("INSERT INTO users (username, password, salt, id, balance) VALUES(?,?,?,?,?)",
                           (username, hashedpassword, salt, identity, balance)) #insert username, hashedpassword, the salt, an id,
            #and the balance in the database
            conn.commit()

    
    def loginacc(self):
        username = self.usernameinputlog.get()
        password = self.passinputlog.get()

        #selects Bill's password and hash within the database corresponding to his username
        cursor.execute("SELECT password, salt FROM users WHERE username = ?", (username,))
        result = cursor.fetchone() #retrieves the first row of the result as tuple

        if result:
            savedpassword, salt = result #https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python
            #break up tuple into a savedpassword and a salt(which will be added to the hashed version of the password entered)

            t_sha = hashlib.sha512() #hash entered password
            t_sha.update(password.encode('utf-8') + salt.encode('utf-8')) #salt entered password
            hashedpassword = base64.urlsafe_b64encode(t_sha.digest()).decode('utf-8')

            if hashedpassword == savedpassword: #if the hashed and salted password in database is the same as the hashed + salted one entered
                messagebox.showinfo("Success", "Login Successful") #successful login
                program = BankProgram(username) #proceed to main program
                program.showbank()
            else:
                messagebox.showerror("Error", "Invalid Password") #else produce error
        else:
            messagebox.showerror("Error", "Invalid Username") #else produce error


class BankProgram:
    def __init__(self,username): #used to familiarize certain variables with this class
        self.bankframe=bankframe
        self.withdrawframe=withdrawframe
        self.depframe=depframe
        self.username=username
        self.bankbutton = Button(bankframe, text="Dep/with", justify="center", width=10,
                            command=lambda: self.showbank()) #call showbank() function if pressed
        self.bankbutton.place(relx=0.2, rely=0.95, anchor=CENTER)

        program=BudgetProgram(username,id)
        self.budgetbutton = Button(bankframe, text="Budget", justify="center", width=10,
                              command=lambda: program.showbudget()) #call showbudget() function if pressed
        self.budgetbutton.place(relx=0.8, rely=0.95, anchor=CENTER)


        cursor.execute("SELECT balance FROM users WHERE username = ?", (self.username,))
        currball = cursor.fetchone()

        self.balance=currball[0]

    def showbank(self): #used to showcase all GUI elements related to the bank frame, prompting the user to either go to withdraw or deposit
        #frame/tab
        self.bankframe.tkraise() #show bank frame/tab

        for frame in [bankframe,depframe]:
            frame.place(relwidth=1,relheight=1)

        banklab = Label(bankframe, text="Deposit/Withdraw", font=("Arial", 12, "bold"), justify="center")
        banklab.place(relx=0.5, rely=0.3, anchor=CENTER)

        depbutton=Button(bankframe,text="Deposit",width=20,justify="center",
                         command=lambda: self.showdep()) #https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
                        #call showdep() function if pressed
        depbutton.place(relx=0.3,rely=0.6,anchor=CENTER)
        withbutton = Button(bankframe, text="Withdraw", width=10, justify="center",
                           command=lambda: self.showwith()) #call showwith() function if pressed

        withbutton.place(relx=0.7, rely=0.6, anchor=CENTER)

    def showwith(self): #used to showcase all GUI elements related to the withdrawal frame
        self.withdrawframe.tkraise() #raise withdrawframe

        withlab = Label(withdrawframe, text="Withdraw Amount", font=("Arial", 12, "bold"), justify="center")
        withlab.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.withdraw=Entry()
        self.withdraw.place(relx=0.5,rely=0.4,anchor=CENTER)

        withbutamount=Button(withdrawframe,text="Withdraw",width=10,justify="center",
                             command=lambda:self.withamount(self.balance)) #call withamount() function if pressed
        withbutamount.place(relx=0.7,rely=0.6,anchor=CENTER)
        backbuttonwith = Button(withdrawframe, text="Back", justify="center", width=10,
                                  command=lambda: bankframe.tkraise()) #show bankframe frame/tab if pressed
        backbuttonwith.place(relx=0.5, rely=0.9, anchor=CENTER)

    def withamount(self,balance):
        try: #try getting the amount from the withdraw entry field
            amount=float(self.withdraw.get())
            if amount>self.balance: #if the amount is more than the balance produce an error
                messagebox.showerror("Error","Insufficient funds")
            else: #else deduct the amount from the balance and save to database
                self.balance = self.balance-amount
                self.balance=round(self.balance,2)
                cursor.execute("UPDATE users SET balance=? WHERE username=?", (self.balance, self.username))
                conn.commit()
                #update Bill's balance after withdrawal

                messagebox.showinfo("Success", f"Amount: {amount} was withdrawn")
        except ValueError: #if Bill places a string or a negative value, produce an error
            messagebox.showerror("Error","Please enter a valid amount")




    def showdep(self):
        self.depframe.tkraise()

        deplab = Label(depframe, text="Deposit Amount", font=("Arial", 12, "bold"), justify="center")
        deplab.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.depentry=Entry(depframe) #initialize entry field
        self.depentry.place(relx=0.5, rely=0.4, anchor=CENTER)

        depbutamount=Button(depframe, text="Deposit", width=10, justify="center", command=lambda:
                            self.depositamount(self.balance)) #call depositamount() function if pressed and pass Bill's balance by value
        depbutamount.place(relx=0.7,rely=0.6,anchor=CENTER)

        backbuttondep = Button(depframe, text="Back", justify="center", width=10,
                                command=lambda: bankframe.tkraise()) #show bankframe frame/tab if pressed
        backbuttondep.place(relx=0.5, rely=0.9, anchor=CENTER)
    def depositamount(self,balance):

        try: #try getting the amount from the withdraw entry field
            amount=float(self.depentry.get())
            if amount<=0:  #if the amount entered by Bill is negative or zero produce an error
                messagebox.showerror("Error","Amount must not be negative or zero")
            else: #else add the amount to his balance and save to database
                self.balance=self.balance+amount
                self.balance=round(self.balance,2)
                cursor.execute("UPDATE users SET balance=? WHERE username=?",(self.balance,self.username))
                conn.commit() #update Bill's balance after withdrawal
                messagebox.showinfo("Success",f"Amount: {amount} was deposited")
        except ValueError: #if Bill places a string, produce an error
            messagebox.showerror("Error","Please enter a valid amount")

class BudgetProgram:
    def __init__(self,username,identity):
        self.on_tree_select = None
        self.budgetframe=budgetframe
        self.username=username
        self.addframe=addframe
        self.identity=identity

        bankbutton = Button(budgetframe, text="Dep/with", justify="center", width=10,
                            command=lambda: bankframe.tkraise()) #show bankframe frame/tab if pressed
        bankbutton.place(relx=0.2, rely=0.95, anchor=CENTER)

        budgetbutton = Button(budgetframe, text="Budget", justify="center", width=10,
                              command=lambda: budgetframe.tkraise()) #show budgetframe frame/tab if pressed
        budgetbutton.place(relx=0.8, rely=0.95, anchor=CENTER)



    def showbudget(self): #showcases all GUI elements from budget tab
        self.budgetframe.tkraise()
        sendbudgetemailbutton = Button(budgetframe, text="Send Budget to Email", justify="center", width=20,
                              command=lambda: self.sendemail())
        sendbudgetemailbutton.place(relx=0.75, rely=0.90, anchor=CENTER)
        createbutton = Button(budgetframe, text="Create category", justify="center", width=20,
                            command=lambda: self.showadd())
        createbutton.place(relx=0.15, rely=0.05, anchor=CENTER)
        checkbalbutton = Button(budgetframe, text="Financial Projection", justify="center", width=20,
                              command=lambda: self.projection())
        checkbalbutton.place(relx=0.5, rely=0.05, anchor=CENTER)
        removebutton = Button(budgetframe, text="Remove category", justify="center", width=20,
                              command=lambda: self.removecat())
        removebutton.place(relx=0.85, rely=0.05, anchor=CENTER)
        scrollbary = Scrollbar(self.budgetframe, orient=VERTICAL)
        self.tree = Treeview(self.budgetframe, yscrollcommand=scrollbary.set)
        self.tree.place(x=50, y=80, width=300, height=350)
        scrollbary.place(x=350, y=80, width=20, height=350)
        scrollbary.configure(command=self.tree.yview)
        self.tree.configure(selectmode="extended")
        self.tree.bind("<<TreeviewSelect>>",self.on_tree_select)
        self.tree.configure(
            columns=(
                "Cat",
                "SubCat",
                "Date",
                "Amount",
            )
        )
        self.tree.heading("Cat", text="Category", command=lambda: Main.treeview_sort_column(self.tree, "Cat", False))
        self.tree.heading("SubCat", text="Sub-Category",
                          command=lambda: Main.treeview_sort_column(self.tree, "SubCat", False))
        self.tree.heading("Amount", text="Amount",
                          command=lambda: Main.treeview_sort_column(self.tree, "Amount", False))
        self.tree.heading("Date", text="Date to be paid", command=lambda: Main.treeview_sort_column(self.tree, "Date", False))


        self.tree.column("#0",width=0,stretch=False)
        self.tree.column("Cat",minwidth=0,width=4)
        self.tree.column("SubCat",minwidth=0, width=4)
        self.tree.column("Date",minwidth=0, width=5)
        self.tree.column("Amount",minwidth=0, width=5)



        self.displaydata() #refresh and show data

    def displaydata(self):
        cursor.execute("SELECT category,subcategory,date,amount"
                       " FROM budgetdata WHERE id IN (SELECT id FROM users WHERE username=?)",
                       (self.username,)) #selects all budgetary data corresponding to Bill's username/id
        result = cursor.fetchall()
        for data in result:
            self.tree.insert("", "end", values=data) #Place the data fetched by the database in the Treeview



    def showadd(self): #showcases every GUI element related to the frame for addition of new rows/budgetary data
        self.addframe.tkraise() #showcases the new frame/screen

        backbuttonadd = Button(addframe, text="Back", justify="center", width=10,
                               command=lambda: budgetframe.tkraise())
        backbuttonadd.place(relx=0.5, rely=0.9, anchor=CENTER)
        createrowlab=Label(addframe,text="Create Category",font=("Arial",12,"bold"),justify="center")
        createrowlab.place(relx=0.4,rely=0.05)
        catlab=Label(addframe,text="Category: ",font=("Arial", 9), justify="center")
        catlab.place(relx=0.2,rely=0.15)
        subcatlab = Label(addframe, text="Sub-Category: ", font=("Arial", 9), justify="center")
        subcatlab.place(relx=0.2, rely=0.3)
        datelab = Label(addframe, text="Date: ", font=("Arial", 9), justify="center")
        datelab.place(relx=0.2, rely=0.45)
        amountlab = Label(addframe, text="Amount: ", font=("Arial", 9), justify="center")
        amountlab.place(relx=0.2, rely=0.6)
        createrowbutton=Button(addframe,text="Create Category",justify="center", width=20,
                              command=lambda: self.addcat())

        createrowbutton.place(relx=0.5,rely=0.8)
        self.catentry=Entry(addframe) #allows user input for category
        self.catentry.place(relx=0.4,rely=0.15)
        self.subcatentry = Entry(addframe) #allows user input for subcategory
        self.subcatentry.place(relx=0.5,rely=0.3)
        self.amountentry = Entry(addframe) #allows user input for amount to be paid
        self.amountentry.place(relx=0.4, rely=0.6)
        self.dateentry = Entry(addframe) #allows user input for date to be paid
        self.dateentry.place(relx=0.4, rely=0.45)

    def validateemailsyntax(self,email): #https://docs.kickbox.com/docs/python-validate-an-email-address
    #validates whether the user follows correct email syntax e.g @abc.com is wrong while abc@gmail.com is correct
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    def sendemail(self):
        userpromptemail=simpledialog.askstring("Input","Enter your email address")

        #loops until it is cancelled
        while True:
            if not userpromptemail:
                break
            if userpromptemail and self.validateemailsyntax(userpromptemail):
                break  #if the user enters a valid email, break the loop

            #if the email is invalid, show an error and prompt again
            messagebox.showerror("Error", "Please enter a valid email address!")
            userpromptemail = simpledialog.askstring("Input", "Enter your email address")

        #if the user pressed cancel, stop further execution
        if not userpromptemail:
            return

        #fetch all budgetary data related to a specific user in a tuple of rows
        cursor.execute(
            "SELECT category, subcategory, date, amount FROM budgetdata WHERE id IN (SELECT id FROM users WHERE username=?)",
            (self.username,))
        budget_data = cursor.fetchall()



        #format the budgetary data into a readable message to be sent
        message="Budget data: \n\n"
        for data in budget_data:
            message += (f"Category: {data[0]}\n"
                        f"Sub-Category: {data[1]}\n"
                        f"Date: {data[2]}\n"
                        f"Amount: {data[3]}\n\n")

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("xxxx@gmail.com", "xxxx")
        # message to be sent
        # sending the mail
        s.sendmail("xxxx@gmail.com", userpromptemail, message)
        # terminating the session
        s.quit()



    def removecat(self): #removes selected rows containing budgetary data


        fordeletion=[] #empty list to store rows for deletion
        x=self.tree.selection() #Obtain all rows that were clicked with the mouse

        if len(x)!=0: #check if rows are selected
            sure=messagebox.askyesno("Confirm","Are you sure you want to delete the selected categories?") #prompt user
            if sure==True: #if Bill wants to delete the categories
                for i in x: #loop through each row
                    values=self.tree.item(i)["values"] #get the values of each row and column
                    if len(values)==4: #ensure the row has 4 columns
                        fordeletion.append((values[0],values[1],values[2],values[3])) #append the values of each column to the list
                    self.tree.delete(i) #remove row from Treeview

                for k in fordeletion: #loops through all values in the list and deletes from database
                    cursor.execute("DELETE FROM budgetdata WHERE category = ? AND subcategory = ? AND date = ? AND amount = ? "
                                   "AND id IN (SELECT id FROM users WHERE username=?)",
                                   (*k, self.username))
                    conn.commit()
                    #removes a row of budgetary data

                messagebox.showinfo("Success","Successful Deletion!")

                self.displaydata() #refresh the data to be displayed
            else:
                messagebox.showerror("Error","Cancelled deletion") #User pressed cancel
        else:
            messagebox.showerror("Error","Please select rows for deletion") #Bill did not click on rows to be deleted


    def addcat(self): #creates rows containing budgetary data
        category=self.catentry.get() #get value of category field
        subcategory=self.subcatentry.get() #get value of subcategory field
        amount=self.amountentry.get() #get value of amount field
        date=self.dateentry.get() #get value of date field
        def exceptions(): #function to check whether Bill inputted smth on each entry field
            match(bool(category),bool(subcategory),bool(amount),bool(date)):
                case(False,True,True,True):
                    messagebox.showerror("Error","Please enter a category")
                case(True,False,True,True):
                    messagebox.showerror("Error","Please enter a subcategory")
                case(True,True,False,True):
                    messagebox.showerror("Error","Please enter an amount")
                case(True,True,True,False):
                    messagebox.showerror("Error","Please enter a date")
                case(True,True,True,True):
                    return 1
        def checkdate(date): #Function to validate date format and check whether inputted date is older than the one at the time
            try:
                enteredtime=datetime.strptime(date,'%d/%m/%Y') #converts string to datetime object
                currenttime=datetime.now() #take the current date
                if enteredtime<currenttime: #evaluate if the entered time is smaller than the current time and produce an error
                    messagebox.showerror("Error","The date you entered for projection is invalid")
                    return 0
                return 1
            except:
                messagebox.showerror("Error","Please enter a valid date format (DD/MM/YYYY)")
                return 0
        returnvalue=exceptions() #place the value produced by exceptions function in the variable
        corrdate=checkdate(date) #place the value produced by checkdate function in the variable
        if returnvalue==1 and corrdate==1:  #if both values are True
            try:
                float(self.amountentry.get()) #ensure amount is a float
                cursor.execute("SELECT id FROM users WHERE username=?",(self.username,))
                userid=cursor.fetchone()
                messagebox.showinfo("Success", "Category was added to budget")

                cursor.execute("INSERT INTO budgetdata (id,category,subcategory,date,amount)VALUES (?,?,?,?,?)",
                               (userid[0],category,subcategory,date,amount))
                #add a new row containing budgetary data (e.g category, subcategory, date and amount to be paid)


                conn.commit() #commit changes
            except ValueError: #in case bill enteres a string
                messagebox.showerror("Error", "Please enter a valid amount")
    def projection(self):
        dates = [] #initialize an empty list to hold all the dates to be paid
        amounts=[] #initialize an empty list to hold all the amounts to be paid
        remainingbalanceframe.tkraise() #showcase the projection frame

        backbuttonbal = Button(remainingbalanceframe, text="Back", justify="center", width=10,
                               command=lambda: budgetframe.tkraise()) #go back to the budget frame
        backbuttonbal.place(relx=0.5, rely=0.9, anchor=CENTER)
        cursor.execute("SELECT date, amount"
                       " FROM budgetdata WHERE id IN (SELECT id FROM users WHERE username=?)",
                       (self.username,))
        fetchalldatesandamounts=cursor.fetchall()
        #Fetches all dates and amounts to be paid for each row of budgetary data

        if not fetchalldatesandamounts:
            messagebox.showerror("Error", "No budgetary data to project") #produce error if nothing is found

        for row in fetchalldatesandamounts:
            dates.append(datetime.strptime(row[0], '%d/%m/%Y')) #append the values of each row related to dates to be paid
            amounts.append(float(row[1])) #append the values of each row related to amounts to be paid

        totalamountsspending=sum(amounts) #take the sum of values of the list
        numdays=abs((max(dates)-min(dates))).days+1 #take the difference in days between the furthest and closest date
        avgspending=totalamountsspending/numdays #calculate average spending
        #https://stackoverflow.com/questions/8419564/difference-between-two-dates-in-python


        cursor.execute("SELECT balance FROM users WHERE username = ?", (self.username,))
        currball = cursor.fetchone()

        daysuntilout = currball[0] / avgspending #calculate when his money will run out based on his balance
        projection = datetime.now() + timedelta(days=daysuntilout) #create a projection

        projectionlabel = Label(remainingbalanceframe, text=f"Average Daily Spending: {avgspending:.2f}\n"
                                                       f"Projected Date When Money Will Run Out: {projection.strftime('%d/%m/%Y')}",
                            font=("Arial", 12, "bold"))
        projectionlabel.place(relx=0.5, rely=0.3, anchor=CENTER) #place average spending and projected date in the label



        #plot the spending trends graph

        plt.plot(dates, amounts, label="Daily Spending")
        plt.axhline(avgspending, color='r', linestyle='-', label="Average Daily Spending")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Spending Projection")


#instantiate the Main class to build the main menu, create-account, and login screens
main = Main(mainmenuframe, createaccframe, loginframe)

mainmenuframe.tkraise()
GUI.mainloop() #exit the GUI
conn.commit() #commit changes
conn.close() #close database
uploadtodrive() #call uploadtodrive()