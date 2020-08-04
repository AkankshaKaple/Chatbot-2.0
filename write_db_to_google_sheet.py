from datetime import timedelta, date
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId
import pygsheets
from config import Config


username = Config.Mongodb.username[0]
password = Config.Mongodb.password[0]
database_name = Config.Mongodb.database_name
port = 27017
server_address = Config.Mongodb.host[0]

uri = "mongodb://{}:{}@{}:{}/{}".format(username, password, server_address, port, database_name)
client = MongoClient(uri)

db = client.akanksha

# authorization
gc = pygsheets.authorize(service_file='client_secret.json')

sh = gc.open(Config.Google_Sheet.GOOGLE_SHEET_NAME)

# select the first sheet
wks = sh[0]


def get_data_from_db(db, given_date):
    question = []
    answer = []
    email_id = []
    date = []
    time = []
    name = []

    cursor = db.QuestionAnswer.find({'project_id': '5dc15779c346052fe774a8d1'})

    for i in cursor:
        if given_date in str(i['datetime']):
            if len(i['user_id']) > 0:
                user_info = list(db.UserInformation.find({"_id": ObjectId(i['user_id'])}))[0]

                question.append(i['question'])
                answer.append(i['answer'])
                email_id.append(user_info['email_id'])
                name.append(user_info['name'])
                date.append(str(i['datetime'].date())),
                time.append(str(i['datetime'].time()))

    df = pd.DataFrame(
        {'question': question, 'answer': answer, 'email_id': email_id, 'name': name, 'date': date, 'time': time})
    return df


def write_data_to_google_sheet(sh):
    yesterday = date.today() - timedelta(days=1)

    df = get_data_from_db(db, str(yesterday))

    if df.shape[0] != 0:
        wks.append_table(
            df.values.tolist(),
            start='A2',
            end=None,
            dimension='ROWS',
            overwrite=False,
        )
        print("Data saved to the google sheet")
    else:
        print("No data for this date")


write_data_to_google_sheet(sh)
