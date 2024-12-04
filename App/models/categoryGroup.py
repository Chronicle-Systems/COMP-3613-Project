from App.database import db


class CategoryGroup(db.Model):
    __tablename__ = 'category_group'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False, unique=True)
    average_duration_days = db.Column(db.Integer, nullable=False)

    def __init__(self, average_duration_days: int):
        self.average_duration_days = average_duration_days

    def __str__(self) -> str:
        return f"""
CategoryGroup Info:
    - ID: {self.id}
    - Average Assessment Duration (Days): {self.average_duration_days}
"""

    def __repr__(self) -> str:
        return (f"<CategoryGroup(id={self.id}, "
                f"average_duration_days={self.average_duration_days})>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "average_duration_days": self.average_duration_days
        }
