import sqlite3
import sys
import time
import random
import logging

sys.path.insert(0, '/home/nickshiell/Documents/Work/SocialMediaAPIInterface/SocialMediaAPIInterface/')

from Utils import *
from DataBaseUtils import SetJobStatus, SetOutputFilePath

####################################################################################################
#
####################################################################################################

def PerformCrawl(sqliteCursor,jobDict):
    
    listOfResponsesJSON = []

    time.sleep(random.randint(1,5))
    
    return listOfResponsesJSON

####################################################################################################
#
####################################################################################################
def CrawlerInterface(dataBaseFilename,
                    jobDict):
   
    logging.info('PERFORMING JOBS:',flush=True)
    logging.info(jobDict,flush=True)
   
    dataBaseConnection = sqlite3.connect(dataBaseFilename)
    dataBaseConnection.row_factory = sqlite3.Row 
    sqliteCursor = dataBaseConnection.cursor()

    # Set the job status to "IN PROG"
    SetJobStatus(dataBaseConnection, sqliteCursor, jobDict['id'], '\'INPROG\'')

    # make the reddit API call
    listOfResponsesJSON = PerformCrawl(sqliteCursor,jobDict)

    # save the output to a file
    filePath = SaveOutput(listOfResponsesJSON)
  
    # update the dataFilePath to "<filepath>" and the job status to "DONE" 
    SetOutputFilePath(dataBaseConnection, sqliteCursor, jobDict['id'],filePath)
    SetJobStatus(dataBaseConnection, sqliteCursor, jobDict['id'], '\'DONE\'')

    return  
              