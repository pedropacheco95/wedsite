import functools
import datetime
import os
import random

from flask import Blueprint, flash, redirect, render_template, request, session, url_for , current_app
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import null, inspect

from wedsite.models import User
from wedsite.tools import image_tools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        name = request.form['name']
        full_name= request.form['full_name']
        prefered_hand= request.form['prefered_hand']
        prefered_position= request.form['prefered_position']
        height= request.form['height']
        birthday= datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d') if request.form['birth_date'] else None

        final_files = request.files.getlist('finalFile')

        error = None
        if not username:
            error = 'Tens que por um username oh burro.'
        elif not password:
            error = 'Tens que por uma password oh burro.'
        elif User.query.filter_by(username=username).first() is not None:
            error = f"O username {username} já está registado oh burro."
        elif User.query.filter_by(email=email).first() is not None:
            error = f"O email {email} já está registado oh burro."
        elif not name:
            error = 'Tens que por um nome oh burro.'

        if error is None:
            user = User(username=username, email=email , password= password, player_id=player.id)
            user.create()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html',players=players)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            error = 'Wrong username.'
        elif not check_password_hash(user.password, password):
            error = 'Wrong password.'

        
        if error is None:
            session['user'] = user
            
            if username == 'admin' or user.is_admin:
                session['admin_logged'] = True
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/forgot_password', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Enganaste-te no username oh burro.'

        if error is None:

            email = user.email
            generated_code = random.randint(10000, 99999)

            user.generated_code = generated_code
            user.save()

            mail_body = render_template('messages/forgot_password_email.html', user=user, generated_code = generated_code)

            email_tools.send_email('Código autenticação', [email], html = mail_body)

            return redirect(url_for('auth.verify_generated_code',user_id=user.id))

        flash(error)

    return render_template('auth/forgot_password.html')

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

@bp.route('/generate_new_code/<user_id>', methods=('GET', 'POST'))
def generate_new_code(user_id):
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    generated_code = random.randint(10000, 99999)
    user.generated_code = generated_code
    user.save()
    mail_body = render_template('messages/forgot_password_email.html', user=user, generated_code = generated_code)
    email_tools.send_email('Código autenticação', [email], html = mail_body)
    return redirect(url_for('auth.verify_generated_code',user_id=user.id))

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
