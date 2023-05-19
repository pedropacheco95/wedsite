from . import main
from . import api
from . import products
from . import honeymoon
from . import confirmations
from . import editor
from . import auth

# Register Blueprints
def register_blueprints(app):
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(honeymoon.bp)
    app.register_blueprint(confirmations.bp)
    app.register_blueprint(editor.bp)
    app.register_blueprint(auth.bp)
    return True