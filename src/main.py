import os
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Todo


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/Todos',methods=['GET','POST'])
@app.route('/Todo/<int:id>', methods=['GET','DELETE'])
def todos(id=None):

    if request.method == 'GET':

        if id is not None:
            todo = Todo.query.get(id)
            if todo:
                return jsonify(todo.serialize()), 200
            else:
                return jsonify({"msg": "Todo not found"}), 404
        else:
            todos = Todo.query.all()
            todos = list(map(lambda todo: todo.serialize(), todos))
            return jsonify(todos), 200
        

    if request.method == 'POST':
        todo = request.json.get('todo', None)
        

        if not todo:
            return jsonify({"msg": 'Name is required'}), 400
        
        todo = Todo()
        todo.todo = todo

        db.session.add(todo)
        db.session.commit()

        return jsonify(todo.serialize()), 201



    if request.method == 'DELETE':
        todo = Todo.query.get(id)

        if not todo:
            return jsonify({"msg": "Todo not found"}), 404

        db.session.delete(todo)
        db.session.commit()
        return jsonify({"msg": "Todo deleted"}), 200

if __name__ == "__main__":
    manager.run()