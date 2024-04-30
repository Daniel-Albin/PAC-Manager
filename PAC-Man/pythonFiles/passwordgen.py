from flask import Flask, request, jsonify
import secrets
import string

app = Flask(__name__)

def password_gen(password_length):

    characters = string.printable.replace(' ','')

    secure_password = ''.join(secrets.choice(characters) for i in range(password_length))

    return secure_password

@app.route('/password_gen', methods=['POST'])
def generate_password():
    data = request.get_json()
    password_length = data.get('password_length')
    if not password_length:
        password_length = 12  
    password = password_gen(password_length)
    return jsonify({"password": password})
