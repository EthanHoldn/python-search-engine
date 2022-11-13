import re
import traceback
from urllib.request import urlopen
import os
import random
import numpy
import time
from textblob import TextBlob
wordsindex = []
def init():
    global english
    english = open("search-engine/english.txt").read().split("\n")

def get_txt(url):   #gets the text from the HTML of a web page
                    #also filters non english web pages
    output = ""
    with urlopen(url) as response:
        html = re.sub("(<!--.*?-->)", "", str(response.read()).replace("\\n", " ").replace("\\t", " ") , flags=re.DOTALL)
        title = html.split('title=\"')
        for x in range(len(title)-1):
            text = title[x+1].split("\"")[0]
            #print(text)
        #print("\n\n")
        head = html.split(">")
        for x in range(len(head)-1):
            text = head[x+1].split("<")[0]
            tag = head[x].split("<")[-1].split(" ")[0]
            #print(head[x])
            if len(text.strip()) > 1 and tag.count("/") == 0 and tag != "a" and tag != "script" and tag != "style":
                #print("-"+text+"-")
                line = re.sub("\W"," ", re.sub("\\\\\w\w\w"," ",text)).lower()
                output = output+line+"\n"
                #print("tag: " + tag)
            #if x > 100: exit()
    return output

def get_words(text):
    #blacklist = ['as', 'on', 'with', 'We', 'is', 'that','such', 'it', 'an', 'we', 'in', 'and', 'to', 'a', 'of', '', 'the']
    blacklist = ['']
    text = text.replace("\n", " ").split(" ")
    #text = text.replace("\n", " ").split(" ")
    words = []
    for word in text:
        if word not in blacklist:
            for indexword in words:
                if indexword[0] == word:
                    indexword[1] += 1
                    break
            else:
                words.append([word, 1])
    words.sort(key=lambda x: x[1])
    #print(words[-20:])
    print(len(words))
    return words

def count_words():
        #blacklist = ['as', 'on', 'with', 'We', 'is', 'that','such', 'it', 'an', 'we', 'in', 'and', 'to', 'a', 'of', '', 'the']
    links = os.listdir("search-engine/web/links")
    for i in links:
        for ii in open("search-engine/web/links/"+i).read().split("\n")[1:]:
            blacklist = ['']
            try:
                if is_english(ii) < .3:
                    print(ii)
                    break
                text = get_txt(ii)
            except:
                break
            
            text = text.replace("\n", " ").split(" ")
            #text = text.replace("\n", " ").split(" ")
            stime = time.time()
            for word in text:
                if word not in blacklist and len(word) >= 3:
                    for indexword in wordsindex:
                        if indexword[0] == word:
                            indexword[1] += 1
                            break
                    else:
                        wordsindex.append([word, 1])
            wordsindex.sort(key=lambda x: x[1])
            #print(time.time()-stime)
            #print(wordsindex[-20:])
            #print(len(wordsindex))

def is_english(url):
    words = get_txt(url).replace("\n", " ").split(" ")
    y = 0
    n = 0
    for word in words:
        if word != '':
            if word in english:
                y += 1
            else:
                n += 1

    return(y/(y+n))

init()
#is_english("https://www.gstatic.com/_/mss/boq-dots/_/ss/k=boq-dots.DotsSplashUi_desktop_ms.hnIDUFIWJCk.L.X.O/am=EF2YBXAACUQ/d=1/ed=1/rs=ALs0n2NSowzFifzGyfXAjVW0YPwNEyvxhQ/m=topstories,_b,_tp,_r")
#is_english("https://apple.com")
#print(get_txt("https://reddit.com"))
#is_english("https://raw.githubusercontent.com/khvorostin/useful-english-phrases/master/00-preface.txt")
#print(get_words(get_txt("https://apple.com")))
#print(get_txt("https://www.gstatic.com/_/mss/boq-dots/_/ss/k=boq-dots.DotsSplashUi_desktop_ms.hnIDUFIWJCk.L.X.O/am=EF2YBXAACUQ/d=1/ed=1/rs=ALs0n2NSowzFifzGyfXAjVW0YPwNEyvxhQ/m=topstories,_b,_tp,_r"))
#get_txt("https://www.gstatic.com/_/mss/boq-dots/_/ss/k=boq-dots.DotsSplashUi_desktop_ms.hnIDUFIWJCk.L.X.O/am=EF2YBXAACUQ/d=1/ed=1/rs=ALs0n2NSowzFifzGyfXAjVW0YPwNEyvxhQ/m=topstories,_b,_tp,_r")
count_words()