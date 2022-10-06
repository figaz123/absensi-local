from enum import unique
from fileinput import filename
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import cv2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

def photo():
    cap = cv2.VideoCapture(0)
    
    while(True):
        ret, frame = cap.read()
        cv2.imshow('img1', frame)
        filename = "pro_image/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpeg"
        if cv2.waitKey(1) & 0xFF == ord('y'):
            cv2.imwrite(filename, frame)
            cv2.destroyAllWindows()
            break
    cap.release()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    angkatan = db.Column(db.String(256), nullable=False)
    jurusan = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_email = request.form['email']
        task_angkatan = request.form['angkatan']
        task_jurusan = request.form['jurusan']
        new_task = Todo(content=task_content, email=task_email, angkatan=task_angkatan, jurusan=task_jurusan)

        try:
            db.session.add(new_task)
            db.session.commit()
            photo()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


# @app.route('/email', methods=['POST', 'GET'])
# def email():
#     if request.method == 'POST':
#         task_email = request.form.get['email']
#         new_task = Todo(content=[task_email])

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'

#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.email = request.form['email']
        task.angkatan = request.form['angkatan']
        task.jurusan = request.form['jurusan']
        #new_task = Todo(content=task.content, email=task.email)

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()