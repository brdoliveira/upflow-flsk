from app import db

class Contact(db.Model):
    __tablename__ = 'tbContacts'
    ContactID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    Message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Company(db.Model):
    __tablename__ = 'tbCompany'
    CompanyID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    CNPJ = db.Column(db.String(14), unique=True, nullable=False)
    Address = db.Column(db.String(255))
    Phone = db.Column(db.String(15))
    FoundationDate = db.Column(db.Date)
    Sector = db.Column(db.String(100))

    def __repr__(self):
        return '<Name %r>' % self.name

class PermissionLevel(db.Model):
    __tablename__ = 'tbPermissionLevel'
    LevelID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Employee(db.Model):
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
        return '<Name %r>' % self.name
