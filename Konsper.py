# Импорт библиотек
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from googletrans import Translator
import json
import speech_recognition as sr
import tkinter as tk
from tkinter import *
import threading
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Создание переменных
translator = Translator()
global status
status = False
global threadstatus
threadstatus=False
global threadstatus1
threadstatus1=False
text = " "

# Функции
def copy():
  root.clipboard_clear()
  root.clipboard_append(text)
  root.update()

def to_eng():
  global text
  translation=translator.translate(text, dest="en")
  text = translation.text
  label.config(text=text)

def to_rus():
  global text
  translation=translator.translate(text, dest="ru")
  text = translation.text
  label.config(text=text)

def transcription():
  global threadstatus1
  threadstatus1=True
  global text
  parsed_data = json.loads(r.recognize_vosk(audio, language='ru-RU'))
  text = text + parsed_data["text"] + ". "
  label.config(text=text)
  threadstatus1=False

def summarize_text(text1, num_sentences=4):
  sentences = sent_tokenize(text1)
  stop_words = set(stopwords.words('russian'))
  processed_sentences = [' '.join([word for word in word_tokenize(sentence.lower()) if word.isalnum() and word not in stop_words]) for sentence in sentences]
  vectorizer = TfidfVectorizer()
  X = vectorizer.fit_transform(processed_sentences)
  scores = X.sum(axis=1).A1
  ranked_sentences = [sentences[i] for i in scores.argsort()[::-1]]
  summary = ' '.join(ranked_sentences[:num_sentences])
  x = False
  while x == False:
      if(threadstatus)==True or (threadstatus1)==True:
        time.sleep(0.5)
      else:
        x = True
  global text
  text=summary
  label.config(text=summary)

def potoki():
  g = threading.Thread(target = start)
  g.start()

def potoki2():
  w = threading.Thread(target = stop)
  w.start()

def start():
  global threadstatus
  threadstatus=True
  global audio
  global status
  status=True
  global r
  r = sr.Recognizer()
  sr.LANGUAGE = 'ru.RU'
  while status:
    with sr.Microphone() as sourse:
      r.adjust_for_ambient_noise(sourse)
      audio = r.listen(sourse)
      global x
      x = threading.Thread(target = transcription)
      x.start()
  threadstatus=False

def stop():
  global status
  status = False
  summarize_text(text)

# Создание и настройка окна
root = tk.Tk()
root.title("Конспект лекций")
root.geometry("300x300")
root.resizable(0,0)
start_btn = tk.Button(root,text="Начать",command=lambda : potoki())
start_btn.pack()
start_btn.place(x=0, y=30)
stop_btn = tk.Button(root,text="Закончить",command=lambda : potoki2())
stop_btn.pack()
stop_btn.place(x=60, y=30)
stop_btn = tk.Button(root,text="Скопировать",command=lambda : copy())
stop_btn.pack()
stop_btn.place(x=150, y=30)
stop_btn = tk.Button(root,text="Перевести на русский",command=lambda : to_rus())
stop_btn.pack()
stop_btn.place(x=0, y=0)
stop_btn = tk.Button(root,text="Перевести на английский",command=lambda : to_eng())
stop_btn.pack()
stop_btn.place(x=150, y=0)
label = Label(root, text=text, wraplength=300)
label.pack()
label.place(x=0, y=60)
root.mainloop()