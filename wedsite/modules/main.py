from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from wedsite.models import Product , Hotel , FAQ

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    date_time = datetime(2024, 8, 30, 15, 30)

    # Format the date and time
    formatted_date_time = date_time.strftime('%Y-%m-%dT%H:%M')
    return render_template('main/index.html',formatted_date_time=formatted_date_time)

@bp.route('/faqs', methods=('GET', 'POST'))
def faqs():
    q_and_as = FAQ.query.all()
    return render_template('faqs/faqs.html',q_and_as=q_and_as)

@bp.route('/informations', methods=('GET', 'POST'))
def informations():
    hotels = Hotel.query.all()
    return render_template('informations/informations.html',hotels=hotels)
