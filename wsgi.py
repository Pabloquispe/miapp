import os
from app import create_app

# Obtener el nombre de la configuración desde las variables de entorno, usar 'default' si no está establecido
config_name = os.getenv('FLASK_CONFIG', 'default')

# Crear la aplicación Flask con la configuración especificada
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
