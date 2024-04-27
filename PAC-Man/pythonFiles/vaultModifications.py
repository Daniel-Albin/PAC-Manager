from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'  # I need to replace this with PostgreSQL connection URI
db = SQLAlchemy(app)

class VaultEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

@app.route('/addToVault', methods=['POST'])
def addToVault():
    data = request.json
    website = data.get('website')
    username = data.get('username')
    password = data.get('password')
    
    # Create a new VaultEntry object
    new_entry = VaultEntry(website=website, username=username, password=password)
    
    try:
        # Add the new entry to the database session
        db.session.add(new_entry)
        # Commit the session to save the changes to the database
        db.session.commit()
        # Retrieve the ID of the newly inserted record
        new_id = new_entry.id
        return jsonify({'message': 'Entry added successfully', 'id': new_id})
    except Exception as e:
        # If an error occurs, rollback the session
        db.session.rollback()
        return jsonify({'message': 'Error occurred while adding entry', 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/editVault', methods=['POST'])
def editVault(website, username, password, ID, vault):
    vault[ID] = (website, username, password)
    print("Login information updated successfully")
    #Updates previously entered information
    print("Editing vault:", request.json)
    return jsonify({"message": "Information edited in the vault"})

@app.route('/deleteFromVault', methods=['POST'])
def deleteFromVault(website, username, password, ID, vault):
    if ID in vault:
        del vault[ID]
        print("Entry deleted successfully.")
    else:
        print("Invalid Entry ID Provided")

if __name__ == '__main__':
    app.run(debug=True)


