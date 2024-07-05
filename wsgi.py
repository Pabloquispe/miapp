import os
from app import create_app

# Obtener el nombre de la configuración desde las variables de entorno, usar 'default' si no está establecido
config_name = os.getenv('FLASK_CONFIG', 'default')

# Crear la aplicación Flask con la configuración especificada
app = create_app(config_name)

# Asegurarse de que la aplicación solo se ejecute si este script es ejecutado directamente
if __name__ == "__main__":
    # En producción, Gunicorn manejará la ejecución de la aplicación
    # Pero si estás ejecutando localmente, puedes usar el servidor de desarrollo de Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
