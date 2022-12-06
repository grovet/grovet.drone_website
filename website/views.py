from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User, Project, Record

views = Blueprint('views', __name__)

@views.route('/home')
@login_required
def home():
    projects = []
    #records = current_user.records
    records = Record.query.filter_by(user_id=current_user.id).all()
    for record in records:
       project_set = Project.query.filter_by(id=record.project_id).first()
       project = project_set.project_name
       p_url = project_set.project_url
       projects.append([project, p_url])
    return render_template("home.html", curr_user=current_user, projects=projects)

@views.route('/service')
@login_required
def service():
    return render_template("services.html", curr_user=current_user)