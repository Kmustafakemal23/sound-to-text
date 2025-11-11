import streamlit as st
from pydub import AudioSegment
import tempfile
import os
import speech_recognition as sr
import subprocess

st.set_page_config(page_title="Speech to Text", page_icon="🎙️", layout="centered")

st.title("🎙️ Ses / Video'dan Yazıya Dönüştürme Aracı")

uploaded_file = st.file_uploader("Bir ses veya video dosyası yükleyin", type=["mp3", "wav", "mp4"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    wav_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

    try:
        if uploaded_file.name.endswith(".mp4"):
            st.info("🎥 Video dosyası algılandı, sesi çıkarılıyor...")

            # ffmpeg kullanarak sesi çıkart
            command = [
                "ffmpeg",
                "-i", temp_file_path,
                "-vn",  # video yok
                "-acodec", "pcm_s16le",  # WAV
                "-ar", "44100",
                "-ac", "2",
                wav_path,
                "-y"
            ]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        elif uploaded_file.name.endswith(".mp3"):
            sound = AudioSegment.from_mp3(temp_file_path)
            sound.export(wav_path, format="wav")

        else:
            sound = AudioSegment.from_wav(temp_file_path)
            sound.export(wav_path, format="wav")

        # Ses tanıma
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            st.info("🎧 Ses çözümleniyor, lütfen bekleyin...")
            text = recognizer.recognize_google(audio_data, language="tr-TR")

        st.success("✅ Dönüştürme tamamlandı!")
        edited_text = st.text_area("Metni düzenleyebilirsiniz:", value=text, height=300)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 TXT olarak indir"):
                temp_txt = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
                with open(temp_txt.name, "w", encoding="utf-8") as f:
                    f.write(edited_text)
                with open(temp_txt.name, "rb") as f:
                    st.download_button("📥 İndir", f, file_name="metin.txt")
        with col2:
            st.text_area("📋 Kopyalamak için metin:", value=edited_text, height=300)

    except Exception as e:
        st.error(f"❌ Hata oluştu: {e}")
