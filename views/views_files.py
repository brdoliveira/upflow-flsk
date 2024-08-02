import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from models import File
from decorators import login_required, permission_required
from enums import PermissionLevel as pl

# Rota para listar arquivos
@app.route('/list_files', methods=['GET'])
@login_required
@permission_required(pl.EDITOR)
def list_files():
    """
    Lista todos os arquivos.
    
    Requer:
    - Usuário autenticado.
    - Permissão de EDITOR.
    """
    files = File.query.all()
    return render_template('list_files.html', files=files)

# Rota para fazer upload de arquivos
@app.route('/upload', methods=['GET', 'POST'])
@login_required
@permission_required(pl.EDITOR)
def upload_file():
    """
    Faz upload de um novo arquivo.
    
    Métodos:
    - GET: Renderiza o formulário de upload.
    - POST: Processa o envio do formulário e salva o arquivo no servidor.
    
    Requer:
    - Usuário autenticado.
    - Permissão de EDITOR.
    """
    if request.method == 'POST':
        file = request.files['file']
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Verifica se o diretório existe, se não, cria-o
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            file.save(file_path)
            
            new_file = File(Status='Uploaded', FilePath=file_path, TemplateID=1) # 1 até definir o fluxo
            db.session.add(new_file)
            db.session.commit()
            
            flash('Arquivo enviado com sucesso!', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('Nenhum arquivo selecionado.', 'danger')
    
    return render_template('upload_files.html')

# Rota para deletar arquivos
@app.route('/delete_file/<int:file_id>', methods=['POST'])
@login_required
@permission_required(pl.EDITOR)
def delete_file(file_id):
    """
    Deleta um arquivo.
    
    Métodos:
    - POST: Processa a deleção do arquivo.
    
    Requer:
    - Usuário autenticado.
    - Permissão de EDITOR.
    """
    file = File.query.get_or_404(file_id)
    try:
        file.delete_file()
        db.session.delete(file)
        db.session.commit()
        flash('Arquivo deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Ocorreu um erro ao deletar o arquivo: {str(e)}', 'danger')
    return redirect(url_for('list_files'))
