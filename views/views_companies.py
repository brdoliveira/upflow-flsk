from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Company
from decorators import login_required, permission_required
from enums import PermissionLevel as pl

# Rota para listar empresas
@app.route('/companies', methods=['GET'])
@login_required
@permission_required(pl.ADMIN)
def list_companies():
    """
    Lista todas as empresas.
    
    Requer:
    - Usuário autenticado.
    - Permissão de ADMIN.
    """
    companies = Company.query.all()
    return render_template('list_companies.html', companies=companies)

# Rota para adicionar empresa
@app.route('/companies/add', methods=['GET', 'POST'])
@login_required
@permission_required(pl.ADMIN)
def add_company():
    """
    Adiciona uma nova empresa.
    
    Métodos:
    - GET: Renderiza o formulário de empresa.
    - POST: Processa o envio do formulário e salva a nova empresa no banco de dados.
    
    Requer:
    - Usuário autenticado.
    - Permissão de ADMIN.
    """
    if request.method == 'POST':
        name = request.form['name']
        cnpj = request.form['cnpj']
        address = request.form['address']
        phone = request.form['phone']
        foundation_date = request.form['foundation_date']
        sector = request.form['sector']

        new_company = Company(Name=name, CNPJ=cnpj, Address=address, Phone=phone, FoundationDate=foundation_date, Sector=sector)
        db.session.add(new_company)
        db.session.commit()
        flash('Empresa adicionada com sucesso!', 'success')
        return redirect(url_for('list_companies'))
    
    return render_template('company_form.html', company=None)

# Rota para editar empresa
@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
@login_required
@permission_required(pl.ADMIN)
def edit_company(company_id):
    """
    Edita uma empresa existente.
    
    Métodos:
    - GET: Renderiza o formulário de empresa com dados existentes.
    - POST: Processa o envio do formulário e atualiza a empresa no banco de dados.
    
    Requer:
    - Usuário autenticado.
    - Permissão de ADMIN.
    """
    company = Company.query.get_or_404(company_id)
    if request.method == 'POST':
        company.Name = request.form['name']
        company.CNPJ = request.form['cnpj']
        company.Address = request.form['address']
        company.Phone = request.form['phone']
        company.FoundationDate = request.form['foundation_date']
        company.Sector = request.form['sector']

        db.session.commit()
        flash('Empresa atualizada com sucesso!', 'success')
        return redirect(url_for('list_companies'))
    
    return render_template('company_form.html', company=company)

# Rota para deletar empresa
@app.route('/companies/delete/<int:company_id>', methods=['POST'])
@login_required
@permission_required(pl.ADMIN)
def delete_company(company_id):
    """
    Deleta uma empresa.
    
    Métodos:
    - POST: Processa a deleção da empresa.
    
    Requer:
    - Usuário autenticado.
    - Permissão de ADMIN.
    """
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Empresa deletada com sucesso!', 'success')
    return redirect(url_for('list_companies'))
