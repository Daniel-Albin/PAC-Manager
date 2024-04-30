from flask import Flask, redirect, render_template, request, session, jsonify
from pythonFiles.OTP import gen_OTP_account, verify_OTP
from pythonFiles.Database import insert_to_database, verify_user, addCredentials, getCredentials, updateCredentials, deleteCredentials, getTOTP, valid_email, getPass
from pythonFiles.strengthchecking import password_check, password_print
from pythonFiles.Pac_Man_encryption import decrypt_password
from pythonFiles.passwordgen import password_gen

app = Flask(__name__)

app.secret_key = 'PAC-MANAGER'

#name and define function for each directory of website
@app.route('/')
def home():
    return render_template('pachomepage.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup-retry', methods=['GET', 'POST'])
def retrySignup():
    error_message = session.get('error_message', None)
    return render_template("errorsignup.html", error_message=error_message)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/OTPnewuser', methods=['POST'])
def newuserOTP():
    email = request.form["email"].lower()
    password1 = request.form["masterpass1"]
    password2 = request.form["masterpass2"]
    #check if email is valid
    if not valid_email(email):
        session['error_message'] = "Email is not valid" 
        return redirect('/signup-retry')
    
    try: 
        getPass(email)
        session['error_message'] = "Email already exists" 
        return redirect('/signup-retry')
    except:
        #check if user correctly entered password both times
        if  password1 == password2:
            pstrength = password_check(password1)
            if pstrength < 5:
                session['error_message'] = "Weak password, Have: 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character"
                return redirect('/signup-retry')
            else:
                insert_to_database(email, password1)
                gen_OTP_account(email)
                image = "static/" + email + ".png"
                session['image'] = image
                session['email'] = email
                return render_template('newOTP.html', image=image)
        else:
            session['error_message'] = "Passwords do not match" 
            return redirect('/signup-retry')

@app.route('/OTP', methods=['POST'])
def OTP():
    email = request.form["email"].lower()
    password = request.form["masterpass"]
    #search databse for entry matching email/pass credential
    try:
        valid = verify_user(email, password)
        session['email'] = email
    except:
        valid = False
    #if SQL Query finds a math valid = true
    if valid:
        return render_template("OTP.html")
    else:
       return render_template("errorlogin.html")

@app.route('/new-user-sign-in', methods=['GET', 'POST'])
def newsignin():
    image = session.get('image', None)
    email = session.get('email', None)
    totp = getTOTP(str(email)) 
    code = request.form["OTP"]

    if verify_OTP(code, totp):
        return redirect ('/PAC-Vault')
    else:
        return render_template('newOTP.html', image=image)
    
@app.route('/user-sign-in', methods=['POST'])
def signin():
    email = session.get('email', None)
    totp = getTOTP(str(email)) 
    code = request.form["OTP"]

    if verify_OTP(code, totp):
        return redirect('/PAC-Vault')
    else:
        return render_template('OTP.html')
    
@app.route('/PAC-Vault', methods=['GET', 'POST'])
def pVault():
    email = session.get('email', None)
    password = getPass(email)

    accountid = getCredentials(email)
    decryptCred =[]
    for cred in accountid:
        cred = list(cred)
        cred[2] = decrypt_password(cred[2], password)
        decryptCred.append(cred)

    return render_template("pacuserhomepage.html", accountid=decryptCred)

@app.route('/addTo-Vault', methods=['GET', 'POST'])
def addToVault():
    email = session.get('email', None)
    data = request.json

    name = data.get('name')
    url = data.get('url')
    username = data.get('username')
    password = data.get('password')

    addCredentials(email, url, username, password, name)

    return redirect('/PAC-Vault')

@app.route('/update-Vault', methods=['GET', 'POST'])
def updateVault():
    email = session.get('email', None)
    data = request.json

    accountid = data.get('id')
    url = data.get('url')
    username = data.get('username')
    password = data.get('password')
        
    updateCredentials(email, accountid, url, username, password)

    return redirect('/PAC-Vault')

@app.route('/deleteFromVault', methods=['POST'])
def deleteFromVault():
    data = request.json
    ID = data.get('id')

    deleteCredentials(ID)

    return redirect('/PAC-Vault')

@app.route('/password_check', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password')
    strength = password_check(password)
    msg = password_print(strength)
    return jsonify({"strength": msg})

@app.route('/password_gen', methods=['POST'])
def generate_password():
    data = request.get_json()
    password_length = data.get('password_length')
    if not password_length:
        password_length = 12  
    password = password_gen(password_length)
    return jsonify({"password": password})


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    account = session.get('email', None)
    image = "static/" + account + ".png"
    return render_template("pacprofile.html", image=image, account=account, )

@app.route('/help')
def help():
    return render_template("help.html")

if __name__ == "__main__":
    #turn off debug when running with host = 0.0.0.0
    app.run(ssl_context='adhoc', host='0.0.0.0')
    #app.run(debug=True)
