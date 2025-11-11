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

        # Ses dosyasını yükle
        audio = AudioSegment.from_wav(wav_path)
        
        # Ses dosyasını 30 saniyelik parçalara böl
        chunk_length_ms = 30000  # 30 saniye
        chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
        
        st.info(f"🎧 Ses {len(chunks)} parçaya bölündü ve çözümleniyor...")
        
        # Her parçayı tanıma
        recognizer = sr.Recognizer()
        full_text = []
        
        progress_bar = st.progress(0)
        for idx, chunk in enumerate(chunks):
            # Her parçayı geçici WAV dosyası olarak kaydet
            chunk_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
            chunk.export(chunk_path, format="wav")
            
            try:
                with sr.AudioFile(chunk_path) as source:
                    audio_data = recognizer.record(source)
                    chunk_text = recognizer.recognize_google(audio_data, language="tr-TR")
                    full_text.append(chunk_text)
            except sr.UnknownValueError:
                st.warning(f"⚠️ {idx + 1}. parça anlaşılamadı, atlaniyor...")
            except sr.RequestError as e:
                st.error(f"❌ Google API hatası: {e}")
                raise
            finally:
                os.unlink(chunk_path)
            
            progress_bar.progress((idx + 1) / len(chunks))
        
        text = " ".join(full_text)

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
