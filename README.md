# 🎙️ Audio/Video to Text Converter

A user-friendly web application that converts audio and video files to text using speech recognition technology.

## ✨ Features

- 🎵 **Audio File Support**: MP3, WAV formats
- 🎥 **Video File Support**: Extract audio from MP4 files and convert to text
- 🔄 **Auto Chunking**: Splits long audio files into 30-second segments
- 🏃 **Real-time Progress**: Live progress tracking during conversion
- ✏️ **Text Editing**: Edit converted text directly in the app
- 💾 **Download Option**: Export text as TXT file
- 📋 **Copy Support**: Easy copy to clipboard
- 🌍 **Multi-language**: Supports Turkish language recognition

## 🚀 Installation

### Requirements

- Python 3.7+
- FFmpeg

### FFmpeg Installation

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from official website
```

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

### Python Dependencies

1. Clone or download the project files
2. Install required packages:

```bash
pip install streamlit pydub speechrecognition
```

## 🎯 Usage

1. **Run the application:**
   ```bash
   streamlit run app.py
   ```

2. **Upload a file:**
   - Supported formats: MP3, WAV, MP4
   - Click "Browse files" or drag and drop your file

3. **Wait for processing:**
   - The app will automatically convert video to audio (if needed)
   - Audio is split into 30-second chunks
   - Each chunk is processed through Google Speech Recognition API

4. **Review and edit:**
   - Edit the converted text in the text area
   - Download as TXT file or copy to clipboard

## ⚙️ Technical Details

### File Processing Flow:
1. Uploaded file is saved to temporary storage
2. MP4 files are converted to WAV using FFmpeg
3. MP3 files are converted to WAV using pydub
4. Audio is split into 30-second chunks
5. Each chunk is processed by Google Speech Recognition
6. Results are combined and displayed

### Dependencies:
- `streamlit`: Web application framework
- `pydub`: Audio file manipulation
- `speechrecognition`: Speech-to-text functionality
- `ffmpeg`: Video/audio processing (system dependency)

## 🛠️ Configuration

- **Chunk Size**: 30 seconds (adjustable in code)
- **Language**: Turkish (tr-TR) - can be modified
- **Sample Rate**: 44100 Hz
- **Channels**: 2 (stereo)

## ❗ Limitations

- Requires internet connection (uses Google Speech Recognition API)
- Maximum file size depends on available memory
- Processing time varies with file length and internet speed
- Accuracy depends on audio quality and speaker clarity

## 🐛 Troubleshooting

**Common Issues:**

1. **FFmpeg not found**: Ensure FFmpeg is installed and in system PATH
2. **Conversion errors**: Check if the audio file is corrupted
3. **No speech detected**: Verify audio contains clear speech and adequate volume
4. **API errors**: Check internet connection and Google Speech Recognition service status

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
