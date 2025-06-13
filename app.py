import streamlit as st
import cv2
import os
import numpy as np
from moviepy.editor import VideoFileClip
import tempfile

# Set Streamlit UI layout
st.set_page_config(layout="centered", page_title="Smart Video Summarizer")
st.title("🎬 Smart Video Summarizer")

# Sidebar: Upload video
st.sidebar.header("📁 Upload Video")
video_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])

# Sidebar: Filters
st.sidebar.header("🧪 Key Frame Filters")
filter_option = st.sidebar.radio("Choose a filter to apply on key frames:", ("None", "Grayscale", "Sepia"))
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)

# Sidebar: Audio
st.sidebar.header("🔊 Audio Options")
keep_audio = st.sidebar.radio("Audio in summarized video:", ("Keep", "Mute"))

# Sidebar: Watermark
st.sidebar.header("📝 Watermark")
add_watermark = st.sidebar.checkbox("Add Watermark to Video", value=True)
watermark_text = st.sidebar.text_input("Watermark Text", "Created by Krushna")

# Function to apply filters and watermark
def apply_filters(image, filter_option, brightness, contrast, watermark_text=None):
    enhanced = cv2.convertScaleAbs(image, alpha=contrast, beta=(brightness - 1) * 100)

    if filter_option == "Grayscale":
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
    elif filter_option == "Sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        enhanced = cv2.transform(enhanced, kernel)
        enhanced = np.clip(enhanced, 0, 255)

    if watermark_text:
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (10, image.shape[0] - 10)
        font_scale = 0.6
        color = (255, 255, 255)
        thickness = 2
        cv2.putText(enhanced, watermark_text, position, font, font_scale, color, thickness, cv2.LINE_AA)

    return enhanced.astype(np.uint8)

# Function to add audio using moviepy
def add_audio_to_video(original_video_path, new_video_path, final_output_path, keep_audio=True):
    video_clip = VideoFileClip(new_video_path)
    if keep_audio:
        original_clip = VideoFileClip(original_video_path)
        video_clip = video_clip.set_audio(original_clip.audio)
    else:
        video_clip = video_clip.without_audio()

    video_clip.write_videofile(final_output_path, codec='libx264', audio_codec='aac')

# Main Logic
if video_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    video_path = tfile.name

    st.video(video_file)
    st.write("Extracting key frames and processing video... Please wait.")

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    success, prev = cap.read()
    frame_no = 1
    key_frames = [prev]

    while True:
        success, frame = cap.read()
        if not success:
            break
        diff = cv2.absdiff(cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY), cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        non_zero_count = np.count_nonzero(diff)
        if non_zero_count / diff.size > 0.02:
            key_frames.append(frame)
        prev = frame
        frame_no += 1

    cap.release()

    height, width, _ = key_frames[0].shape
    output_path_no_audio = os.path.join(tempfile.gettempdir(), "output_no_audio.mp4")
    out = cv2.VideoWriter(output_path_no_audio, cv2.VideoWriter_fourcc(*"mp4v"), 1, (width, height))

    for frame in key_frames:
        if add_watermark:
            enhanced = apply_filters(frame, filter_option, brightness, contrast, watermark_text)
        else:
            enhanced = apply_filters(frame, filter_option, brightness, contrast, None)
        out.write(enhanced)

    out.release()

    final_output_path = os.path.join(tempfile.gettempdir(), "final_summary.mp4")
    add_audio_to_video(video_path, output_path_no_audio, final_output_path, keep_audio == "Keep")

    with open(final_output_path, "rb") as f:
        st.success("✅ Video summarization completed!")
        st.download_button("📥 Download Summarized Video", f, file_name="summary.mp4")

