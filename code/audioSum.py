import os
import re
import uuid
from urllib import request
from dotenv import load_dotenv
from summarizer import summarize
from bs4 import BeautifulSoup as bs
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from nvidiaNim import model_2_1, model_2_2


load_dotenv()
VOICE_ID = "pFZP5JQG7iQjIQuC4Bku"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def load_content(url):

  print("- Loading and summarizing the article...")
  html = request.urlopen(url).read().decode('utf8')
  soupObj = bs(html, "html.parser")
  paras = soupObj.find_all('p')
  allPara = " "

  for para in paras:
    allPara = allPara + para.text
  allPara = re.sub(r'\xa0', '', allPara) 

  if len(allPara) < 200:
    return "Content is too short to summarize. Less than 200 characters."
  
  return allPara

def elevenlabs_tts(text):

  print("- Converting text to speech...")
  response = client.text_to_speech.convert(
        voice_id = VOICE_ID,  
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2",  # or use `eleven_multilingual_v2` for multilingual support
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )
  
  save_file_path = f"{uuid.uuid4()}.mp3"

  with open(save_file_path, "wb") as f:
      for chunk in response:
          if chunk:
              f.write(chunk)

  print(f"A new audio file was saved successfully at {save_file_path}")

  return save_file_path

def audio_summarize(url, modelNo):

  content = load_content(url)

  if content == "Content is too short to summarize. Less than 200 characters.":
    return content
  
  if modelNo == 1:
    summary = summarize(content)
  elif modelNo == 2:
    summary = model_2_1(content)
  elif modelNo == 3:
    summary = model_2_2(content)
  audio_path = elevenlabs_tts(summary)
  
  return audio_path