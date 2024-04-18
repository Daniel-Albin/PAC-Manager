import psycopg2
#from pythonFiles.Pac_Man_encryption import hash_master_password, generate_salt, verify_hash_password
from Pac_Man_encryption import hash_master_password, generate_salt, verify_hash_password, encrypt_password, decrypt_password

def insert_to_database(email, password):
    conn = psycopg2.connect("dbname=pacmanager user=postgres password=goodyear")
    cur = conn.cursor()
    #generate salt to use for hashing
    salt = generate_salt()
    cur.execute("INSERT INTO pacusers (email, masterpass, salt) VALUES (%s, %s, %s);", (email, hash_master_password(password), salt))
    conn.commit()
    cur.close()
    conn.close()

def insert_otp(email, otp):
    conn = psycopg2.connect("dbname=pacmanager user=postgres password=goodyear")
    cur = conn.cursor()
    cur.execute("UPDATE pacusers SET otpkey = %s WHERE email = %s;", (otp, email))
    conn.commit()
    cur.close()
    conn.close()

def verify_user(email, password):
    conn = psycopg2.connect("dbname=pacmanager user=postgres password=goodyear")
    cur = conn.cursor()
    #find hashed password matching email for verification
    cur.execute("SELECT masterpass FROM pacusers WHERE email = %s;",[email])
    hash = cur.fetchall()
    valid = verify_hash_password(hash[0][0], password)
    cur.close()
    conn.close()
    return valid

def getTOTP(email):
    conn = psycopg2.connect("dbname=pacmanager user=postgres password=goodyear")
    cur = conn.cursor()
    #find OTPkey
    cur.execute("SELECT otpkey FROM pacusers WHERE email = %s;",[email])
    key = cur.fetchall()
    totp = key[0][0]
    cur.close()
    conn.close()
    return totp

def addCredentials(email, url, username, password, name):
    conn = psycopg2.connect("dbname=pacmanager user=postgres password=goodyear")
    cur = conn.cursor()
    cur.execute("SELECT masterpass, salt FROM pacusers WHERE email = %s;",[email])
    res = cur.fetchall()
    masterpass = res[0][0]
    cur.execute("INSERT INTO pacvault (email, url, username, password, name) VALUES (%s, %s, %s, %s);", (email, url, username, encrypt_password(password, masterpass, generate_salt(), name)))
    conn.commit()
    cur.close()
    conn.close()
    return 

def getCredentials(email, accountid):
    conn = psycopg2.connect("dbname=pacmanager user=postgres password=goodyear")
    cur = conn.cursor()
    cur.execute("SELECT url, username, password , name FROM pacvault WHERE email = %s AND accountid = %s;",(email, accountid))
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res[0]

def updateCredentials(email, accountid, url, username, password):
    conn = psycopg2.connect("dbname=pacmanager user=postgres password=goodyear")
    cur = conn.cursor()
    cur.execute("SELECT masterpass, salt FROM pacusers WHERE email = %s;",[email])
    res = cur.fetchall()
    masterpass = res[0][0]
    cur.execute("UPDATE pacvault SET url = %s, username = %s, password = %s WHERE email = %s AND accountid = %s;", (url, username, encrypt_password(password, masterpass, generate_salt()), email, accountid))
    conn.commit()
    cur.close()
    conn.close()
    return

