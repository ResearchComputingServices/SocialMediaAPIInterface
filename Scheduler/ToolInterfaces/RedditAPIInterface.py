import sqlite3
import logging
from SocialMediaAPIInterface.Scheduler.Utils import *

import sys
sys.path.insert(0, BASE_DIR)

from DataBaseUtils import GetRedditTableRow, GetCredentialsTableRow, SetJobStatus, SetOutputFilePath
from SocialMediaAPIInterface.Tools.RedditAPITool.RedditAPISession import RedditAPISession

####################################################################################################
#
####################################################################################################
def PerformRedditAPICall(sqliteCursor,jobDict):
    
    listOfResponsesJSON = []

    optionsDict = GetRedditTableRow(sqliteCursor,jobDict['redditJobID'])    
    credentialsDict = GetCredentialsTableRow(sqliteCursor,jobDict['credentialsID'])
    
    session = RedditAPISession(credentialsDict) 
    #listOfResponsesJSON = session.HandleJobDict(optionsDict) 
    STATUS, numQuota, msg = session.HandleJobDict(optionsDict) 
    session.End()
            
    return listOfResponsesJSON

####################################################################################################
#
####################################################################################################
def RedditToolInterface(dataBaseFilename,
                        jobDict):
   
    logging.info('PERFORMING JOBS:',flush=True)
    logging.info(jobDict,flush=True)
   
    # Set up connection to database
    dataBaseConnection = sqlite3.connect(dataBaseFilename)
    dataBaseConnection.row_factory = sqlite3.Row 
    sqliteCursor = dataBaseConnection.cursor()

    # Set the job status to "IN PROG"
    SetJobStatus(dataBaseConnection, sqliteCursor, jobDict['id'], '\'INPROG\'')

    # make the reddit API call
    listOfResponsesJSON = PerformRedditAPICall(sqliteCursor,jobDict)

    # save the output to a file
    filePath = SaveOutput(listOfResponsesJSON)
  
    # update the dataFilePath to "<filepath>" and the job status to "DONE" 
    SetOutputFilePath(dataBaseConnection, sqliteCursor, jobDict['id'], filePath)
    SetJobStatus(dataBaseConnection, sqliteCursor, jobDict['id'], '\'DONE\'')

    return  
              