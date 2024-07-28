import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
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
        FilePath VARCHAR(255) NOT NULL,
        EmployeeID INT,
        FOREIGN KEY (EmployeeID) REFERENCES tbEmployee(EmployeeID)
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
        FOREIGN KEY (TemplateID) REFERENCES tbTemplate(TemplateID),
        FOREIGN KEY (FileID) REFERENCES tbFiles(FileID)
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

# Commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()
