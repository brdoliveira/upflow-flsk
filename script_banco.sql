-- Criação do banco de dados
DROP DATABASE IF EXISTS db_upflow;
CREATE DATABASE db_upflow;

-- Conectar ao banco de dados criado
\c db_upflow;

-- Criação das tabelas
CREATE TABLE tbCompany (
    CompanyID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    CNPJ CHAR(14) UNIQUE NOT NULL,
    Address VARCHAR(255),
    Phone CHAR(15),
    FoundationDate DATE,
    Sector VARCHAR(100)
);

CREATE TABLE tbPermissionLevel (
    LevelID SERIAL PRIMARY KEY,
    Description VARCHAR(255) NOT NULL
);

CREATE TABLE tbEmployee (
    EmployeeID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Phone CHAR(15),
    CompanyID INT,
    PermissionLevelID INT,
    FOREIGN KEY (CompanyID) REFERENCES tbCompany(CompanyID),
    FOREIGN KEY (PermissionLevelID) REFERENCES tbPermissionLevel(LevelID)
);

CREATE TABLE tbFiles (
    FileID SERIAL PRIMARY KEY,
    Status VARCHAR(50),
    InsertionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FilePath VARCHAR(255) NOT NULL,
    TemplateID INT
);

CREATE TABLE tbFileData (
    DataID SERIAL PRIMARY KEY,
    TemplateID INT,
    FileID INT,
    InsertionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Information JSON,
    FOREIGN KEY (FileID) REFERENCES tbFiles(FileID)
);

CREATE TABLE tbContacts (
    ContactID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Message TEXT NOT NULL
);

-- Inserção de dados iniciais
INSERT INTO tbPermissionLevel (Description) VALUES
('Admin'),
('Editor'),
('Viewer'),
('Guest');

INSERT INTO tbCompany (Name, CNPJ, Address, Phone, FoundationDate, Sector) VALUES
('Admin Company', '12345678000195', '123 Admin St', '1234567890', '2020-01-01', 'Technology');

INSERT INTO tbEmployee (Name, Email, Password, Phone, CompanyID, PermissionLevelID) VALUES
('Admin User', 'admin@example.com', 'scrypt:32768:8:1$gvPkYL3FFzIxjUyY$591d3a014eab7edd50c90dc13d2660c1918d51fa60d1cdf8ed3a7a7280b266345fe215e4ab3df0a0efaa8107c2b7748fa3c5d2bd55332058cb9e65d3dfa1ca79', '0987654321',
(SELECT CompanyID FROM tbCompany WHERE Name='Admin Company'),
(SELECT LevelID FROM tbPermissionLevel WHERE Description='Admin'));
