from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<todo %r" % self.todo

    def serialize(self):
        return {
            "id": self.id,
            "todo": self.todo,
        }
