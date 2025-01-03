import os
import json
import time
import torch
import librosa
import subprocess
from summarizer import summarize
from nvidiaNim import model_2_1, model_2_2
from news_fakery import fake_video_detector
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor , AutoTokenizer, AutoModelForSeq2SeqLM

S2T_MODEL_ID = "/tmp/models/wav2vec2_speech_to_text"
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = Wav2Vec2Processor.from_pretrained(S2T_MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(S2T_MODEL_ID)
model.to(device)

def download_audio(url, output_file, max_duration=60):
 
    print("- Downloading audio...")

    result = subprocess.run(
        ["yt-dlp", "--skip-download", "--print-json", url],
        stdout=subprocess.PIPE, text=True
    )
    video_info = json.loads(result.stdout)
    duration = video_info["duration"]  
    download_duration = min(max_duration, duration)
    subprocess.run([
        "yt-dlp", url,
        "-x", "--audio-format", "mp3",
        f"--postprocessor-args=-ss 00:00:00 -t {download_duration}",
        "-o", output_file
    ])

def transcribe_audio(audio_file):

    print("- Transcribing audio...")
    audio_data, _ = librosa.load(audio_file, sr=16000)
    inputs = processor(audio_data, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    predicted_sentence = processor.decode(predicted_ids[0])
    return predicted_sentence  

def summarize_text(text):

    print("- Summarizing text...")

    if s_model == 1:
        summarized = summarize(text)
    elif s_model == 2:
        summarized = model_2_1(text)
    elif s_model == 3:
        summarized = model_2_2(text)
    return summarized

def fake_video_news(url, modelNo):

    global s_model
    s_model = modelNo
    print("- Processing video...")
    start_time = time.time()
    output_file = "./audio.mp3"
    delete_after_process = True 
    download_audio(url, output_file)
    transcript = transcribe_audio(output_file)
    summary = summarize_text(transcript)
    result = fake_video_detector(summary)

    if delete_after_process and os.path.exists(output_file):
        os.remove(output_file)
        print(f"File {output_file} has been deleted.")

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken to analyze: {time_taken:.2f} seconds")
    
    return result

