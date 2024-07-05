import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_session import Session
from redis import Redis
from config import config_by_name
from modelos.models import db
from controladores.admin_routes import admin_bp
from controladores.user_routes import user_bp
from controladores.auth_routes import auth_bp
from controladores.main_routes import main_bp
from controladores.routes import register_routes
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_app(config_name):
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__, template_folder='vistas/templates', static_folder='vistas/static')
    app.config.from_object(config_by_name[config_name])

    # Configurar opciones del motor SQLAlchemy
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 3600,
    }

    # Configurar Redis para sesiones
    session_redis_url = app.config.get('SESSION_REDIS')
    if session_redis_url:
        app.config['SESSION_REDIS'] = Redis.from_url(session_redis_url)
        Session(app)
    else:
        raise ValueError("La configuración SESSION_REDIS no está definida o es None.")

    db.init_app(app)
    db.app = app

    migrate = Migrate(app, db)

    # Registrar Blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    register_routes(app)

    with app.app_context():
        db.create_all()

    # Configuración de logs
    configure_logging(app)

    # Manejo de errores personalizados
    configure_error_handlers(app)

    return app

def configure_logging(app):
    """Configura los logs de la aplicación."""
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Aplicación iniciada')

def configure_error_handlers(app):
    """Configura los manejadores de errores."""
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
