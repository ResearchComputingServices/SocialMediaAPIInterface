import concurrent.futures
import time
import sqlite3
from .Utils import  *
from .ToolInterfaces.RedditAPIInterface import RedditToolInterface
from .ToolInterfaces.CrawlerInterface import CrawlerInterface
from .ToolInterfaces.YouTubeInterface import YouTubeInterface

##############################################################################################################
# CLASS DEFINITION: Job Scheduler
##############################################################################################################

class JobScheduler:

    #########################################################################
    # MEMBER(S)
    #########################################################################
    dataBaseConnection_ = None
    dataBaseFilePath_ = None
    
    keepRunning_ = True
    waitTime_ = 60 # the number of seconds to wait before checking for new jobs
     
    # This dictionary connects job type flags to the tool which handles them
    jobHandleDict ={REDDIT_JOB  : RedditToolInterface,
                    CRAWL_JOB   : CrawlerInterface,
                    TWITTER_JOB : DummyInterface,
                    YOUTUBE_JOB : YouTubeInterface}
        
    #########################################################################
    # CONSTRUCTOR
    #########################################################################
    
    def __init__(   self,
                    dataBaseFilename = '',
                    waitTime = 60):
        
        self.waitTime_ = waitTime
   
        self.keepRunning_ = True
        
        # ToDo: this code will be replaced when NodeJS backend is complete
        self.dataBaseFilePath_ = dataBaseFilename
        self.dataBaseConnection_ = sqlite3.connect(dataBaseFilename)
        self.dataBaseConnection_.row_factory = sqlite3.Row 
   
    #########################################################################
    # PRIVATE FUNCTIONS
    #########################################################################
   
    ############################################################################################
    # This function will take in a list of dictionarys which describe a job and creates seperate
    # threads to run them
    def submitJobs(self, 
                   listOfJobDicts):

        # Create a context manager to handle the opening/closing of processes
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for jobDict in listOfJobDicts:           
                
                # get the data from the job dictionary    
                jobType = jobDict['jobType']
            
                if jobType in self.jobHandleDict.keys():
                    # start a process that will execute the correct script
                    executor.submit(self.jobHandleDict[jobType],
                                    self.dataBaseFilePath_, # todo: REMOVE THIS WHEN WE USE THE NODEjs bACK END
                                    jobDict) 
                else:
                    print('[ERROR]: Unknown Job Type: ', jobType)
            
            # this allows the context manager to return before each process is finished
            # which means the scheduler is free to go back and check for other new jobs
            executor.shutdown(wait=False)

        return

    ############################################################################################
    # This function checks the data base for any rows in the JobsTable which has a job
    # status set to READY
    # ToDo: This function will need to be updated to use the NodeJS endpoints when they are ready
    def checkDataBaseForNewJobs(self):
        
        sqliteCursor = self.dataBaseConnection_.cursor()
        
        sql_table_query = '''SELECT * FROM JobsTable WHERE jobStatus = \'READY\' '''
        sqliteCursor.execute(sql_table_query)
        
        things = sqliteCursor.fetchall()
        
        sqliteCursor.close()
        
        listOfJobsDicts = [{k: item[k] for k in item.keys()} for item in things]
                      
        return listOfJobsDicts

    ############################################################################################
    # This function checks for any sort of exit conditions
    def checkExit(self):
        print('CheckExit')
        
        return True
     
    #########################################################################
    # PUBLIC FUNCTIONS
    #########################################################################
       
    ############################################################################################
    # This is the main loop for the job scheduler
    def Run(self):
                
        while self.keepRunning_:
            
            # This function will check the database for news and return a list of dictionaries with
            # the row ID of the new job
            listOfJobsDicts = self.checkDataBaseForNewJobs()

            if len(listOfJobsDicts) > 0:               
                # This function will submit the jobs to be run on seperate processes
                self.submitJobs(listOfJobsDicts)
                
            time.sleep(WAIT_TIME)
            
            # check if some type of exit condition has been set
            self.checkExit()


##############################################################################################################
if __name__ == '__main__':
    
    js = JobScheduler('testDataBase.db', 5)
    
    js.Run()
    
 
# Need to have API calls which can replace the functionality in checkDataBaseForNewJobs   
# 
# an API call which gets all the jobs? Or can we request all the jobs with certain IDs. Status', etc...
#
# def checkDataBaseForNewJobs(self):   
#   sqliteCursor = self.dataBaseConnection_.cursor()    
#   sql_table_query = '''SELECT * FROM JobsTable WHERE jobStatus = \'READY\' '''
#   sqliteCursor.execute(sql_table_query)
#
#   things = sqliteCursor.fetchall()
#
#   sqliteCursor.close()
#
#   listOfJobsDicts = [{k: item[k] for k in item.keys()} for item in things]
#   return listOfJobsDicts