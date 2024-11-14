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
import os
from transformers import AutoModelForImageClassification, ViTImageProcessor
MODEL = 'Falconsai/nsfw_image_detection'
save_directory = '/tmp/models/nsfw_image_detection'
if not os.path.exists('/tmp/models/nsfw_image_detection'):
    model = AutoModelForImageClassification.from_pretrained(MODEL)
    processor = ViTImageProcessor.from_pretrained(MODEL)
    model.save_pretrained(save_directory)
    processor.save_pretrained(save_directory)
print('Falcon NSFW Image Detection model preloaded.')
"

# Load the Facebook RoBERTa Hate Speech Detection Model
python3 -c "
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
location = 'facebook/roberta-hate-speech-dynabench-r4-target'
save_directory = '/tmp/models/roberta_hate_speech'
if not os.path.exists('/tmp/models/roberta_hate_speech'):
    HFtokenizer = AutoTokenizer.from_pretrained(location)
    HFmodel = AutoModelForSequenceClassification.from_pretrained(location)
    HFmodel.save_pretrained(save_directory)
    HFtokenizer.save_pretrained(save_directory)
print('Facebook RoBERTa Hate Speech Detection model preloaded.')
"

# Load the Falcon Text Summarization Model
python3 -c "
import os
from transformers import AutoTokenizer, BartForConditionalGeneration
fb = 'sshleifer/distilbart-cnn-12-6'
save_directory = '/tmp/models/bart_cnn_text_summarization'
if not os.path.exists('/tmp/models/bart_cnn_text_summarization'):
    try:
        model = BartForConditionalGeneration.from_pretrained(fb)
        tokenizer = AutoTokenizer.from_pretrained(fb)
        model.save_pretrained(save_directory)
        tokenizer.save_pretrained(save_directory)
    except Exception as e:
        print(f'An error occurred: {e}')
print('BART CNN Text Summarization model preloaded.')
"

# Load the Wav2Vec2 Speech-to-Text Model
python3 -c "
import os
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
S2T_MODEL_ID = 'jonatasgrosman/wav2vec2-large-xlsr-53-english'
save_directory = '/tmp/models/wav2vec2_speech_to_text'
if not os.path.exists('/tmp/models/wav2vec2_speech_to_text'):
    processor = Wav2Vec2Processor.from_pretrained(S2T_MODEL_ID)
    model = Wav2Vec2ForCTC.from_pretrained(S2T_MODEL_ID)
    model.save_pretrained(save_directory)
    processor.save_pretrained(save_directory)
print('Wav2Vec2 Speech-to-Text model preloaded.')
"

echo "All models preloaded successfully."
