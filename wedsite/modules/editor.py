from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from wedsite.models import *

bp = Blueprint('editor', __name__, url_prefix='/editor')

@bp.route('/', methods=('GET', 'POST'))
def index():
    apps = [
        {'name':'Produtos','url':url_for('editor.display_all',model='Product'),'app_image':url_for('static', filename='images/editor/app_images/product.png'),'style':'product_background_color'},
        {'name':'Contribuições','url':url_for('editor.display_all',model='Contribution'),'app_image':url_for('static', filename='images/editor/app_images/contribution.png'),'style':'contribution_background_color'},
        {'name':'Confirmações','url':url_for('editor.display_all',model='Confirmation'),'app_image':url_for('static', filename='images/editor/app_images/confirmation.png'),'style':'confirmation_background_color'},
        {'name':'Hotéis','url':url_for('editor.display_all',model='Hotel'),'app_image':url_for('static', filename='images/editor/app_images/hotel.png'),'style':'hotel_background_color'},
        {'name':'FAQs','url':url_for('editor.display_all',model='FAQ'),'app_image':url_for('static', filename='images/editor/app_images/faq.png'),'style':'faq_background_color'},
        {'name':'Utilizadores','url':url_for('editor.display_all',model='User'),'app_image':url_for('static', filename='images/editor/app_images/user.png'),'style':'user_background_color'},
        {'name':'Capítulos','url':url_for('editor.display_all',model='Chapter'),'app_image':url_for('static', filename='images/editor/app_images/chapter.png'),'style':'chapter_background_color'},
        {'name':'Website','url':url_for('editor.display_all',model='Client'),'app_image':url_for('static', filename='images/editor/app_images/client.png'),'style':'client_background_color'},
    ]
    return render_template('editor/index.html',page='editor_index',apps=apps)

@bp.route('/display/<model>', methods=('GET', 'POST'))
def display_all(model):
    page = f'editor_{model}_all'
    model = globals()[model]
    empty_instance = model()
    data = empty_instance.get_display_all_data()
    return render_template('editor/display_all.html', page=page, data=data)

@bp.route('/display/<model>/<id>', methods=('GET', 'POST'))
def display(model,id):
    page = f'editor_{model}'
    model = globals()[model]
    instance = model.query.filter_by(id=id).first()
    data = instance.get_display_data()
    return render_template('editor/display.html', page=page, data=data)

@bp.route('/create/<model>', methods=('GET', 'POST'))
def create(model):
    page = f'editor_{model}_create'
    model_name = model
    model = globals()[model_name]
    empty_instance = model()
    form = empty_instance.get_create_form()
    if request.method == 'POST':
        values = form.set_values(request)
        empty_instance.update_with_dict(values)
        empty_instance.create()
        return redirect(url_for('editor.display_all',model=model_name))
    data = empty_instance.get_create_data(form)
    return render_template('editor/create.html', page=page, data=data)

@bp.route('/kanban', methods=('GET', 'POST'))
def kanban():
    model = 'Racer'
    page = 'editor_kanban'
    page = f'editor_{model}_all'
    model = globals()[model]
    empty_instance = model()
    data = empty_instance.get_display_all_data()
    return render_template('editor/kanban.html',page=page, data=data)