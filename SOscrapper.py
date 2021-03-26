
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re



URL = 'https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do'



page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='question')

#answers = results.find_all('div', class_='answers')

def urlFilter(url,page=1):
    base = re.search(r'^.*?\d+',url)
    return base.group(0)+'?page='+str(page)

def answer_data(url,soup):
    
    answerid = re.compile('answer-\d+')
    answerbody = 'js-post-body'
    postusers = 'user-info'
    userinfotext = 'user-details'
    vote_sec = 'js-vote-count'

    multipage = False
    length = 1
    try:
        pager_items = soup.find('div',{'class':'s-pagination'})
        length = len(pager_items.find_all('a'))
    except Exception as e:
        multipage = False
        print("Isn't a multipage prob.",e.args)
        
    for i in range(1,length+1):
        if i!=1:
            page = requests.get(urlFilter(url,i))
            soup = BeautifulSoup(page.content, 'html.parser')
            
        for answer in soup.find_all("div", {"id" : answerid}):
                ansbody = answer.find("div",{'class':answerbody})
                votes = answer.find('div',{'class':vote_sec})
                #print('Post Body::\n==========\n'+ansbody.get_text()+'\n-x-x-x-x-x-x-\n')
                user_sec = answer.find_all('div',{'class':postusers})[-1]
                ans_by = user_sec.find('div',{'class':userinfotext}).a
                print('Answer ID :',answer.attrs['data-answerid'])
                print('Answered by :',ans_by.get_text())
                print('Answerer ID :',answer.attrs['data-ownerid'])
                print('Votes :',votes.get_text())
            


def question_data(soup):

    questionid = 'question'
    quesbody = 'js-post-body'
    postusers = 'user-info'
    userinfotext = 'user-details'
    vote_sec = 'js-vote-count'
    
    question = soup.find('div',questionid)
    quesbody = question.find("div",{'class':quesbody})
    votes = question.find('div',{'class':vote_sec})
    #print('Post Body::\n==========\n'+ansbody.get_text()+'\n-x-x-x-x-x-x-\n')
    user_sec = question.find_all('div',{'class':postusers})[-1]
    ques_by = user_sec.find('div',{'class':userinfotext}).a
    print('Question ID :',question.attrs['data-questionid'])
    print('Asked by :',ques_by.get_text())
    print('Asker ID :',question.attrs['data-ownerid'])
    print('Votes :',votes.get_text())
            

URL = 'https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

question_data(soup)
answer_data(URL,soup)


'''
profile = FirefoxProfile("/home/galaxy/.mozilla/firefox/thmcw7ac.default-release")
driver = webdriver.Firefox(profile)


try:
    driver.get("https://google.com")
    
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get("https://stackoverflow.com")
    
except Exception as e:
    print(e.args)
'''
