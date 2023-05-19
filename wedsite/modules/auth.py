import functools
import datetime
import os
import random

from flask import Blueprint, flash, redirect, render_template, request, session, url_for , current_app
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import null, inspect

from wedsite.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            error = 'Enganaste-te no username oh burro.'
        elif not check_password_hash(user.password, password):
            error = 'Enganaste-te na password oh burro.'

        
        if error is None:
            session['user'] = user
            
            if username == 'admin' or user.is_admin:
                session['admin_logged'] = True
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/verify_generated_code/<user_id>', methods=('GET', 'POST'))
def verify_generated_code(user_id):
    if request.method == 'POST':
        generated_code = int(request.form['generated_code']) if request.form['generated_code'] else None
        user = User.query.filter_by(id=user_id).first()
        error = None

        if generated_code == user.generated_code:
            session.clear()
            session['user'] = user
            user.generated_code = None
            return redirect(url_for('players.edit', id=user.player_id))
        
        error = 'Código errado oh burro.'
        flash(error)
    return render_template('auth/verify_generated_code.html',user_id=user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['user'] is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
