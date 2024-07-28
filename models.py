from app import db

class Contact(db.Model):
    __tablename__ = 'tbContacts'
    ContactID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    Message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
    
class Employee(db.Model):
    __tablename__ = 'tbEmployee'
    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(15))
    CompanyID = db.Column(db.Integer, db.ForeignKey('tbCompany.CompanyID'))
    PermissionLevelID = db.Column(db.Integer, db.ForeignKey('tbPermissionLevel.LevelID'))

    def __repr__(self):
        return '<Name %r>' % self.name