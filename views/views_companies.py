from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Company

@app.route('/companies', methods=['GET'])
def list_companies():
    companies = Company.query.all()
    return render_template('list_companies.html', companies=companies)

@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
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

@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
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

@app.route('/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    db.session.delete(company)
    db.session.commit()
    flash('Empresa deletada com sucesso!', 'success')
    return redirect(url_for('list_companies'))
