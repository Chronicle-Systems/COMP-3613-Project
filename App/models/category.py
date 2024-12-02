from App.database import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'category_group.id'), nullable=False)

    group = db.relationship(
        'CategoryGroup', backref=db.backref('categories', lazy='dynamic'))

    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id

    def __repr__(self):
        return f"<Category (ID={self.id}, Name='{self.name}', Group ID={self.group_id})>"

    def __str__(self):
        return f"Category (ID={self.id}, Name={self.name})"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "group_id": self.group_id,
            "group": self.group.to_json() if self.group else None
        }
