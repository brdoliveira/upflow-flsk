from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app import app, db
from models import Contact, Employee

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        new_contact = Contact(Name=name, Email=email, Message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        employee = Employee.query.filter_by(Email=email).first()
        
        if employee and check_password_hash(employee.Password, password):
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('login.html')
