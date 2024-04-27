from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'database_uri_here' #Needs to be updated with our PostgreSQL URI still
db = SQLAlchemy(app)

class VaultEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

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
        return jsonify({'message': 'Entry added successfully'})
    except Exception as e:
        # If an error occurs, rollback the session
        db.session.rollback()
        return jsonify({'message': 'Error occurred while adding entry', 'error': str(e)})

@app.route('/editVault', methods=['POST'])
def editVault():
    data = request.json
    website = data.get('website')
    username = data.get('username')
    password = data.get('password')
    ID = data.get('id')  # Assuming the frontend sends the ID to identify the entry to edit
    vault_entry = VaultEntry.query.filter_by(id=ID).first()

    if vault_entry:
        vault_entry.website = website
        vault_entry.username = username
        vault_entry.password = password
        try:
            db.session.commit()
            return jsonify({'message': 'Entry edited successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error occurred while editing entry', 'error': str(e)})
    else:
        return jsonify({'message': 'Entry not found'})

@app.route('/deleteFromVault', methods=['POST'])
def deleteFromVault():
    data = request.json
    ID = data.get('id')  # Assuming the frontend sends the ID to identify the entry to delete
    vault_entry = VaultEntry.query.filter_by(id=ID).first()

    if vault_entry:
        try:
            db.session.delete(vault_entry)
            db.session.commit()
            return jsonify({'message': 'Entry deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error occurred while deleting entry', 'error': str(e)})
    else:
        return jsonify({'message': 'Entry not found'})

if __name__ == '__main__':
    app.run(debug=True)
