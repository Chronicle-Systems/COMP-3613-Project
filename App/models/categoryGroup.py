from App.database import db


class CategoryGroup(db.Model):
    __tablename__ = 'category_group'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    average_duration_days = db.Column(db.Integer, nullable=False)

    def __init__(self, average_duration_days):
        self.average_duration_days = average_duration_days

    def __repr__(self):
        return f"<CategoryGroup (ID={self.id}, Average Duration Days={self.average_duration_days})>"

    def __str__(self):
        return f"CategoryGroup (ID={self.id}, Average Duration Days={self.average_duration_days})"

    def to_json(self):
        return {
            "id": self.id,
            "average_duration_days": self.average_duration_days
        }
