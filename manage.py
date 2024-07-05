import os
import sys
from flask import Flask
from flask_migrate import Migrate, upgrade
from config import config_by_name
from modelos.models import db
from controladores.admin_routes import admin_bp
from controladores.user_routes import user_bp
from controladores.auth_routes import auth_bp
from controladores.main_routes import main_bp
from flask_script import Manager, Command
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_app(config_name):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, template_folder='vistas/templates', static_folder='vistas/static')
    app.config.from_object(config_by_name[config_name])
    
    # Inicializar la base de datos
    db.init_app(app)
    migrate = Migrate(app, db)

    # Registrar Blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    with app.app_context():
        from controladores.routes import register_routes
        register_routes(app)
        db.create_all()

    return app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

class DBUpgrade(Command):
    """Actualiza la base de datos a la última versión."""
    def run(self):
        with app.app_context():
            upgrade()

manager.add_command('db_upgrade', DBUpgrade())

@manager.command
def run():
    """Ejecuta la aplicación Flask."""
    app.run(debug=(os.getenv('FLASK_CONFIG') == 'dev'))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'db':
        with app.app_context():
            upgrade()
    else:
        manager.run()
