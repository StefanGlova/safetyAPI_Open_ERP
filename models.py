from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Incident(db.Model):
    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    incident_type = db.Column(db.String(20), nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    person_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, incident_type, incident_date, person_name, description):
        self.incident_type = incident_type
        self.incident_date = incident_date
        self.person_name = person_name
        self.description = description

    @validates('incident_type')
    def validate_incident_type(self, key, incident_type):
        if incident_type not in ('injury', 'damage', 'near_miss'):
            raise ValueError("Invalid input. Choose from 'injury', 'damage', 'near_miss'")
        return incident_type        
