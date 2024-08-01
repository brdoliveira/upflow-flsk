from flask import render_template, request, redirect, url_for, flash, send_from_directory, session
from werkzeug.security import check_password_hash
from app import app, db
from models import Contact, Employee
from decorators import login_required, permission_required
from enums import PermissionLevel

@app.route('/')
def home():
    if session.get('logged_in'):
        return render_template('dashboard.html')
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

@app.route('/contacts', methods=['GET'])
@login_required
@permission_required(PermissionLevel.ADMIN)
def list_contacts():
    contacts = Contact.query.all()
    return render_template('list_contacts.html', contacts=contacts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        employee = Employee.query.filter_by(Email=email).first()
        
        if employee and check_password_hash(employee.Password, password):
            session['logged_in'] = True
            session['employee_id'] = employee.EmployeeID
            session['permission_level_id'] = employee.PermissionLevelID
            session['company_id'] = employee.CompanyID
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('employee_id', None)
    session.pop('permission_level_id', None)
    session.pop('company_id', None)
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('home'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)