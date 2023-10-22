from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from forms import RegisterForm, LoginForm, AddTaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8yEfBA6O6dWlSihBXox7C0sKRlm3c66b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# Login Credential
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Connect to databasee
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_tasks.db'
db = SQLAlchemy()
db.init_app(app)


# Create User table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    tasks = relationship("UserTask", back_populates="staff")


#  Create UserTask table
class UserTask(db.Model):
    __tablename__ = "user_tasks"
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    staff = relationship("User", back_populates="tasks")
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(50), default="To Do")


with app.app_context():
    db.create_all()


# Home page
@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


# Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_tasks"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_tasks'))

    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Create a new task (only admin)
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def get_all_tasks():
    all_tasks = db.session.execute(db.select(UserTask).order_by(UserTask.staff_id)).scalars().all()
    # get all users
    users = db.session.execute(db.select(User).order_by(User.name)).scalars().all()
    user_list = [(user.id, user.name) for user in users]
    print(user_list)
    form = AddTaskForm()
    form.user_assigned.choices = user_list

    if current_user.id == 1 and form.validate_on_submit():
        new_task = UserTask(
            staff_id=form.user_assigned.data,
            title=form.task.data,
            date=date.today().strftime("%B %d, %Y")
        )

        db.session.add(new_task)
        db.session.commit()

        flash("Task added successfully", "success")
        return redirect(url_for('get_all_tasks'))

    return render_template("task.html", form=form, current_user=current_user, tasks=all_tasks)


# Start the task
@app.route('/start_task/<int:task_id>', methods=['POST'])
@login_required
def start_task(task_id):
    task = UserTask.query.get(task_id)
    if task:
        task.status = 'In Progress'
        db.session.commit()
        flash('Task started successfully', 'success')
    return redirect(url_for('get_all_tasks'))


# Complete the task
@app.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = UserTask.query.get(task_id)
    if task:
        task.status = 'Completed'
        db.session.commit()
        flash('Task completed successfully', 'success')
    return redirect(url_for('get_all_tasks'))


if __name__ == "__main__":
    app.run(debug=True, port=5004)
