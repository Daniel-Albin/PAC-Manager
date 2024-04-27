from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Establishing connection to PostgreSQL database
conn = psycopg2.connect("dbname=postgres user=postgres password=goodyear host=pacmanager.c9o2e2iucr6i.us-east-1.rds.amazonaws.com port=5432")
cur = conn.cursor()

@app.route('/addToVault', methods=['POST'])
def addToVault():
    data = request.json
    website = data.get('website')
    username = data.get('username')
    password = data.get('password')

    try:
        cur.execute("INSERT INTO vault_entries (website, username, password) VALUES (%s, %s, %s)", (website, username, password))
        conn.commit()
        return jsonify({'message': 'Entry added successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error occurred while adding entry', 'error': str(e)})

@app.route('/editVault', methods=['POST'])
def editVault():
    data = request.json
    website = data.get('website')
    username = data.get('username')
    password = data.get('password')
    ID = data.get('id')

    try:
        cur.execute("UPDATE vault_entries SET website=%s, username=%s, password=%s WHERE id=%s", (website, username, password, ID))
        conn.commit()
        return jsonify({'message': 'Entry edited successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error occurred while editing entry', 'error': str(e)})

@app.route('/deleteFromVault', methods=['POST'])
def deleteFromVault():
    data = request.json
    ID = data.get('id')

    try:
        cur.execute("DELETE FROM vault_entries WHERE id=%s", (ID,))
        conn.commit()
        return jsonify({'message': 'Entry deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error occurred while deleting entry', 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
