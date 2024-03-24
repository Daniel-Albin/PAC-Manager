import re

def password_check(password):
    if len(password) < 8: #makes sure password is atleast of length 8
        return False
    
    if not re.search(r'[A-Z]', password): #checks to see if password contains atleast 1 capital letter
        return False
    
    if not re.search(r'[a-z]', password): #checks to see if pasword contains atleast 1 lowercase letter 
        return False
    
    if not re.search(r'/d', password): #checks to see if password contains atleast 1 digit
        return False
    
    if not any(not c.isalnum() for c in password): #checks to see if passwrod contains atleast 1 special character 
        return False
    
    return True


