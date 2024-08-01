import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from models import File
from decorators import login_required, permission_required
from enums import PermissionLevel

@app.route('/list_files', methods=['GET'])
@login_required
@permission_required(PermissionLevel.EDITOR)
def list_files():
    files = File.query.all()
    return render_template('list_files.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
@permission_required(PermissionLevel.EDITOR)
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        template_id = request.form.get('template_id')
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            new_file = File(Status='Uploaded', FilePath=file_path, TemplateID=template_id)
            db.session.add(new_file)
            db.session.commit()
            
            flash('Arquivo enviado com sucesso!', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('Nenhum arquivo selecionado.', 'danger')
    
    return render_template('upload_files.html')

@app.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
@permission_required(PermissionLevel.EDITOR)
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    try:
        file.delete_file()
        db.session.delete(file)
        db.session.commit()
        flash('Arquivo deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Ocorreu um erro ao deletar o arquivo: {str(e)}', 'danger')
    return redirect(url_for('list_files'))
