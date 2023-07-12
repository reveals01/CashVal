from flask import Blueprint, redirect,url_for


main = Blueprint('main', __name__)
@main.route('/')
def index():
    #current_app.scheduler.add_job(job1, 'interval', seconds=3)
    return redirect(url_for('users.login'))


