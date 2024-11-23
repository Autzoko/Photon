from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.services.storage_services import save_to_local, upload_to_s3
from app.models.image import Image
from app.models.user import User
from app.extensions import db
from app.utils.file_check import allowed_file
from uuid import uuid4

image_routes = Blueprint('image_routes', __name__)

@image_routes.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        unique_filename = f'{uuid4().hex}_{original_filename}'
        
        try:
            s3_key = f'{user_id}/{unique_filename}'
            file_url = upload_to_s3(file, s3_key)
            
            new_image = Image(filename=unique_filename, original_filename=original_filename, url=file_url, user_id=user.id)
            db.session.add(new_image)
            db.session.commit()
            
            return jsonify({
                "message": "File uploaded successfully",
                "url": file_url
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        