from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from wedsite.models import Product , Hotel , FAQ

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('main/index.html')

@bp.route('/faqs', methods=('GET', 'POST'))
def faqs():
    q_and_as = FAQ.query.all()
    return render_template('faqs/faqs.html',q_and_as=q_and_as)

@bp.route('/informations', methods=('GET', 'POST'))
def informations():
    hotels = Hotel.query.all()
    return render_template('informations/informations.html',hotels=hotels)
