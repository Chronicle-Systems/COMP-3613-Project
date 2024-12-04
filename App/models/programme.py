from App.database import db

class Programme(db.Model):
    __tablename__ = 'programme'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # relationships
    programme_courses = db.relationship(
        "ProgrammeCourse", back_populates="programme", lazy='dynamic'
    )

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"""
Programme Info:
    - ID: {self.id}
    - Name: {self.name}
"""

    def __repr__(self) -> str:
        return (f"<Programme(id={self.id}, "
                f"name='{self.name}')>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }
