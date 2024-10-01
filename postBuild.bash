#!/bin/bash
# This file contains bash commands that will be executed at the end of the container build process,
# after all system packages and programming language specific package have been installed.
#
# Note: This file may be removed if you don't need to use it
pip install fastapi==0.112.2

# Check if the required Python dependencies are installed
pip install torch transformers

# Load the Falcon's NSFW Image Detection Model
python3 -c "
from transformers import AutoModelForImageClassification, ViTImageProcessor
MODEL = 'Falconsai/nsfw_image_detection'
model = AutoModelForImageClassification.from_pretrained(MODEL)
processor = ViTImageProcessor.from_pretrained(MODEL)
print('Falcon NSFW Image Detection model preloaded.')
"

# Load the Facebook RoBERTa Hate Speech Detection Model
python3 -c "
from transformers import AutoModelForSequenceClassification, AutoTokenizer
location = 'facebook/roberta-hate-speech-dynabench-r4-target'
HFtokenizer = AutoTokenizer.from_pretrained(location)
HFmodel = AutoModelForSequenceClassification.from_pretrained(location)
print('Facebook RoBERTa Hate Speech Detection model preloaded.')
"

# Load the Falcon Text Summarization Model
python3 -c "
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
SUM_MODEL_ID = 'Falconsai/text_summarization'
Stokenizer = AutoTokenizer.from_pretrained(SUM_MODEL_ID)
Smodel = AutoModelForSeq2SeqLM.from_pretrained(SUM_MODEL_ID)
print('Falcon Text Summarization model preloaded.')
"

# Load the Wav2Vec2 Speech-to-Text Model
python3 -c "
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
S2T_MODEL_ID = 'jonatasgrosman/wav2vec2-large-xlsr-53-english'
processor = Wav2Vec2Processor.from_pretrained(S2T_MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(S2T_MODEL_ID)
print('Wav2Vec2 Speech-to-Text model preloaded.')
"

echo "All models preloaded successfully."
