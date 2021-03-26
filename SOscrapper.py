
import requests
from bs4 import BeautifulSoup
import re


class SOthread:

    def __init__(self,url):
        self.url = url
        page = requests.get(URL)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        
    @staticmethod
    def urlFilter(url,page=1):
        base = re.search(r'^.*?\d+',url)
        return base.group(0)+'?page='+str(page)

    def answer_data(self):
    
        url=self.url
        soup = self.soup
        
        answerid = re.compile('answer-\d+')
        answerbody = 'js-post-body'
        postusers = 'user-info'
        userinfotext = 'user-details'
        vote_sec = 'js-vote-count'

        posts = []

        multipage = False
        length = 1
        try:
            pager_items = soup.find('div',{'class':'s-pagination'})
            length = len(pager_items.find_all('a'))
        except Exception as e:
            multipage = False
            print("Isn't a multipage prob.",e.args)
        try:
            for i in range(1,length+1):
                if i!=1:
                    page = requests.get(self.urlFilter(url,i))
                    soup = BeautifulSoup(page.content, 'html.parser')

                for answer in soup.find_all("div", {"id" : answerid}):
                    post = {}
                    ansbody = answer.find("div",{'class':answerbody})
                    votes = answer.find('div',{'class':vote_sec})
                    post['body'] = ansbody.get_text()
                    user_sec = answer.find_all('div',{'class':postusers})[-1]
                    ans_by = user_sec.find('div',{'class':userinfotext}).a
                    post['post_id'] = answer.attrs['data-answerid']
                    post['op_name'] = ans_by.get_text()
                    post['op_id'] = answer.attrs['data-ownerid']
                    post['votes'] = votes.get_text()
                    posts.append(post)
        except Exception as e:
            print('In answer_data :',e.args)
        return posts



    def question_data(self):
        
        url = self.url
        soup = self.soup
        
        questionid = 'question'
        quesbody = 'js-post-body'
        postusers = 'user-info'
        userinfotext = 'user-details'
        vote_sec = 'js-vote-count'
        
        post = {}
        
        try:
            question = soup.find('div',questionid)
            quesbody = question.find("div",{'class':quesbody})
            votes = question.find('div',{'class':vote_sec})
            post['body'] = quesbody.get_text()
            user_sec = question.find_all('div',{'class':postusers})[-1]
            ques_by = user_sec.find('div',{'class':userinfotext}).a
            post['post_id'] = question.attrs['data-questionid']
            post['op_name'] = ques_by.get_text()
            post['op_id'] = question.attrs['data-ownerid']
            post['votes'] = votes.get_text()
        except Exception as e:
            print('In question_data :',e.args)
            
        return post

            
if __name__=='__main__':
    URL = 'https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do'

    sot = SOthread(URL)

    quest = sot.question_data()
    ans = sot.answer_data()
    print(len(ans))
    

