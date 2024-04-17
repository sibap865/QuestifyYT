# YouTube_note_search
This project is helpful for searching notes from Youtube videos using RetrivalQA RAG on YouTube transcripts.

## About the YouTube_note_search chrome extension
* This Chrome extension is useful when you have watched a YouTube video but have not taken notes, which is much needed for revision.
* By using our Chrome extension, you can ask questions about the YouTube video. It will generate useful information only from the video with the help of RAG.

## How does it work?
* It consists of two parts: frontend and backend (two directories, frontend and backend).
* Whenever the user validates the url, the video transcript for that video will be stored in a vector database for easy retrival (it will take a while depending on the video size).
* In backend first url will be validated. 
* If the video is ready to search, user can ask questions about it.
* A LLM retrival chain retrives the relevent results from the retriver and show to end user.

## How to run?

### STEPS 01:

Clone the repository

```bash
https://github.com/sibap865/YouTube_note_search.git
```
### STEP 02- Create a conda environment after opening the repository

```bash
conda create -n geminienv python=3.10 -y
```

```bash
conda activate geminienv
```


### STEP 03- install the requirements
```bash
# go to backend folder and install the requirements
cd backend
pip install -r requirements.txt
```


```bash
# Finally run the following command
uvicorn app:app
```
### STEP 04- setup the Chrome Extension

* Open the Chrome browser and go to Extensions, then manage Extensions.
* Turn devloper mode on by clicking on devloper mode on the top right corner.
* Load unpacked folder i.e the frontend folder (because it contain manifest.json)
* Pin the YouTube_note_search chrome extension and open in any youtube education video and take advantage of YouTube note search feature (click on the chrome extension and use it).
### follow 💚 me in Github.
### Github: [Github](https://github.com/sibap865)

Connect with me for more projects like this 😊:
### LinkedIn: [My profile](https://www.linkedin.com/in/sibaprasad-naik-behera-98043b1ba/)