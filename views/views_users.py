from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from app import app, db
from models import PermissionLevel, Employee, Company
from decorators import login_required, permission_required
from enums import PermissionLevel as pl

# Rota para listar empregados
@app.route('/employees', methods=['GET'])
@login_required
@permission_required(pl.VIEWER)
def list_employees():
    """
    Lista todos os empregados.
    
    Requer:
    - Usuário autenticado.
    - Permissão de VISUALIZADOR.
    """
    employees = Employee.query.all()
    return render_template('list_employees.html', employees=employees)

# Rota para adicionar empregado
@app.route('/employees/add', methods=['GET', 'POST'])
@login_required
@permission_required(pl.EDITOR)
def add_employee():
    """
    Adiciona um novo empregado.
    
    Métodos:
    - GET: Renderiza o formulário de empregado.
    - POST: Processa o envio do formulário e salva o novo empregado no banco de dados.
    
    Requer:
    - Usuário autenticado.
    - Permissão de EDITOR.
    """
    companies = Company.query.all()

    if session.get('permission_level_id') == pl.ADMIN.value:
        permission_levels = PermissionLevel.query.all()
    else:
        permission_levels = PermissionLevel.query.filter(PermissionLevel.LevelID != pl.ADMIN.value).all()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        phone = request.form['phone']
        if session.get('permission_level_id') == pl.ADMIN.value:
            company_id = request.form['company_id']
        else:
            company_id = session.get('company_id')
        permission_level_id = request.form['permission_level_id']

        new_employee = Employee(Name=name, Email=email, Password=password, Phone=phone, CompanyID=company_id, PermissionLevelID=permission_level_id)
        db.session.add(new_employee)
        db.session.commit()
        flash('Funcionário adicionado com sucesso!', 'success')
        return redirect(url_for('list_employees'))
    
    return render_template('employee_form.html', companies=companies, permission_levels=permission_levels, employee=None)

# Rota para editar empregado
@app.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
@login_required
@permission_required(pl.EDITOR)
def edit_employee(employee_id):
    """
    Edita um empregado existente.
    
    Métodos:
    - GET: Renderiza o formulário de empregado com dados existentes.
    - POST: Processa o envio do formulário e atualiza o empregado no banco de dados.
    
    Requer:
    - Usuário autenticado.
    - Permissão de EDITOR.
    """
    employee = Employee.query.get_or_404(employee_id)
    companies = Company.query.all()

    if session.get('permission_level_id') == pl.ADMIN.value:
        permission_levels = PermissionLevel.query.all()
    else:
        permission_levels = PermissionLevel.query.filter(PermissionLevel.LevelID != pl.ADMIN.value).all()

    if request.method == 'POST':
        employee.Name = request.form['name']
        employee.Email = request.form['email']
        if request.form['password']:
            employee.Password = generate_password_hash(request.form['password'])
        employee.Phone = request.form['phone']
        if session.get('permission_level_id') == pl.ADMIN.value:
            employee.CompanyID = request.form['company_id']
        else:
            employee.CompanyID = session.get('company_id')
        employee.PermissionLevelID = request.form['permission_level_id']

        db.session.commit()
        flash('Funcionário atualizado com sucesso!', 'success')
        return redirect(url_for('list_employees'))
    
    return render_template('employee_form.html', companies=companies, permission_levels=permission_levels, employee=employee)

# Rota para deletar empregado
@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
@login_required
@permission_required(pl.EDITOR)
def delete_employee(employee_id):
    """
    Deleta um empregado.
    
    Métodos:
    - POST: Processa a deleção do empregado.
    
    Requer:
    - Usuário autenticado.
    - Permissão de EDITOR.
    """
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Funcionário deletado com sucesso!', 'success')
    return redirect(url_for('list_employees'))
