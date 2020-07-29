from pymongo import MongoClient
import pandas as pd
from bson import ObjectId
import pygsheets
import pandas as pd


secretkey=12345
database='akanksha'
chatbotuser='akanksha'
chatbotpass='akanksha'
dbport=27017

username = chatbotuser
password = chatbotpass
database_name = database
port = 27017
server_address = "localhost"

uri = "mongodb://{}:{}@{}:{}/{}".format(username, password, server_address, port, database_name)
client = MongoClient(uri)
db = client.akanksha
db.list_collection_names()


date = "2020-04-17"
# today = datetime.date.today()
# yesterday = today - datetime.timedelta(days=1)

question = []
answer = []
email_id = []
datetime = []
name = []

cursor = db.QuestionAnswer.find({'project_id' : '5dc15779c346052fe774a8d1'})

for i in cursor:
    if date in str(i['datetime']):
        if len(i['user_id']) > 0:
            user_info = list(db.UserInformation.find({"_id" : ObjectId(i['user_id'])}))[0]
            
            question.append(i['question'])
            answer.append(i['answer'])
            email_id.append(user_info['email_id'])
            name.append(user_info['name'])
            datetime.append(i['datetime'])
            
df = pd.DataFrame({'question': question, 'answer': answer, 'email_id': email_id, 'name': name, 'date': datetime})

#authorization
gc = pygsheets.authorize(service_file='client_secret.json')


sh = gc.open('Chatbot')

#select the first sheet 
wks = sh[0]

wks.set_dataframe(df,(1,1))
print("Done")
