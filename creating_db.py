import requests
from pprint import pprint
import sqlite3

gk_easy_response = requests.get('https://opentdb.com/api.php?amount=30&category=9&difficulty=easy&type=multiple')
gk_medium_response = requests.get('https://opentdb.com/api.php?amount=30&category=9&difficulty=medium&type=multiple')
gk_hard_response = requests.get('https://opentdb.com/api.php?amount=30&category=9&difficulty=hard&type=multiple')
history_easy_response = requests.get('https://opentdb.com/api.php?amount=30&category=23&difficulty=easy&type=multiple')
history_medium_response = requests.get('https://opentdb.com/api.php?amount=30&category=23&difficulty=medium&type=multiple')
history_hard_response = requests.get('https://opentdb.com/api.php?amount=30&category=23&difficulty=hard&type=multiple')
science_nature_easy_response = requests.get('https://opentdb.com/api.php?amount=30&category=17&difficulty=easy&type=multiple')
science_nature_medium_response = requests.get('https://opentdb.com/api.php?amount=30&category=17&difficulty=medium&type=multiple')
science_nature_hard_response = requests.get('https://opentdb.com/api.php?amount=30&category=17&difficulty=hard&type=multiple')

gk_easy = gk_easy_response.json()
gk_medium = gk_medium_response.json()
gk_hard = gk_hard_response.json()
history_easy = history_easy_response.json()
history_medium = history_medium_response.json()
history_hard = history_hard_response.json()
science_nature_easy = science_nature_easy_response.json()
science_nature_medium = science_nature_medium_response.json()
science_nature_hard = science_nature_hard_response.json()


conn = sqlite3.connect('question_answers_db.db')
c = conn.cursor()
def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS question_answers(id INT,question TEXT, answer TEXT,wrong_answers TEXT,difficulty INT,subject TEXT)")
def data_entry():
    k = 1
    for i in [gk_easy['results'],gk_medium['results'],gk_hard['results'],history_easy['results'],history_medium['results'],history_hard['results'],science_nature_easy['results'],science_nature_medium['results'],science_nature_hard['results']]:
        for j in range(len(i)):
            difficulty=None
            if i[j]['difficulty']=='easy':
                difficulty = 1
            elif i[j]['difficulty']=='medium':
                difficulty = 2
            else:
                difficulty = 3
            c.execute("INSERT INTO question_answers(id, question, answer, wrong_answers, difficulty, subject) VALUES (?,?, ?, ?, ?, ?)",(k,str(i[j]['question']) , str(i[j]['correct_answer']), str(i[j]['incorrect_answers']), difficulty,str(i[j]['category'])))
            k += 1
            conn.commit()
    c.close()
    conn.close()
create_table()
data_entry()