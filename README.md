# Podconvertation

An application capable of generating a presentation/video presentation from an audio file. Whatever it may be - a university lecture, podcast, and much more.


Instructions for use are provided below.

Start virtual environment
```
python -m venv venv
source venv/bin/activate
```
and run
```
pip install -r requirements.txt
```

To run FastAPI:
```
uvicorn app.main:app --reload --port 8000
```
Then open index.html in browser and enjoy.

For testing purposes, an MP3 file of an excerpt from the Lex Fridman with Guido Van Rossum podcast has been provided. [video](https://youtu.be/F2Mx-u7auUs?si=cHiRZ4nmOtuR8OqH)
