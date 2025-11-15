"""
Simple test script to verify all emotion detection services work
"""
import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        from services.image_emotion import analyze_image_emotion
        print("✓ Image emotion service imported")
    except Exception as e:
        print(f"✗ Image emotion service import failed: {e}")
        return False
    
    try:
        from services.audio_emotion import analyze_audio_emotion
        print("✓ Audio emotion service imported")
    except Exception as e:
        print(f"✗ Audio emotion service import failed: {e}")
        return False
    
    try:
        from services.text_emotion import analyze_text_emotion
        print("✓ Text emotion service imported")
    except Exception as e:
        print(f"✗ Text emotion service import failed: {e}")
        return False
    
    try:
        from services.fusion import fuse_emotions
        print("✓ Fusion service imported")
    except Exception as e:
        print(f"✗ Fusion service import failed: {e}")
        return False
    
    return True

def test_text_service():
    """Test text emotion detection"""
    print("\nTesting text emotion detection...")
    try:
        from services.text_emotion import analyze_text_emotion
        
        test_texts = [
            "I am very happy today!",
            "This is so sad and depressing.",
            "I'm really angry about this!"
        ]
        
        for text in test_texts:
            result = analyze_text_emotion(text)
            print(f"  Text: '{text}'")
            print(f"  → Emotion: {result['emotion']}, Confidence: {result['confidence']:.2f}")
        
        print("✓ Text emotion detection working")
        return True
    except Exception as e:
        print(f"✗ Text emotion detection failed: {e}")
        return False

def test_fusion():
    """Test fusion module"""
    print("\nTesting fusion module...")
    try:
        from services.fusion import fuse_emotions
        
        # Mock results
        modalities = [
            ('image', {'emotion': 'happy', 'confidence': 0.8, 'scores': {'happy': 0.8, 'neutral': 0.2}}),
            ('audio', {'emotion': 'neutral', 'confidence': 0.6, 'scores': {'neutral': 0.6, 'happy': 0.4}}),
            ('text', {'emotion': 'joy', 'confidence': 0.9, 'scores': {'joy': 0.9, 'neutral': 0.1}})
        ]
        
        result = fuse_emotions(modalities)
        print(f"  Fused Emotion: {result['emotion']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Modalities used: {result['modalities_used']}")
        print("✓ Fusion module working")
        return True
    except Exception as e:
        print(f"✗ Fusion module failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🧪 Testing Multimodal Emotion Detection Services")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        print("\n❌ Import tests failed. Please install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Test text service (doesn't require files)
    if not test_text_service():
        all_passed = False
    
    # Test fusion
    if not test_fusion():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        print("\nNote: Image and audio tests require actual files.")
        print("You can test them through the web interface at http://localhost:5000")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 60)

