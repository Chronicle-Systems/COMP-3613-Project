from App.database import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'category_group.id'), nullable=False)

    group = db.relationship(
        'CategoryGroup', backref=db.backref('category', lazy='dynamic'))

    def __init__(self, name: str, group_id: int):
        self.name = name
        self.group_id = group_id

    def __str__(self) -> str:
        return f"""
Category Info:
    - ID: {self.id}
    - Name: {self.name}
    - Group ID: {self.group_id}
"""

    def __repr__(self) -> str:
        return (f"<Category(id={self.id}, "
                f"name='{self.name}', "
                f"group_id={self.group_id})>")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "group_id": self.group_id
        }
