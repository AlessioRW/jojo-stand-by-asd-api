from fastapi import FastAPI
import numpy as np
import matplotlib.pyplot as plt
import time as Time
from fastapi.middleware.cors import CORSMiddleware
import cv2, base64, os, io

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def getNum(letter):
    if letter == '∞':
        return 100
    elif letter == 'A' :
        return 83.3
    elif letter == 'B':
        return 66.6
    elif letter == 'C':
        return 50 
    elif letter == 'D':
        return 33.3
    elif letter == 'E':
        return 16.6
    elif letter == '∅':
        return 0

def getNumSimple(letter):
    if letter == '∞':
        return 6
    elif letter == 'A' :
        return 5
    elif letter == 'B':
        return 4
    elif letter == 'C':
        return 3 
    elif letter == 'D':
        return 2
    elif letter == 'E':
        return 1
    elif letter == '∅':
        return 0
    


@app.post('/graph/{userScore}/{standScore}/{standName}')
def graph(userScore: str, standScore: str, standName: str):

    time = ''.join(str(Time.time()).split('.'))
    userStats = []
    for stat in userScore.split('-'):
        userStats.append(getNumSimple(stat))

    standStats = []
    for stat in standScore.split('-'):
        standStats.append(getNumSimple(stat))

    categories = ['Power', 'Speed', 'Range', 'Stamina', 'Precision', 'Potential']
    categories = [*categories, categories[0]]

    userStats = [*userStats, userStats[0]]
    standStats = [*standStats, standStats[0]]

    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(userStats))
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(polar=True)
    ax.set_yticklabels([])
    plt.ylim(0,6)

    plt.plot(label_loc, userStats, label='Your Stats', linestyle='dashed')
    plt.plot(label_loc, standStats, label= standName+' Stats', linestyle='dashed')

    PAD = 0.05
    ax.text(0.4, 1 + PAD, "E", size=16)
    ax.text(0.4, 2 + PAD, "D", size=16)
    ax.text(0.4, 3 + PAD, "C", size=16)
    ax.text(0.4, 4 + PAD, "B", size=16)
    ax.text(0.4, 5 + PAD, "A", size=16)
    
    plt.title(' ', size=20, y=1.05)
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
    plt.legend(loc='lower center')
    # plt.savefig('images/stats-'+time+'.png')

    # im = cv2.imread("images/stats-"+time+".png")
    # _, encoded_img = cv2.imencode('.PNG', im)
    # encoded_img = base64.b64encode(encoded_img)

    # os.remove("images/stats-"+time+".png")


    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

    return 200,{'buffer': my_base64_jpgData}
    
