from flask import Blueprint, render_template,request,flash,redirect,url_for
from flask_login import current_user
from flask_login import login_required
from project import db,app
import datetime
from functools import wraps
from flask_login import login_user, login_required, logout_user

from ..accounts.models import Account,Position

positions_bp = Blueprint('positions', __name__,template_folder='templates')

@positions_bp.route('/positions', methods=['GET'])
@positions_bp.route('/positions/<oneIsin>', methods=['GET'])
@login_required
def positions(oneIsin='all'):
    if (oneIsin =='all'):
        listPositions=Position.query.all()
    else:
        listPositions=Position.query.filter_by(ISIN=oneIsin)
    return render_template('positions.html',listItems=listPositions,navActive='positions')



