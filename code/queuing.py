import re
import json
import queue
import threading
from audioSum import audio_summarize
from video_model import fake_video_news
from text_model import detect_hate_speech
from image_model import detect_nsfw_image
from news_fakery import fake_news_detector
from ytlink import get_youtube_links_from_url

class Agent:
    """
    Agent class for processing text and image data concurrently.
    Attributes:
        text_queue (queue.Queue): Queue to hold text data for processing.
        image_queue (queue.Queue): Queue to hold image URLs for processing.
        processed_text (list): List to store processed text responses.
        processed_image (Any): Variable to store the processed image result.
        text_thread (threading.Thread): Thread for processing text data.
        image_thread (threading.Thread): Thread for processing image data.
    Methods:
        __init__(): Initializes the Agent with queues, processed data storage, and starts the processing threads.
        process_text(): Continuously processes text data from the text_queue, detects hate speech, and stores the result.
        process_image(): Continuously processes image URLs from the image_queue, detects NSFW content, and stores the result.
    """

    def __init__(self):
        self.text_queue = queue.Queue()
        self.image_queue = queue.Queue()
        self.processed_text = []
        self.processed_image = None
        self.text_thread = threading.Thread(target=self.process_text, daemon=True)
        self.image_thread = threading.Thread(target=self.process_image, daemon=True)
        self.text_thread.start()
        self.image_thread.start()

    def process_text(self):
        while True:
            try:
                sentence = self.text_queue.get(timeout=1)
                respond_text = detect_hate_speech(sentence, t_model)
                self.processed_text.append(respond_text)  
                self.text_queue.task_done()
            except queue.Empty:
                continue

    def process_image(self):
        while True:
            try:
                img_url = self.image_queue.get(timeout=1)
                self.processed_image = detect_nsfw_image(img_url, gImage)
                self.image_queue.task_done()
            except queue.Empty:
                continue


def process_text_content(text, text_model="default"):

    print("- Detecting hate speech...")
    global t_model
    t_model = 2 if text_model == "meta/llama-3.1-405b-instruct [NVIDIA NIM]" else 3 if text_model == "meta/llama-3.1-8b-instruct [NVIDIA NIM]" else 1
    splits = re.split(r'([.!?;:])', text)
    agent.processed_text.clear()
    sentence_buffer = ""

    for item in splits:
        if item:
            if item.strip() in ".!?;:":
                sentence_buffer += item
                agent.text_queue.put(sentence_buffer.strip())  
                sentence_buffer = ""  
            else:
                sentence_buffer = item  

    agent.text_queue.join()
    result = ' '.join(agent.processed_text)

    return result if result else text

def process_image_content(url, image=None):

    if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid URL: {url}")
        
    global gImage
    gImage = image 
    
    agent.processed_image = None  
    agent.image_queue.put(url)
    agent.image_queue.join()  

    return agent.processed_image

def process_url_content(url, sum_model="default"):

    article_response = fake_news_detector(url)
    article_response_json = json.loads(article_response)
    combined_response = {"Article": article_response_json}
    mNo = 2 if sum_model == "ibm/granite-3.0-8b-instruct [NVIDIA NIM]" else 3 if sum_model == "google/gemma-2b [NVIDIA NIM]" else 1

    if article_response_json['fake'] == False:
        ytlink_list = get_youtube_links_from_url(url)
        video_response = {}
        for i, link in enumerate(ytlink_list):
            response = fake_video_news(link, mNo)
            video_response[f"Video {i+1} with URL {link}"] = response
        combined_response["Video"] = video_response

    return combined_response

def process_audio_content(url, sum_model):
    
    mNo = 2 if sum_model == "ibm/granite-3.0-8b-instruct [NVIDIA NIM]" else 3 if sum_model == "google/gemma-2b [NVIDIA NIM]" else 1
    result = audio_summarize(url, mNo)
    
    return result

agent = Agent()
