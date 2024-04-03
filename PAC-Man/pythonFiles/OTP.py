import pyotp, qrcode, os, shutil
from pythonFiles.Database import insert_otp

#For new user, creates a personalized google authenticator sign in
#Generates QR code for that user
def gen_OTP_account(email):
    key = pyotp.random_base32()
    totp = pyotp.totp.TOTP(key).provisioning_uri(name=email, issuer_name='Pac-Manager')
    #-----> Needs to be entered into the database for each user
    insert_otp(email, totp)

    uri = pyotp.totp.TOTP(key).provisioning_uri(name=email,
                                            issuer_name="Pac-Manager")
    code = email + ".png"
    qrcode.make(uri).save(code)
    shutil.move("/Users/visharipal/Desktop/Spring 2024/Software Engineering/PAC-Man/" + code, "/Users/visharipal/Desktop/Spring 2024/Software Engineering/PAC-Man/static")

#verify that the user code is valid
def verify_OTP(passcode, totp):
    totp = pyotp.parse_uri(totp)
    return(totp.verify(passcode))

def deleteQR(email):
    os.system("rm /Users/visharipal/Desktop/Spring\ 2024/Software\ Engineering/PAC-Man/static" + email + ".png")