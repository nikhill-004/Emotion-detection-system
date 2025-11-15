from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import tempfile
import uuid

from services.image_emotion import analyze_image_emotion
from services.audio_emotion import analyze_audio_emotion
from services.text_emotion import analyze_text_emotion
from services.fusion import fuse_emotions
import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = 'emotion-detection-secret-key'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'ogg'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/detect', methods=['POST'])
def detect_emotion():
    """Main endpoint for multimodal emotion detection"""
    try:
        results = {
            'image_emotion': None,
            'audio_emotion': None,
            'text_emotion': None,
            'final_emotion': None,
            'confidence': None,
            'error': None
        }
        
        temp_files = []
        
        print(f"DEBUG: Received request with files: {list(request.files.keys())}")
        print(f"DEBUG: Form data text: {request.form.get('text', '')[:50] if request.form.get('text') else 'None'}")
        
        # Process Image
        if 'image' in request.files:
            image_file = request.files['image']
            # Check if file exists and has content (filename might be empty for webcam)
            if image_file and image_file.filename:
                # Check if it's a valid image file
                if allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                    try:
                        filename = secure_filename(image_file.filename)
                        temp_path = os.path.join(tempfile.gettempdir(), filename)
                        image_file.save(temp_path)
                        temp_files.append(temp_path)
                        
                        image_result = analyze_image_emotion(temp_path)
                        results['image_emotion'] = image_result
                        print(f"DEBUG: Image emotion result: {image_result}")
                    except Exception as e:
                        error_msg = f"Image processing error: {str(e)}"
                        results['error'] = error_msg
                        print(f"DEBUG: {error_msg}")
                        import traceback
                        traceback.print_exc()
            elif image_file:
                # Handle case where filename is empty (e.g., webcam blob)
                try:
                    filename = f"temp_image_{uuid.uuid4().hex}.jpg"
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                    image_file.save(temp_path)
                    temp_files.append(temp_path)
                    
                    image_result = analyze_image_emotion(temp_path)
                    results['image_emotion'] = image_result
                except Exception as e:
                    if not results['error']:
                        results['error'] = ""
                    results['error'] += f" Image processing error: {str(e)}"
        
        # Process Audio
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file and audio_file.filename and allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
                try:
                    filename = secure_filename(audio_file.filename)
                    temp_path = os.path.join(tempfile.gettempdir(), filename)
                    audio_file.save(temp_path)
                    temp_files.append(temp_path)
                    
                    audio_result = analyze_audio_emotion(temp_path)
                    results['audio_emotion'] = audio_result
                except Exception as e:
                    if not results['error']:
                        results['error'] = ""
                    results['error'] += f" Audio processing error: {str(e)}"
        
        # Process Text
        text_input = request.form.get('text', '').strip()
        if text_input:
            try:
                text_result = analyze_text_emotion(text_input)
                results['text_emotion'] = text_result
                print(f"DEBUG: Text emotion result: {text_result}")
            except Exception as e:
                error_msg = f" Text processing error: {str(e)}"
                if not results['error']:
                    results['error'] = ""
                results['error'] += error_msg
                print(f"DEBUG: {error_msg}")
                import traceback
                traceback.print_exc()
        
        # Fusion - combine all available modalities
        # Only include modalities that have valid emotion data
        modalities = []
        if results['image_emotion'] and results['image_emotion'].get('emotion'):
            modalities.append(('image', results['image_emotion']))
        if results['audio_emotion'] and results['audio_emotion'].get('emotion'):
            modalities.append(('audio', results['audio_emotion']))
        if results['text_emotion'] and results['text_emotion'].get('emotion'):
            modalities.append(('text', results['text_emotion']))
        
        if modalities:
            try:
                final_result = fuse_emotions(modalities, weights=config.MODALITY_WEIGHTS)
                results['final_emotion'] = final_result['emotion']
                results['confidence'] = final_result['confidence']
                results['all_scores'] = final_result['all_scores']
                results['individual_results'] = final_result.get('individual_results', {})
                print(f"DEBUG: Fusion result: {final_result}")
            except Exception as e:
                error_msg = f"Fusion error: {str(e)}"
                if not results['error']:
                    results['error'] = ""
                results['error'] += error_msg
                print(f"DEBUG: {error_msg}")
                import traceback
                traceback.print_exc()
        else:
            # No valid modalities - try to set final_emotion from any available result
            if results['image_emotion'] and results['image_emotion'].get('emotion'):
                results['final_emotion'] = results['image_emotion'].get('emotion', 'neutral')
                results['confidence'] = results['image_emotion'].get('confidence', 0.5)
            elif results['audio_emotion'] and results['audio_emotion'].get('emotion'):
                results['final_emotion'] = results['audio_emotion'].get('emotion', 'neutral')
                results['confidence'] = results['audio_emotion'].get('confidence', 0.5)
            elif results['text_emotion'] and results['text_emotion'].get('emotion'):
                results['final_emotion'] = results['text_emotion'].get('emotion', 'neutral')
                results['confidence'] = results['text_emotion'].get('confidence', 0.5)
            else:
                if not results['error']:
                    results['error'] = "No valid inputs provided. Please provide at least one of: image, audio, or text."
                print(f"DEBUG: No modalities available. Image: {results['image_emotion']}, Audio: {results['audio_emotion']}, Text: {results['text_emotion']}")
        
        # Ensure final_emotion is always set if we have any valid result
        if not results['final_emotion']:
            if results['image_emotion'] and results['image_emotion'].get('emotion'):
                results['final_emotion'] = results['image_emotion'].get('emotion', 'neutral')
                results['confidence'] = results['image_emotion'].get('confidence', 0.5)
            elif results['audio_emotion'] and results['audio_emotion'].get('emotion'):
                results['final_emotion'] = results['audio_emotion'].get('emotion', 'neutral')
                results['confidence'] = results['audio_emotion'].get('confidence', 0.5)
            elif results['text_emotion'] and results['text_emotion'].get('emotion'):
                results['final_emotion'] = results['text_emotion'].get('emotion', 'neutral')
                results['confidence'] = results['text_emotion'].get('confidence', 0.5)
        
        # Cleanup temp files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f"Server error: {str(e)}"}), 500

@app.route('/api/webcam', methods=['POST'])
def webcam_detect():
    """Endpoint for webcam image detection"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Save to temp file
        filename = secure_filename(image_file.filename)
        temp_path = os.path.join(tempfile.gettempdir(), f"webcam_{filename}")
        image_file.save(temp_path)
        
        try:
            image_result = analyze_image_emotion(temp_path)
            
            results = {
                'image_emotion': image_result,
                'final_emotion': image_result['emotion'],
                'confidence': image_result['confidence']
            }
            
            return jsonify(results)
        finally:
            # Cleanup
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
    
    except Exception as e:
        return jsonify({'error': f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', '0').strip().lower() in ('1', 'true', 'yes')
    # Disable auto-reloader in offline mode to avoid site-packages reload storms
    use_reloader = debug_mode and not config.OFFLINE_MODE
    app.run(debug=debug_mode, host='0.0.0.0', port=5000, use_reloader=use_reloader)

