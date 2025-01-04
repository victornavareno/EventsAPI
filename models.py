from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Local(db.Model):
    __tablename__ = 'events'  # table name here

    id_local = db.Column(db.Integer, primary_key=True)  # PRIMARY KEEEY 
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    events = db.Column(db.ARRAY(db.Integer), nullable=True)

    def to_dict(self):
        return {
            'id_local': self.id_local,
            'name': self.name,
            'city': self.city,
            'address': self.address,
            'events': self.events,
        }