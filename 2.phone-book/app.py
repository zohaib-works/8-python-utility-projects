from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Contact {self.name}>'

@app.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        contacts = Contact.query.filter(
            (Contact.name.contains(search))
            | (Contact.phone.contains(search) )
            | (Contact.email.contains(search))
            | (Contact.address.contains(search))
            ).order_by(Contact.name).all()
    else:
        contacts = Contact.query.all()
    return render_template('website/index.html', contacts=contacts, search=search)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        if not name or not email or not address:
            flash('Name, email, and address are required', 'danger')
            return redirect(url_for('create'))
        
        existing_contact = Contact.query.filter_by(email=email).first()
        if existing_contact:
            flash('Email already exists', 'danger')
            return redirect(url_for('create'))
        
        if phone:
            existing_contact = Contact.query.filter_by(phone=phone).first()
            if existing_contact:
                flash('Phone number already exists', 'danger')
                return redirect(url_for('create'))

        contact = Contact(name=name, phone=phone, email=email, address=address)
        db.session.add(contact)
        db.session.commit()
        flash('Contact created successfully', 'success')
        return redirect(url_for('index'))
    return render_template('website/create.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        if not name or not email or not address:
            flash('Name, email, and address are required', 'danger')
            return redirect(url_for('edit', id=id))
        
        existing_contact = Contact.query.filter_by(email=email).first()
        if existing_contact and existing_contact.id != id:
            flash('Email already exists', 'danger')
            return redirect(url_for('edit', id=id))
        
        if phone:
            existing_contact = Contact.query.filter_by(phone=phone).first()
            if existing_contact and existing_contact.id != id:
                flash('Phone number already exists', 'danger')
                return redirect(url_for('edit', id=id))

        contact.name = name
        contact.phone = phone
        contact.email = email
        contact.address = address
        db.session.commit()
        flash('Contact updated successfully', 'success')
        return redirect(url_for('index'))
    return render_template('website/edit.html', contact=contact)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact deleted successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)