import streamlit as st
from googletrans import Translator
import speech_recognition as sr
import tempfile
from pydub import AudioSegment

# Set Streamlit UI config
st.set_page_config(page_title="AI Translator", layout="centered")

# App title
st.markdown("<h1 style='text-align: center;'>🌐 AI-Powered Translator</h1>", unsafe_allow_html=True)
st.markdown("#### Speak or type, and break language barriers in real-time!")

# Language dictionary
languages = {
    'English': 'en', 'Hindi': 'hi', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
    'Chinese (Simplified)': 'zh-cn', 'Japanese': 'ja', 'Korean': 'ko', 'Arabic': 'ar', 'Russian': 'ru'
}

# Input mode selection
input_mode = st.radio("Choose input method:", ["📝 Text", "🎤 Voice"])

input_text = ""

# Handle Text Input
if input_mode == "📝 Text":
    input_text = st.text_area("Enter the text to translate:")

# Handle Voice Input
else:
    st.info("Record your voice message (in supported languages).")
    audio_file = st.file_uploader("Upload voice (WAV/MP3)", type=["wav", "mp3"])

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            sound = AudioSegment.from_file(audio_file)
            sound.export(temp_audio.name, format="wav")

            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_audio.name) as source:
                audio_data = recognizer.record(source)
                try:
                    input_text = recognizer.recognize_google(audio_data)
                    st.success(f"Detected Text: {input_text}")
                except sr.UnknownValueError:
                    st.error("Could not understand audio.")
                except sr.RequestError:
                    st.error("Speech Recognition API unavailable.")

# Language selection
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("From Language", list(languages.keys()), index=0)
with col2:
    target_lang = st.selectbox("To Language", list(languages.keys()), index=1)

# Translate
if st.button("🌍 Translate"):
    if input_text.strip() == "":
        st.warning("Please enter or record text first.")
    else:
        translator = Translator()
        try:
            translated = translator.translate(input_text, src=languages[source_lang], dest=languages[target_lang])
            st.markdown("---")
            st.markdown("### 🎯 Translated Output")
            st.success(translated.text)
        except Exception as e:
            st.error(f"Translation failed: {e}")
