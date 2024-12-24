from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import torchaudio
import torchaudio.transforms as transforms
import torch
import os

# Function to convert .m4a to .wav
def convert_m4a_to_wav(audio_path):
    """Converts an .m4a file to .wav format."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"The file {audio_path} does not exist.")
    
    audio = AudioSegment.from_file(audio_path)
    wav_path = audio_path.replace(".m4a", ".wav")
    audio.export(wav_path, format="wav")
    return wav_path

# Function to load the Whisper model and processor
def load_whisper_model(model_name="openai/whisper-tiny.en"):
    """Loads the Whisper model and processor."""
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)
    model.config.forced_decoder_ids = None
    return processor, model

# Function to preprocess and transcribe audio
def transcribe_audio(audio_path, processor, model):
    """Preprocesses and transcribes an audio file."""
    # Convert .m4a to .wav if necessary
    if audio_path.endswith(".m4a"):
        audio_path = convert_m4a_to_wav(audio_path)
    
    # Load the audio file
    waveform, sample_rate = torchaudio.load(audio_path)

    # Resample to 16 kHz if needed
    if sample_rate != 16000:
        resampler = transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)

    # Convert audio to input features
    input_features = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt").input_features

    # Generate token ids (set language='en' to force translation to English)
    predicted_ids = model.generate(input_features)
    
    # Decode token ids to text
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription