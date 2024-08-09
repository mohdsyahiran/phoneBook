from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'phone_number': c.phone_number} for c in contacts])

@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    new_contact = Contact(name=data['name'], phone_number=data['phone_number'])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({'message': 'Contact added'}), 201

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.get_json()
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    contact.name = data['name']
    contact.phone_number = data['phone_number']
    db.session.commit()
    return jsonify({'message': 'Contact updated'})

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted'})

if __name__ == '__main__':
    app.run(debug=True)
