from flask import render_template, request, redirect, url_for, flash, send_from_directory, session
from werkzeug.security import check_password_hash
from app import app, db
from models import Contact, Employee
from decorators import login_required, permission_required
from enums import PermissionLevel as pl

# Rota para a página inicial
@app.route('/')
def home():
    """
    Renderiza a página inicial. Se o usuário estiver logado, renderiza o dashboard.
    """
    if session.get('logged_in'):
        return render_template('dashboard.html')
    return render_template('home.html')

# Rota para a página de serviços
@app.route('/services')
def services():
    """
    Renderiza a página de serviços.
    """
    return render_template('services.html')

# Rota para a página sobre
@app.route('/about')
def about():
    """
    Renderiza a página sobre.
    """
    return render_template('about.html')

# Rota para a página de contato
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Renderiza a página de contato e lida com o envio de formulários.
    
    Métodos:
    - GET: Renderiza o formulário de contato.
    - POST: Processa o envio do formulário e salva a mensagem de contato no banco de dados.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        new_contact = Contact(Name=name, Email=email, Message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Rota para listar mensagens de contato
@app.route('/contacts', methods=['GET'])
@login_required
@permission_required(pl.ADMIN)
def list_contacts():
    """
    Lista todas as mensagens de contato.
    
    Requer:
    - Usuário logado.
    - Permissão de ADMIN.
    """
    contacts = Contact.query.all()
    return render_template('list_contacts.html', contacts=contacts)

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Lida com o processo de login.
    
    Métodos:
    - GET: Renderiza o formulário de login.
    - POST: Autentica o usuário e inicia uma sessão se for bem-sucedido.
    """
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

# Rota para logout
@app.route('/logout')
def logout():
    """
    Faz o logout do usuário e redireciona para a página inicial.
    """
    session.pop('logged_in', None)
    session.pop('employee_id', None)
    session.pop('permission_level_id', None)
    session.pop('company_id', None)
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('home'))

# Rota para servir arquivos
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    """
    Serve um arquivo do diretório de uploads.
    """
    return send_from_directory('uploads', nome_arquivo)
