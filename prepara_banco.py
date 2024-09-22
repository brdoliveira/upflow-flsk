import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `db_upflow`;")
cursor.execute("CREATE DATABASE `db_upflow`;")
cursor.execute("USE `db_upflow`;")

TABLES = {}

TABLES['tbCompany'] = ('''
    CREATE TABLE tbCompany (
        CompanyID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        CNPJ CHAR(14) UNIQUE NOT NULL,
        Address VARCHAR(255),
        Phone CHAR(15),
        FoundationDate DATE,
        Sector VARCHAR(100)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['tbPermissionLevel'] = ('''
    CREATE TABLE tbPermissionLevel (
        LevelID INT AUTO_INCREMENT PRIMARY KEY,
        Description VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['tbEmployee'] = ('''
    CREATE TABLE tbEmployee (
        EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,                
        Phone CHAR(15),
        CompanyID INT,
        PermissionLevelID INT,
        FOREIGN KEY (CompanyID) REFERENCES tbCompany(CompanyID),
        FOREIGN KEY (PermissionLevelID) REFERENCES tbPermissionLevel(LevelID)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['tbTemplate'] = ('''
    CREATE TABLE tbTemplate (
        TemplateID INT AUTO_INCREMENT PRIMARY KEY,
        InsertionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
        Description VARCHAR(255),
        SelectedData TEXT,
        FilePath VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['tbFiles'] = ('''
    CREATE TABLE tbFiles (
        FileID INT AUTO_INCREMENT PRIMARY KEY,
        Status VARCHAR(50),
        InsertionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
        FilePath VARCHAR(255) NOT NULL,
        TemplateID INT,
        FOREIGN KEY (TemplateID) REFERENCES tbTemplate(TemplateID)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['tbFileData'] = ('''
    CREATE TABLE tbFileData (
        DataID INT AUTO_INCREMENT PRIMARY KEY,
        TemplateID INT,
        FileID INT,
        InsertionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
        Information JSON,
        FOREIGN KEY (FileID) REFERENCES tbFiles(FileID),
        FOREIGN KEY (TemplateID) REFERENCES tbTemplate(TemplateID)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

TABLES['tbContacts'] = ('''
    CREATE TABLE tbContacts (
        ContactID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Message TEXT NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
''')

for table_name in TABLES:
    table_sql = TABLES[table_name]
    try:
        print(f'Criando tabela {table_name}:', end=' ')
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Já existe')
        else:
            print(err.msg)
    else:
        print('OK')

cursor.execute("INSERT INTO tbPermissionLevel (Description) VALUES('Admin'),('Editor'),('Viewer'),('Guest');")

cursor.execute("INSERT INTO tbCompany (Name, CNPJ, Address, Phone, FoundationDate, Sector) VALUES\
               ('Admin Company', '12345678000195', '123 Admin St', '1234567890', '2020-01-01', 'Technology');")

cursor.execute("\
INSERT INTO tbEmployee (Name, Email, Password, Phone, CompanyID, PermissionLevelID) VALUES\
('Admin User', 'admin@example.com', 'scrypt:32768:8:1$gvPkYL3FFzIxjUyY$591d3a014eab7edd50c90dc13d2660c1918d51fa60d1cdf8ed3a7a7280b266345fe215e4ab3df0a0efaa8107c2b7748fa3c5d2bd55332058cb9e65d3dfa1ca79', '0987654321',\
(SELECT CompanyID FROM tbCompany WHERE Name='Admin Company'),\
(SELECT LevelID FROM tbPermissionLevel WHERE Description='Admin'))\
")

cursor.execute("INSERT INTO tbTemplate (Description, SelectedData, FilePath)\
VALUES ('Nota Fiscal - Documento referente a uma transação comercial.', 'Documento fiscal emitido para registrar uma transação comercial.', '/uploads/ml_files/nota_fiscal/');")

cursor.execute("INSERT INTO tbTemplate (Description, SelectedData, FilePath)\
VALUES ('Boleto Bancário - Documento utilizado para cobrança.', 'Documento utilizado para cobrança de um valor.', '/uploads/ml_files/boleto/');")

cursor.execute("INSERT INTO tbTemplate (Description, SelectedData, FilePath)\
VALUES ('Imposto de Renda - Documento para declaração anual de rendimentos.', 'Documento utilizado para declaração de rendimentos ao governo.', '/uploads/ml_files/imposto_de_renda/');")

cursor.execute("INSERT INTO tbTemplate (Description, SelectedData, FilePath)\
VALUES ('Tipo Desconhecido - Documento não identificado.', 'Documento de tipo não identificado.', 'sem arquivo');")

# Commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
