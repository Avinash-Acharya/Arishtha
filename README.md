# Arishtha

A 'Content Moderation Tool' utilizing Multimodal Agentic approach which can be embedded within an Browser.

## Demo

![Demo](./media/demo.gif)

_Figure 1: Demo_

![App Screenshot](/media/nvidiaArchi2.png)

_Figure 2: Process-Flow/Architecture Diagram_

## Getting Started

### Prerequisites:

- Have [NVIDIA AI Workbench](https://www.nvidia.com/en-in/deep-learning-ai/solutions/data-science/workbench/) Program Installed. ([Reference](https://docs.nvidia.com/ai-workbench/user-guide/latest/installation/overview.html))
- [Docker](https://www.docker.com/products/container-runtime/).
- WSL2 ( This will be Installed with the Workbench, if not Installed in prior )

### Environment Variables:

To run this project, you will be needing the following environment variable. Where to add one will be discussed later.

`GEMINI_API_KEY` - This can be accessed from [Google AI Studio](https://aistudio.google.com/app/prompts/new_chat/?utm_source=hackathon&utm_medium=referral&utm_campaign=Devfolio&utm_content=)

`NVIDIA_API_KEY` - This can be accessed from [NVIDIA NIM](https://build.nvidia.com/nim)

`ELEVENLABS_API_KEY` - This can be accessed from [ElevenLabs](https://elevenlabs.io/app/speech-synthesis/text-to-speech)

> Adding all the key are not necessary if you are not using those functionalities. But make sure to add random values and save it, or the **program will not run**.


## Run Locally

Open the newly installed NVIDIA AI Workbench from your system and follow the below mentioned comprehensive steps :

### 1. Choosing the Container Runtime :

Choose Docker as your container Runtime.

![App Screenshot](/media/dockr.png)

_Figure 3: Runtime Selection Process_

### 2. Cloning this Repo :

Choose a Location and clone this Repository.

```bash
https://github.com/Avinash-Acharya/Arishtha.git
```

![App Screenshot](/media/clone.png)

_Figure 4: Cloning This Repository_

### 3. Enter the Environment Variables:

Navigate to the `Environment` menu towards the left side panel and search for the `Secrets` where you need to enter the API Keys. 

![App Screenshot](/media/key.png)

_Figure 5: Adding Secret Environment Variable_

### 4. Start the Build:

Start the Build process by clicking on `Start Build` button 

![App Screenshot](/media/build_needed.png)

_Figure 6: Image during PreBuild_

![App Screenshot](/media/complete_build.png)

_Figure 7: Image during PostBuild_

### 5. Run the Application :

Navigate to the `Application` section under `Environment` and Run the Gradio Application.

**Port:** `http://localhost:10000/projects/Arishtha/applications/Gradio/`

![App Screenshot](/media/application.png)

_Figure 8: Running Gradio Application_



>**URL:** `https://nsfw-eg.vercel.app/` ⚠️Harsh Words WARNING!!⚠️
_(This Webpage was built for testing purpose only)_

## License

MIT
