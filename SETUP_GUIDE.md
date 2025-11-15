# Multimodal Emotion Detection — Setup Guide

This guide walks you through installing every required library individually (with `pip install ...` commands), extra assets you may need, and how to run the application in both **online** and **offline** modes.

---

## 1. Prerequisites

1. **Python 3.10+** (3.10 or higher is recommended).  
   Download from https://www.python.org/downloads/ and make sure `python` / `pip` is on your PATH.
2. **Git** (optional, only if you clone the repository via Git).  
   Download from https://git-scm.com/downloads.
3. (Optional but recommended) **Virtual environment** to isolate dependencies:
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux
   source .venv/bin/activate
   ```

---

## 2. Install Required Libraries

> **Tip:** You can install everything at once with `pip install -r requirements.txt`. The commands below show individual installations in case you want to do them separately or troubleshoot specific packages.

| Library | Purpose | Install Command |
| ------- | ------- | ---------------- |
| Flask | Web application server | `pip install flask` |
| Werkzeug | Helper utilities (Flask dependency) | `pip install werkzeug` |
| DeepFace | Facial emotion detection | `pip install deepface` |
| OpenCV | Image processing (fallbacks, preprocessing) | `pip install opencv-python` |
| NumPy | Core numerical library | `pip install numpy` |
| pandas | Misc. data utilities (DeepFace dependency) | `pip install pandas` |
| Pillow | Image I/O (DeepFace dependency) | `pip install pillow` |
| SpeechBrain | Audio emotion classification | `pip install speechbrain` |
| librosa | Audio feature extraction (fallback) | `pip install librosa` |
| soundfile | Audio file reading | `pip install soundfile` |
| Transformers | Text emotion detection | `pip install transformers` |
| Torch | Required by SpeechBrain/Transformers | `pip install torch` |
| Torchaudio | Audio utilities (optional, SpeechBrain) | `pip install torchaudio` |
| SciPy | Signal processing helpers | `pip install scipy` |
| scikit-learn | Transformers dependency | `pip install scikit-learn` |
| Requests | HTTP utilities (DeepFace dependency) | `pip install requests` |
| tqdm | Progress bars (DeepFace dependency) | `pip install tqdm` |
| boto3 | Optional (SpeechBrain utilities) | `pip install boto3` |

You may already have several of these packages if you installed via `requirements.txt`. Re-running the commands is safe; pip will skip packages that are already installed.

---

## 3. Additional Assets / Model Downloads

When you run the app **online** for the first time, these models download automatically and are cached locally:

| Component | Model | Size | Triggered By |
| --------- | ----- | ---- | ------------ |
| Image | DeepFace (VGG-Face by default) | ≈ 100 MB | First image analysis |
| Audio | SpeechBrain wav2vec2 IEMOCAP | ≈ 500 MB | First audio analysis |
| Text | `j-hartmann/emotion-english-distilroberta-base` | ≈ 300 MB | First text analysis |

> Once downloaded, the cached models allow you to run completely offline (see the Offline Mode section below).

---

## 4. Running the Application

### 4.1 Online Mode (first-time setup / downloading models)

```powershell
# From the project directory
python app.py
```

Visit http://localhost:5000 in your browser. Upload an image/audio/text and click **Analyze Emotion**.  
Allow the first request for each modality to finish so the models are cached.

### 4.2 Offline Mode (after models are cached, or when you want lightweight heuristics)

```powershell
# Windows PowerShell
$env:OFFLINE_MODE="true"
python app.py
```

```bash
# macOS / Linux (bash/zsh)
export OFFLINE_MODE=true
python app.py
```

In offline mode the app:

- Uses cached DeepFace / SpeechBrain / Transformers models if they exist.
- Falls back to OpenCV + librosa + keyword heuristics when models are unavailable.
- Disables Flask’s auto-reloader to avoid restarts when running offline.

> **Recommended workflow:** Run the app once in online mode to download models, then restart with `OFFLINE_MODE=true` for reliable offline use.

---

## 5. Troubleshooting

| Issue | Quick Fix |
| ----- | --------- |
| `ImportError` or missing package | Re-run the relevant `pip install ...` command above, or install everything with `pip install -r requirements.txt`. |
| Audio analysis warning about torchaudio | Install/support `torchaudio`; if unavailable, the app automatically uses the librosa heuristic. |
| App reloading repeatedly offline | Ensure `OFFLINE_MODE` is set before launching; this disables Flask’s reloader. |
| “Failed to fetch” in browser | Confirm the Flask server is running in PowerShell and reachable at `http://localhost:5000`. |

---

## 6. Next Steps

- Review `README_MULTIMODAL.md` for architectural details.
- Customize modality weights in `config.py` if desired.
- Use `test_services.py` to sanity-check installations (`python test_services.py`).

Enjoy building with the Multimodal Emotion Detection system! 🎭


