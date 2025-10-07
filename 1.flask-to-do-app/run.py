from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# ORM type
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'Task {self.id}'


@app.route("/", defaults={'type': None})
@app.route("/<string:type>")
def index(type): 
    if type == 'completed':
        tasks = Todo.query.filter_by(status=True).all()
    else:
        tasks = Todo.query.all()
    return render_template("todo/index.html", tasks=tasks, type=type)

@app.route("/create")
def create(): 
    return render_template("todo/create.html")

@app.route("/store", methods=['POST'])
def store(): 
    if request.method == 'POST':
        task = request.form.get('task')
        todo = Todo(content=task)
        try:
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

@app.route("/update-status/<int:id>")
def complete(id): 
    task = Todo.query.get_or_404(id)
    try:
        if task.status == False:
            task.status = True
        else:
            task.status = False
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem completing that task"


@app.route("/edit/<int:id>")
def edit(id): 
    todo = Todo.query.get_or_404(id)
    return render_template("todo/edit.html", todo=todo)

@app.route("/update/<int:id>", methods=['POST'])
def update(id): 
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form.get('task')
        task.status = False
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"

@app.route("/delete/<int:id>")
def delete(id): 
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

