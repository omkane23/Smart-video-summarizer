
# 🎬 Smart Video Summarizer

A powerful and user-friendly Streamlit application that allows you to upload a video, extract key frames, apply visual enhancements, and generate a summarized video with optional audio and watermark.

---

## 🚀 Features

- 📁 **Video Upload**: Supports `.mp4`, `.avi`, `.mov` formats
- 🧠 **Key Frame Extraction**: Detects frames with visual differences
- 🎨 **Filters**:
  - Grayscale
  - Sepia
  - Brightness & Contrast adjustments
- 🔊 **Audio Options**:
  - Retain original audio
  - Mute audio
- 📝 **Watermarking**: Add custom watermark text
- 📥 **Download Summarized Video**

---

## 🛠 Built With

- Python
- Streamlit
- OpenCV
- MoviePy
- NumPy

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/smart-video-summarizer.git
cd smart-video-summarizer

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser to use the app.

---

## 📄 Project Structure

```
smart-video-summarizer/
├── app.py              # Streamlit application script
├── README.md           # Project documentation
├── requirements.txt    # Python package requirements
```

---

## ✨ Future Ideas

- Add watermark positioning options
- Allow manual frame selection
- Display summary preview before download

---

## 👨‍💻 Author

**Krushna** – Built using Streamlit, OpenCV, and MoviePy

---

## 📜 License

This project is licensed under the MIT License.
