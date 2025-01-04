from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'events'  # Table name in the database

    id_event = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(255), nullable=False)  # Event name
    description = db.Column(db.Text, nullable=True)  # Event description
    city = db.Column(db.String(100), nullable=False)  # Event city
    max_capacity = db.Column(db.Integer, nullable=False)  # Maximum capacity
    subscribers = db.Column(db.ARRAY(db.Integer), default=[], nullable=False)  # Subscribers array (Will introduce user IDs here)

    def to_dict(self):
        return {
            'id_event': self.id_event,
            'name': self.name,
            'description': self.description,
            'city': self.city,
            'max_capacity': self.max_capacity,
            'subscribers': self.subscribers,
        }
