from flask import Blueprint, request, jsonify
from app.services.storage_services import save_to_local, upload_to_s3

image_routes = Blueprint('image_routes', __name__)

@image_routes.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        
        # save to local
        local_path = save_to_local(file)
        
        # upload to s3
        file_url = upload_to_s3(file)
        
        return jsonify({
            "message": "File uploaded successfully",
            #"url": local_path,
            "url": file_url
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
        