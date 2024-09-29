import os
import json
import codecs
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db, pdf_classifier
from models import File, FileData
from decorators import login_required, permission_required
from enums import PermissionLevel as pl
from tools.extractors.boleto_extraction import BoletoExtractionStrategy
from tools.extractors.nota_fiscal_extraction import NotaFiscalExtractionStrategy
from tools.extractors.imposto_de_renda_extraction import ImpostoDeRendaExtractionStrategy
import pandas as pd
from flask import send_file
from io import BytesIO

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
    
    for file in files:
        for file_data in file.file_data:
            file_data.Information = decode_unicode_escape(file_data.Information)

    return render_template('list_files.html', files=files)

def decode_unicode_escape(data):
    if isinstance(data, dict):
        return {key: decode_unicode_escape(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [decode_unicode_escape(item) for item in data]
    elif isinstance(data, str):
        try:
            # Tenta primeiro decodificar a string como 'utf-8' normal
            data = data.encode('latin1').decode('utf-8')
            # Tenta decodificar novamente para capturar todas as sequências de escape
            data = codecs.decode(data, 'unicode_escape')
            return data
        except (UnicodeEncodeError, UnicodeDecodeError):
            return data
    else:
        return data

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
            prediction = pdf_classifier.predict_pdf_type(file_path)

            templateID = 4
            if prediction == "Nota Fiscal":
                extraction_strategy = NotaFiscalExtractionStrategy()
                templateID = 1
            elif prediction == "Boleto":
                extraction_strategy = BoletoExtractionStrategy()
                templateID = 2
            elif prediction == "Imposto de Renda":
                extraction_strategy = ImpostoDeRendaExtractionStrategy()
                templateID = 3
            else:
                raise ValueError("Tipo de documento desconhecido.")

            new_file = File(Status='Uploaded', FilePath=file_path, TemplateID=templateID)
            db.session.add(new_file)
            db.session.commit()
            
            # Extrair dados usando a estratégia selecionada
            text = pdf_classifier.extract_text_from_pdf(file_path)
            extracted_data = extraction_strategy.extract_data(text)

            # Salva os dados extraídos na tabela FileData
            new_file_data = FileData(
                FileID=new_file.FileID,  # Associa o FileData ao File criado
                Information=json.dumps(extracted_data)  # Converte o dicionário extracted_data para JSON
            )
            db.session.add(new_file_data)
            db.session.commit()
                    
            flash(f'Arquivo do tipo {prediction} salvo com sucesso!', 'success')
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
    Responsável por deletar um arquivo.
    
    Métodos:
    - POST: Processar a exclusão do arquivo.
    
    Requer:
    - Usuário estar autenticado.
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

@app.route('/export_excel', methods=['POST'])
@login_required
@permission_required(pl.EDITOR)
def export_excel():
    """
    Exporta os arquivos relacionados a um TemplateID para um arquivo Excel.
    
    Requer:
    - Usuário autenticado.
    - Permissão de EDITOR.
    """
    template_id = request.form.get('template_id')
    files = File.query.filter_by(TemplateID=template_id).all()

    if not files:
        flash('Nenhum arquivo encontrado para o Template selecionado.', 'warning')
        return redirect(url_for('list_files'))

    data = []
    for file in files:
        for file_data in file.file_data:
            data.append({
                'FileID': file.FileID,
                'Status': file.Status,
                'InsertionDate': file.InsertionDate,
                'FilePath': file.FilePath,
                'TemplateID': file.TemplateID,
                'DataID': file_data.DataID,
                'FileData_InsertionDate': file_data.InsertionDate,
                'Information': file_data.Information
            })

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Files')
    
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='files_export.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')