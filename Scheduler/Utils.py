import os
import json
import uuid

WAIT_TIME = 10 # Amount of time to sleep before checking the data base for new jobs
BASE_DIR = '/home/nickshiell/Documents/Work/SocialMediaAPIInterface/SocialMediaAPIInterface/Scheduler'
DATA_BASE_FILE_NAME = 'DataBase.db'
DATA_BASE_FILE_PATH = os.path.join(BASE_DIR, DATA_BASE_FILE_NAME)

REDDIT_JOB = 'REDDIT'
CRAWL_JOB = 'CRAWL'
YOUTUBE_JOB = 'YOUTUBE'
TWITTER_JOB = 'TWITTER'

def DummyInterface():
    print('DummyInterface')
    
def SaveOutput(listOfResponsesJSON):
    
    filename = './OutputData/'+str(uuid.uuid4())+'.json'
    
    with open(filename, "w") as outfile:
        for json_object in listOfResponsesJSON:
            json.dump(json_object,outfile)
            
    return filename