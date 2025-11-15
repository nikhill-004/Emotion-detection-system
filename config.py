"""
Configuration file for multimodal emotion detection
"""
import os

# Modality weights for fusion (must sum to 1.0)
# User requirement: text: 0.4, audio: 0.3, image: 0.3
MODALITY_WEIGHTS = {
    'text': float(os.getenv('TEXT_WEIGHT', '0.4')),
    'audio': float(os.getenv('AUDIO_WEIGHT', '0.3')),
    'image': float(os.getenv('IMAGE_WEIGHT', '0.3'))
}

# Offline mode: when true, use lightweight local heuristics and avoid heavy model downloads
OFFLINE_MODE = os.getenv('OFFLINE_MODE', 'false').strip().lower() in ('1', 'true', 'yes')

# File upload settings
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = 'uploads'

# Model settings
DEEPFACE_BACKEND = 'opencv'  # or 'ssd', 'dlib', 'mtcnn', 'retinaface'
DEEPFACE_MODEL = 'VGG-Face'  # or 'Facenet', 'OpenFace', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace'

# SpeechBrain settings
SPEECHBRAIN_MODEL = "speechbrain/emotion-recognition-wav2vec2-IEMOCAP"
SPEECHBRAIN_SAVEDIR = "pretrained_models/emotion-recognition-wav2vec2-IEMOCAP"

# Transformers settings
TEXT_MODEL = "j-hartmann/emotion-english-distilroberta-base"

# Standard emotions
STANDARD_EMOTIONS = ['anger', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

