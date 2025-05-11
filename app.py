from flask import Flask, render_template, request, redirect, url_for, send_file, session, jsonify, Response
import os
import secrets
# from PIL import Image
from encoder import get_Password
from werkzeug.utils import secure_filename
from decoder import decrypt_image


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/transmit')
def transmit():
    return render_template('transmit.html')

@app.route('/receive')
def receive():
    return render_template('receive.html')

@app.route('/process_transmit', methods=['POST'])
def process_transmit():
    if request.method == 'POST':
        try:
            # Get form data
            keyword = request.form.get('keyword')
            prime_number = int(request.form.get('prime_number'))
            random_number = int(request.form.get('random_number'))
            secret_message = request.form.get('secret_message')
            
            print(f"Form data received: keyword={keyword}, prime={prime_number}, random={random_number}")
            
            # Get uploaded image
            if 'image' not in request.files:
                return jsonify({'error': 'No image uploaded'}), 400
            
            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({'error': 'No image selected'}), 400
            
            # Check if the file is a .png
            if not image_file.filename.lower().endswith('.png'):
                return jsonify({'error': 'Wrong file extension. Please upload a .png file.'}), 400
            
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)
            print(f"Image saved to: {filepath}")
            
            # Generate password
            print("Generating password...")
            password = get_Password(image_path=filepath, keyword=keyword, prime_number=prime_number, random_number=random_number)
            print(f"Password generated: {password}")
            
            # Create output filename and path
            output_filename = f"encoded_{filename}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            print(f"Output path will be: {output_path}")
            
            # Import encryption function and encrypt the image
            print("Starting image encryption...")
            from encoder import encrypt_image
            from visualise import vis
            # Check if function exists
            if not callable(encrypt_image):
                return jsonify({'error': 'encrypt_image function not found or not callable'}), 500
                
            # Call the encryption function
            try:
                encrypt_image(
                    image_path=filepath,
                    random_number=random_number,
                    secret_message=secret_message,
                    output_path=output_path
                )
                print(f"Encryption complete, checking if file exists: {output_path}")
                
                # Verify the file was created
                if os.path.exists(output_path):
                    print(f"File exists and has size: {os.path.getsize(output_path)} bytes")
                else:
                    print(f"ERROR: Output file was not created!")
                    
            except Exception as e:
                print(f"Error in encrypt_image function: {str(e)}")
                import traceback
                print(traceback.format_exc())
                return jsonify({'error': f'Encryption failed: {str(e)}'}), 500
            
            # Generate download URL
            download_url = url_for('download_file', filename=output_filename)
            
            return jsonify({
                'success': True,
                'password': password,
                'output_file': output_filename,
                'download_url': download_url
            })
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({'error': str(e), 'success': False}), 500

@app.route('/process_receive', methods=['POST'])
def process_receive():
    if request.method == 'POST':
        # Get password
        password = request.form.get('password')
        
        # Get uploaded image
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        
        try:
            # Call your decoder function to get the hidden message
            decoded_message = decrypt_image(filepath, password)
            
            return jsonify({
                'success': True,
                'message': decoded_message  # Include the decoded message in the response
            })
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            # For debugging - print the file we're looking for and what files exist
            print(f"Looking for: {file_path}")
            print(f"Files in directory: {os.listdir(app.config['UPLOAD_FOLDER'])}")
            return jsonify({'error': 'File not found'}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(f"Error in download_file: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port, debug=True)
    app.run(debug=True, port=8080)
    