from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Project, Record
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email/Username does not exist.', category='error')

    return render_template("login.html", curr_user=current_user)

@auth.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        button_name = request.form.get('buttonName')
        if button_name == 'button1':
            email = request.form.get('email')
            name = request.form.get('firstName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            user = User.query.filter_by(email=email).first()
            if user:
                flash(f'{user.email} already exists', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 4 characters.', category='error')
            elif len(name) < 2:
                flash('First name must be greater than 2 characters.', category='error')
            elif password1 != password2:
                flash('Passwords do not match.', category='error')
            elif len(password1) < 7:
                flash('Password must be greater than 7 characters.', category='error')
            else:
                new_user = User(email=email, first_name=name, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('User created!', category='success')
                return redirect(url_for('auth.admin'))
        elif button_name == 'button2': 
            project_name = request.form.get('projectName')
            project_url = request.form.get('projectUrl')

            project = Project.query.filter_by(project_name=project_name).first()
            if project:
                flash('Project already exists', category='error')
            elif len(project_name) < 4:
                flash('Project Name must be greater than 4 characters.', category='error')
            elif len(project_url) < 4:
                flash('Project url must be greater than 4 characters.', category='error')
            else:
                new_project = Project(project_name=project_name, project_url=project_url)
                db.session.add(new_project)
                db.session.commit()
                flash('Project added!', category='success')
                return redirect(url_for('auth.admin'))
        else:
            email = request.form.get('email')
            project_url = request.form.get('projectUrl')

            user = User.query.filter_by(email=email).first()
            project = Project.query.filter_by(project_url=project_url).first()
            if not user:
                flash(f'{user.email} does not exist', category='error')
            elif not project:
                flash(f'{project.project_name} does not exist', category='error')
            else:
                new_record = Record(user_id=user.id,project_id=project.id)
                db.session.add(new_record)
                db.session.commit()
                flash('Record created!', category='success')
                return redirect(url_for('auth.admin'))

    users = User.query
    projects = Project.query
    return render_template("admin.html", users=users, projects=projects, curr_user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))