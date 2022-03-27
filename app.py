from flask import Flask, render_template, request
import pyrebase

import urllib3

app = Flask(__name__)

# REQUIRED
# Grab Info From firebase and copy data from firebaseConfig Section
firebaseConfig = {
    'apiKey': "AIzaSyC5p9pMOWMAanWufHwrY44q33BPDrnDoBo",
    'authDomain': "contact-me-fb.firebaseapp.com",
    'databaseURL': "https://contact-me-fb-default-rtdb.firebaseio.com",
    'projectId': "contact-me-fb",
    'storageBucket': "contact-me-fb.appspot.com",
    'messagingSenderId': "248174360827",
    'appId': "1:248174360827:web:6e07eafb0ae611d651185e"
}

# initilize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# Firebase Auth
auth = firebase.auth()

# FireBase Database
db = firebase.database()

# Firebase Storage
storage = firebase.storage()


@app.route('/')
def index():
    form_LOG_IN = LogIn()
    form_SIGN_UP = SignUp()
    return render_template('Home.html', form_LOG_IN=form_LOG_IN, form_SIGN_UP=form_SIGN_UP)


@app.route('/login', methods=['GET', 'POST'])
def LogIn():
    if request.method == 'POST':
        email = request.form["USER_EMAIL"]
        password = request.form["USER_PASSWORD"]
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('TestSignOut.html')
        except:
            return render_template('Home.html')
    return render_template('Home.html')


@app.route('/signup', methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        email = request.form["NEW_USER_EMAIL"]
        password = request.form["NEW_USER_PASSWORD"]
        try:
            auth.create_user_with_email_and_password(email, password)
            return render_template('TestSignOut.html')
        except:
            return 'Email Already in use'
    return render_template('Home.html')


@app.route('/TestSignOut.html', methods=['GET', 'POST'])
def SignOut():
    if request.method == 'POST':
        auth.current_user = None
    return render_template('Home.html')


@app.route('/user_home_page', methods=['GET', 'POST'])
def userContactList():
    form_ADD_CONTACT = addContact()
    form_EDIT_CONTACT = editContact()
    form_DELETE_CONTACT = deleteContact()
    Contacts = auth.current_user
    ContactList = db.child(auth.current_user).child("CONTACT_LIST").child("First_Name").get()
    for Contacts in ContactList.each():
        Contacts.key()
        Contacts.val()
    return render_template('TestSignOut.html', form_ADD_CONTACT=form_ADD_CONTACT, form_EDIT_CONTACT=form_EDIT_CONTACT,
                           form_DELETE_CONTACT=form_DELETE_CONTACT)


@app.route('/add_Contact', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        NEW_CONTACT_firstName = request.form['NEW_CONTACT_firstName']
        NEW_CONTACT_lastName = request.form['NEW_CONTACT_lastName']
        NEW_CONTACT_phoneNumber = request.form['NEW_CONTACT_phoneNumber']
        NEW_CONTACT_address = request.form['NEW_CONTACT_address']
        try:
            data = {"First_Name": NEW_CONTACT_firstName,
                    "Last_Name": NEW_CONTACT_lastName,
                    "Phone_Number": NEW_CONTACT_phoneNumber,
                    "Address": NEW_CONTACT_address}
            db.child(auth.current_user).child("CONTACT_LIST").child("First_Name").set(data)
            render_template('TestSignOut.html')
        except:
            print('DATABASE LOGGING FAILURE')
    render_template('TestSignOut.html')


@app.route('/edit_Contact', methods=['GET', 'POST'])
def editContact():
    Contact = db.child(auth.current_user).child("CONTACT_LIST").child("First_Name")
    if request.method == 'POST':
        EDIT_CONTACT_firstName = request.form['EDIT_CONTACT_firstName']
        EDIT_CONTACT_lastName = request.form['EDIT_CONTACT_lastName']
        EDIT_CONTACT_phoneNumber = request.form['EDIT_CONTACT_phoneNumber']
        EDIT_CONTACT_address = request.form['EDIT_CONTACT_address']
        try:
            if len(EDIT_CONTACT_firstName) != 0:
                Contact.update("First_Name")
            if len(EDIT_CONTACT_lastName) != 0:
                Contact.update("Last_Name")
            if len(EDIT_CONTACT_phoneNumber) != 0:
                Contact.update("Phone_Number")
            if len(EDIT_CONTACT_firstName) != 0:
                Contact.update("Address")
        except:
            print('DATABASE DATA CHANGE FAILURE')
        return render_template('TestSignOut.html')
    return render_template('TestSignOut.html')


@app.route('/delete_Contact', methods=['GET','POST'])
def deleteContact():
    Contact = db.child(auth.current_user).child("CONTACT_LIST").child("First_Name")
    if request.method == 'POST':
        DELETE_CONTACT = request.form['DELETE_CONFIRMATION_NAME']
        CONFIRMATION_NAME = db.child(auth.current_user).child("CONTACT_LIST").child("First_Name").get()
        if CONFIRMATION_NAME == request.form['DELETE_CONFIRMATION_NAME']:
            Contact.remove()
    return render_template('TestSignOut.html')


if __name__ == '__main__':
    app.run()
