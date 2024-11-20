from flask import Flask

from app.routes import image_routes
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(image_routes.image_routes, url_prefix='/api/images')
    
    return app