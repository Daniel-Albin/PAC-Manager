import re

def password_check(password):
    strength = 0 

    if len(password) > 8: #makes sure password is atleast of length 8
        strength +=1 
    
    if re.search(r'[A-Z]', password): #checks to see if password contains atleast 1 capital letter
        strength +=1 
    
    if re.search(r'[a-z]', password): #checks to see if pasword contains atleast 1 lowercase letter 
        strength +=1 
    
    if re.search(r'\d', password): #checks to see if password contains atleast 1 digit
        strength +=1 
    
    if any(not c.isalnum() for c in password): #checks to see if passwrod contains atleast 1 special character 
        strength +=1 
    
    return strength

def password_print(strength):
    if strength == 5:
        return("Password is very strong!")
    
    elif strength >= 3:
        return("Password is strong.")
    
    elif strength >= 2:
        return("Password is moderate.")
    
    elif strength >= 1:
        return("Password is weak.")
    
    else:
        return("Password is very weak.")