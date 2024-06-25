from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from wedsite.tools import tools

from wedsite.models import Product , Contribution, Chapter


bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('/all', methods=('GET', 'POST'))
@bp.route('/all/<update>', methods=('GET', 'POST'))
def all(update=None):    
    products = Product.query.filter_by().order_by(Product.priority).all()
    chapters = Chapter.query.all()
    if update == 'update':
        for product in products:
            product.update_price_paid()
    return render_template('products/all.html', chapters=chapters)

@bp.route('/product/<product_id>', methods=('GET', 'POST'))
@bp.route('/product/<product_id>/<contribution_id>', methods=('GET', 'POST'))
def product(product_id,contribution_id=None):
    product = Product.query.filter_by(id=product_id).first()
    contribution=None
    if contribution_id:
        contribution = Contribution.query.filter_by(id=contribution_id).first()

    ##VERFICAR SE A CONTRIBUICAO FOI DESTE PRODUTO
    if request.method == 'POST':
        error = None
        name = request.form.get('name')
        value_contributed = float(request.form.get('value_contributed')) if request.form.get('value_contributed') else None
        message = request.form.get('message')

        if not name:
            error = 'Pedimos desculpa, mas precisamos de um nome para poder registar a contribuição'
        if not value_contributed:
            error = 'Pedimos desculpa, mas precisamos de um valor para poder registar a contribuição'

        if error is None:
            contribution = Contribution(name=name,value_contributed=value_contributed,product_id=product.id)
            if message:
                contribution.message = message
            contribution.create()

            product.price_paid += value_contributed
            product.save()

            return redirect(url_for('products.product',product_id=product.id,contribution_id=contribution.id))
        flash(error)
    return render_template('products/product.html',product=product,contribution=contribution)
