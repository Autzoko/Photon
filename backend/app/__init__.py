from flask import Flask

from app.routes import image_routes, auth_routes
from app.config import Config
from app.extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    app.register_blueprint(image_routes.image_routes, url_prefix='/api/images')
    app.register_blueprint(auth_routes.auth_routes, url_prefix='/api/auth')
    
    with app.app_context():
        db.create_all()
    
    return app