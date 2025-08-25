#from MAILFETCHING import fetch
from models import textsummarization
from pymongo import MongoClient
from models import primarymodel
import pandas as pd
Client=MongoClient("mongodb+srv://umeshyenugula2007:K5vP3vmqxv8JwOjX@emails.yy5amep.mongodb.net/")
#fetch.get_unread_emails("harshith1")
db=Client['Emails']
emails=db['harshith1']
NoSpam=[]
for email in emails.find():
    subject=email.get('Subject')
    body=email.get('Body')
    setemails=pd.DataFrame([{"subject":subject,"body":body}])
    result=primarymodel.classify_emails(setemails)
    if result[0].get('prediction')=='Not Spam':
        NoSpam.append(result)
#print(NoSpam)
for email in NoSpam:
    textsummarization.summarize(email[0])
