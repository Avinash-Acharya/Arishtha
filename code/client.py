import os
import gradio as gr
from bs4 import BeautifulSoup
from scrape import scrape_content
from custom_css import DARK_THEME_CSS, LIGHT_THEME_CSS
from queuing import process_text_content, process_image_content, process_url_content, process_audio_content

aud = None
soup = None

def process_content(url, toggle_state1, toggle_state2, toggle_state3, highlight_changes, text_model, sum_model):

    print(f"Text Model is "+text_model)
    print(f"Summarization Model is "+sum_model)
    print("- Working on new URL...")

    global aud
    audio_summary = aud
    if audio_summary and os.path.exists(audio_summary):
        os.remove(audio_summary)
        audio_summary = None
    else:
        audio_summary = None

    json_result = None
    content, soup = scrape_content(url)
    if soup is None:
        yield "Error", content, json_result, audio_summary
    if not isinstance(content, dict):
        yield "Error", "Content is not a dictionary", json_result, audio_summary
        return
    
    for style in content.get('styles', []):
        soup.head.append(style)  
    custom_style_tag = soup.new_tag('style')
    custom_style_tag.string = DARK_THEME_CSS
    soup.head.append(custom_style_tag)

    if toggle_state3:
        custom_style_tag = soup.new_tag('style')
        custom_style_tag.string = LIGHT_THEME_CSS
        soup.head.append(custom_style_tag)
    
    for link in content.get('css_links', []):
        soup.head.append(link)  

    # for i, text in enumerate(content.get('text', [])):
    #     original_text = text
    #     processed_text = process_text_content(text)
    #     if highlight_changes and "c#@ng3d" in processed_text :
    #         print("Changes detected")
    #         print(f"Original text: {original_text}")
    #         print(f"Processed text: {processed_text}")
    #         processed_text = processed_text.replace("c#@ng3d", "")
    #         processed_text_html = f"<span class='highlight-old'>{original_text}</span><span class='highlight-new'>{processed_text}</span>"
    #         original_text = None
    #         processed_text = BeautifulSoup(processed_text_html, "html.parser")
    #     else:
    #         print("No changes detected")

    #     element = soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'a', 'li'])[i]

    #     if element.string:
    #         element.string.replace_with(processed_text)
    #     else:
    #         element = processed_text

    #     yield f"Processing text... ({i+1}/{len(content['text'])})", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary

    for i, text in enumerate(content.get('text', [])):
        original_text = text
        processed_text = process_text_content(text, text_model)

        if highlight_changes and "c#@ng3d" in processed_text:
            print("Changes detected")
            print(f"Original text: {original_text}")
            print(f"Processed text: {processed_text}")
            processed_text = processed_text.replace("c#@ng3d", "")
            processed_text_html = f"<span class='highlight-old'>{original_text}</span><span class='highlight-new'>{processed_text}</span><br>"
            processed_text = BeautifulSoup(processed_text_html, "html.parser")
        else:
            print("No changes detected")
            processed_text = processed_text.replace("c#@ng3d", "")

        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'span', 'a', 'li']):
            if element.string and element.string == original_text:
                element.string.replace_with(processed_text)
                break

        yield f"Processing text...({i+1}/{len(content['text'])})", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary
    
    for i, img_src in enumerate(content['images']):
        processed_image = process_image_content(img_src) 
        soup.find_all('img')[i]['src'] = processed_image
        yield f"Processing images... ({i+1}/{len(content['images'])})", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary

    toggledPrior2 = False
    if toggle_state2 and not toggledPrior2:
        yield "Generating audio summary...", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary
        audio_summary = process_audio_content(url, sum_model)
        if audio_summary == "Content is too short to summarize. Less than 200 characters.":
            audio_summary = None
            print("Content is too short to summarize. Less than 200 characters.")
        aud = audio_summary
        toggledPrior2 = True
        yield "Audio Summary Generated", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary


    toggledPrior1 = False
    if toggle_state1 and not toggledPrior1:
        yield "Analyzing News Credibility...", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary
        json_result = process_url_content(url, sum_model) 
        toggledPrior = True
        yield "News Credibility Analyzed", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary

        
    yield "Processing complete", soup.prettify(formatter='html').encode('utf-8').decode('utf-8'), json_result, audio_summary


js_dark="""
        () => {
            document.body.classList.toggle('dark');
        }
        """

# 'allenai/gradio-theme' 'YTheme/Minecraft'

# gradio interface
with gr.Blocks(theme='allenai/gradio-theme') as demo:
    with gr.Tab("Dashboard"):
        with gr.Row():
            with gr.Column(scale=10):
                url_input = gr.Textbox(label="Enter URL", placeholder="https://example.com")
                gr.Examples(
                    examples=["https://nsfw-eg.vercel.app/", "https://www.nbcnews.com/health/health-news/fewer-1-5-large-companies-health-plans-cover-weight-loss-drugs-survey-rcna174345"],
                    inputs=url_input,
                    label="Example URLs"
                )
                submit_btn = gr.Button("Analyze URL")

            with gr.Column(variant="panel",scale=1):
                with gr.Row():
                    toggle_dark = gr.Checkbox(label="Toggle to Light Mode ", value=False)
                with gr.Row():
                    toggle_button1 = gr.Checkbox(label="Toggle to Analyse the Credibility of the article", value=False)
                    toggle_button2 = gr.Checkbox(label="Toggle to Get an Audio Summary of this Page", value=False)
                with gr.Row():
                    highlight_changes = gr.Checkbox(label="Highlight Changes", value=False)
        
        with gr.Row():
            status_output = gr.Label(label="Status")
            json_output = gr.JSON(label="Article Credibility Analysis")
            audio_output = gr.Audio(label="Audio Summary")
        html_output = gr.HTML(label="Modified Webpage")

    with gr.Tab("Models"):
        with gr.Column():
            gr.Markdown("## Pick the Model for the Task you want to perform")
            with gr.Row():
                text_model = gr.Dropdown(["Google's Gemini", "meta/llama-3.1-405b-instruct [NVIDIA NIM]", "meta/llama-3.1-8b-instruct [NVIDIA NIM]"], label="Inappropriate-words/Hate-speech Replacer", info="Pick the Model")
            with gr.Row():
                sum_model = gr.Dropdown(["Facebook BART CNN", "ibm/granite-3.0-8b-instruct [NVIDIA NIM]", "google/gemma-2b [NVIDIA NIM]"], label="Summarization Model", info="Pick the Model")
            if text_model == "meta/llama-3.1-405b-instruct [NVIDIA NIM]" or text_model == "meta/llama-3.1-8b-instruct [NVIDIA NIM]" or sum_model == "ibm/granite-3.0-8b-instruct [NVIDIA NIM]" or sum_model == "google/gemma-2b [NVIDIA NIM]" and not os.getenv("NVIDIA_API_KEY", False):
                gr.Alert("NVIDIA_API_KEY not set", color="red")

    submit_btn.click(process_content, inputs=[url_input, toggle_button1, toggle_button2, toggle_dark, highlight_changes, text_model, sum_model], outputs=[status_output, html_output, json_output, audio_output])    


proxy_prefix = os.environ.get("PROXY_PREFIX")
demo.launch(debug=True, server_name="0.0.0.0", server_port=8080, root_path=proxy_prefix)
# demo.launch(debug=True, server_name="0.0.0.0", server_port=8080)