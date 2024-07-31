from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import app, db
from models import PermissionLevel, Employee, Company

@app.route('/employees', methods=['GET'])
def list_employees():
    employees = Employee.query.all()
    return render_template('list_employees.html', employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    companies = Company.query.all()
    permission_levels = PermissionLevel.query.all()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        phone = request.form['phone']
        company_id = request.form['company_id']
        permission_level_id = request.form['permission_level_id']

        new_employee = Employee(Name=name, Email=email, Password=password, Phone=phone, CompanyID=company_id, PermissionLevelID=permission_level_id)
        db.session.add(new_employee)
        db.session.commit()
        flash('Funcionário adicionado com sucesso!', 'success')
        return redirect(url_for('list_employees'))
    
    return render_template('employee_form.html', companies=companies, permission_levels=permission_levels, employee=None)

@app.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    companies = Company.query.all()
    permission_levels = PermissionLevel.query.all()

    if request.method == 'POST':
        employee.Name = request.form['name']
        employee.Email = request.form['email']
        if request.form['password']:
            employee.Password = generate_password_hash(request.form['password'])
        employee.Phone = request.form['phone']
        employee.CompanyID = request.form['company_id']
        employee.PermissionLevelID = request.form['permission_level_id']

        db.session.commit()
        flash('Funcionário atualizado com sucesso!', 'success')
        return redirect(url_for('list_employees'))
    
    return render_template('employee_form.html', companies=companies, permission_levels=permission_levels, employee=employee)

@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Funcionário deletado com sucesso!', 'success')
    return redirect(url_for('list_employees'))
