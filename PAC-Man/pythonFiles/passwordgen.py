import secrets
import string

def password_gen(password_length):
    #characters = string.printable.replace(' ', '').replace('\x0b', '').replace('    ','')
    characters = string.ascii_letters + string.digits + string.punctuation.replace(' ','').replace('   ','').replace('|','').replace('(','').replace(')','').replace('{','').replace('}','').replace('[','').replace(']','')
    while True:
        secure_password = ''.join(secrets.choice(characters) for I in range(password_length))
        if len(secure_password) == password_length:
            return secure_password