from fastapi import FastAPI
from pydantic import BaseModel
import random
import pandas as pd

# 前処理
## 対話ファイル読み込み
taiwa = pd.read_csv("taiwa.csv")
previous_comments = taiwa["previous_comment"].values
comments = taiwa["comment"].values

def bigram(text):
  for i in range(len(text)-1):
    yield text[i:i+2]

## 辞書作成
t_dict = {}
for i, com in enumerate(previous_comments):
  com = com.replace("\n", "")
  bi_list = set(bigram(com))
  for bi in bi_list:
    if not bi in t_dict:
      t_dict[bi] = []
    t_dict[bi].append(i)

# 返答
def respond(comment):
  # 2-gramでマッチするやつを拾ってきて適当にサンプリング
  com_bi = set(bigram(comment))
  scores = []
  for bi in com_bi:
    if not bi in t_dict:
      continue
    scores.extend(t_dict[bi])
  return comments[random.choice(scores)]


# 以下API処理

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

class Chat(BaseModel):
  message: str = "あいう"

@app.post("/chat")
def chat_responce(chat: Chat):
  return {"response": respond(chat.message)}