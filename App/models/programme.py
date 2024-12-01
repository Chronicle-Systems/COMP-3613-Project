from App.database import db

class Programme(db.Model):
    __tablename__ = 'programme'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)  # Changed p_ID to id
    name = db.Column(db.String(100), nullable=False, unique=True)  # Changed p_name to name and added unique constraint
    programme_courses = db.relationship('CourseProgramme', backref='programme', lazy='joined')  # Updated relationship name

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Programme (ID={self.id}, Name='{self.name}')>"

    def __str__(self):
        return f"Programme (ID={self.id}, Name={self.name})"

    def to_json(self):
        return {
            "id": self.id,  # Changed p_ID to id
            "name": self.name
        }
