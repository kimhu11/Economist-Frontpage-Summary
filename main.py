#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from gensim.summarization import summarize
import requests


# In[122]:


url = 'https://www.economist.com'


# In[138]:


r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")
links = soup.find_all('a', {'class': 'headline-link'})
l = []
for i in range(len(links)):
    if 'https://' in links[i].get('href'):
        l.append(links[i].get('href'))
    else:
        l.append(url+links[i].get('href'))


# In[140]:


text = ''
for i in range(len(l)):

    r = requests.get(l[i])
    soup = BeautifulSoup(r.text, "lxml")
    tags = soup.find_all('p', {'class': 'article__body-text'})
    article = ''
    for tag in tags:
        article += tag.get_text().strip()
    
    ratio = 0.01
    while len(summarize(article, ratio)) < 200:
        if len(summarize(article, ratio)) < 200:
            ratio += 0.01
            if ratio > 1:
                ratio = 1
                break
      
    
    text += soup.title.get_text() + '\n\n' + summarize(article, ratio) + '\n\n\n\n'



with open('today.txt', "w", encoding='utf8') as outfile:       
    outfile.write(text)

