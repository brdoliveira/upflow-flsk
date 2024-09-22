from app import db
from datetime import datetime
import os

class Contact(db.Model):
    """
    Modelo para a tabela de contatos.
    
    Atributos:
    - ContactID: Identificador único do contato.
    - Name: Nome do contato.
    - Email: Email do contato.
    - Message: Mensagem do contato.
    """
    __tablename__ = 'tbContacts'
    ContactID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    Message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.Name

class Company(db.Model):
    """
    Modelo para a tabela de empresas.
    
    Atributos:
    - CompanyID: Identificador único da empresa.
    - Name: Nome da empresa.
    - CNPJ: CNPJ da empresa.
    - Address: Endereço da empresa.
    - Phone: Telefone da empresa.
    - FoundationDate: Data de fundação da empresa.
    - Sector: Setor da empresa.
    """
    __tablename__ = 'tbCompany'
    CompanyID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    CNPJ = db.Column(db.String(14), unique=True, nullable=False)
    Address = db.Column(db.String(255))
    Phone = db.Column(db.String(15))
    FoundationDate = db.Column(db.Date)
    Sector = db.Column(db.String(100))

    def __repr__(self):
        return '<Company %r>' % self.Name

class PermissionLevel(db.Model):
    """
    Modelo para a tabela de níveis de permissão.
    
    Atributos:
    - LevelID: Identificador único do nível de permissão.
    - Description: Descrição do nível de permissão.
    """
    __tablename__ = 'tbPermissionLevel'
    LevelID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<PermissionLevel %r>' % self.Description

class Employee(db.Model):
    """
    Modelo para a tabela de empregados.
    
    Atributos:
    - EmployeeID: Identificador único do empregado.
    - Name: Nome do empregado.
    - Email: Email do empregado.
    - Password: Senha do empregado.
    - Phone: Telefone do empregado.
    - CompanyID: Identificador da empresa associada ao empregado.
    - PermissionLevelID: Identificador do nível de permissão do empregado.
    """
    __tablename__ = 'tbEmployee'
    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(15))
    CompanyID = db.Column(db.Integer, db.ForeignKey('tbCompany.CompanyID'))
    PermissionLevelID = db.Column(db.Integer, db.ForeignKey('tbPermissionLevel.LevelID'))

    Company = db.relationship('Company', backref=db.backref('employees', lazy=True))
    PermissionLevel = db.relationship('PermissionLevel', backref=db.backref('employees', lazy=True))

    def __repr__(self):
        return '<Employee %r>' % self.Name

class Template(db.Model):
    """
    Modelo para a tabela de templates.
    
    Atributos:
    - TemplateID: Identificador único do template.
    - Description: Descrição do template.
    - SelectedData: Dados selecionados.
    - FilePath: Caminho do arquivo no sistema de arquivos.
    - InsertionDate: Data de inserção do template.
    """
    __tablename__ = 'tbTemplate'
    TemplateID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(255))
    SelectedData = db.Column(db.Text)
    FilePath = db.Column(db.String(255), nullable=False)
    InsertionDate = db.Column(db.DateTime, default=datetime.utcnow)

    files = db.relationship('File', backref='template', lazy=True)  # Alterado para 'files'

    def __repr__(self):
        return '<Template %r>' % self.Description

class File(db.Model):
    """
    Modelo para a tabela de arquivos.
    
    Atributos:
    - FileID: Identificador único do arquivo.
    - Status: Status do arquivo.
    - InsertionDate: Data de inserção do arquivo.
    - TemplateID: Identificador do template associado.
    - FilePath: Caminho do arquivo no sistema de arquivos.
    """
    __tablename__ = 'tbFiles'
    FileID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Status = db.Column(db.String(50))
    InsertionDate = db.Column(db.DateTime, default=datetime.utcnow)
    FilePath = db.Column(db.String(255), nullable=False)
    TemplateID = db.Column(db.Integer, db.ForeignKey('tbTemplate.TemplateID'), nullable=False)
    
    file_data = db.relationship('FileData', backref='file', lazy=True)  # Alterado para 'file_data'

    def __repr__(self):
        return '<File %r>' % self.Status

    def delete_file(self):
        """
        Deleta o arquivo do sistema de arquivos se ele existir.
        """
        if os.path.exists(self.FilePath):
            os.remove(self.FilePath)

class FileData(db.Model):
    """
    Modelo para a tabela de dados dos arquivos.
    
    Atributos:
    - DataID: Identificador único dos dados.
    - TemplateID: Identificador do template associado.
    - FileID: Identificador do arquivo associado.
    - InsertionDate: Data de inserção dos dados.
    - Information: Informações dos dados em formato JSON.
    """
    __tablename__ = 'tbFileData'
    DataID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TemplateID = db.Column(db.Integer, db.ForeignKey('tbTemplate.TemplateID'), nullable=False)
    FileID = db.Column(db.Integer, db.ForeignKey('tbFiles.FileID'), nullable=False)
    InsertionDate = db.Column(db.DateTime, default=datetime.utcnow)
    Information = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return '<FileData %r>' % self.DataID
