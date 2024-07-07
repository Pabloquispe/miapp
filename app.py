import os
from flask import Flask
from flask_migrate import Migrate
from config import config_by_name
from modelos.models import db

def create_app(config_name):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, template_folder='vistas', static_folder='vistas/static')
    app.config.from_object(config_by_name[config_name])
    
    # Inicializar la base de datos
    db.init_app(app)
    migrate = Migrate(app, db)

    # Registrar rutas
    with app.app_context():
        from controladores.routes import register_routes
        register_routes(app)
        db.create_all()

    return app

if __name__ == "__main__":
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app = create_app(config_name)
    app.run(debug=True)

