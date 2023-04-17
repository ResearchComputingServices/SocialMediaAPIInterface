import os
from colorama import Fore, Back, Style

####################################################################################################
# GLOBAL CONSTANTS
####################################################################################################

BASE_DIR = '/home/nickshiell/Documents/Work/SocialMediaAPIInterface/SocialMediaAPIInterface'
CREDENTIALS_DIR = os.path.join(BASE_DIR, 'Creds')


API_BASE = 'https://oauth.reddit.com/'

POST_KEYS_OF_INTEREST = [   'subreddit',
                            'selftext',
                            'author_fullname',
                            'title','downs',
                            'name',
                            'upvote_ratio',
                            'ups',
                            'score',
                            'created',
                            'view_count',
                            'id',
                            'author',
                            'num_comments',
                            'created_utc',
                            'num_crossposts']

COMMENT_KEYS_OF_INTEREST = [    'subreddit_id',
                                'subreddit', 	
                                'replies',
                                'id',
                                'author', 	
                                'parent_id', 	
                                'score', 	
                                'author_fullname', 	
                                'body', 	
                                'name', 	
                                'body_html', 	
                                'created', 	
                                'link_id', 	
                                'controversiality', 	
                                'depth', 	
                                'ups'] 	


####################################################################################################
# UTILITY FUNCTIONS
####################################################################################################

####################################################################################################
# This function reads a users credentials from a file and loads them into a dictionary
# which can be passed to the Reddit server for authenification

def GenerateCredentialsDict(filename):
    
    credDict = {'grant_type': 'password'}
    
    filePath = os.path.join(CREDENTIALS_DIR, filename)
    
    file = open(filePath, 'r')
    
    lines = file.readlines()
            
    for line in lines:
        lineSplit = line.split(':')
        
        if len(lineSplit) == 2:
            credDict[lineSplit[0].strip()] = lineSplit[1].strip()
        
    return credDict

####################################################################################################
# This function checks a response for an error. If there is an error than the error code and any
# error text is displayed. If HALT is True than the script waits for the user to hit enter
def Check4ResponseError(resp, HALT = True):
    if 'error' in resp.json().keys():  
        print('Error Code:', resp.json()['error'])

        if 'error_description' in resp.json().keys():
            print('Error Msg:',resp.json()['error_description'])
        
        if HALT:    
            input('Press ENTER to continue...')

####################################################################################################
# This function removed the 'type' code at the front of a reddit ID36
def ExtractID36(str):
    
    id36 = None
    
    strSplit = str.split('_')
    
    if len(strSplit) == 2:
        id36 = strSplit[1]
    
    return id36

####################################################################################################
# This function prints the contents of a dictionary outwith colours
def DisplayDict(dict, keysOfInterest = None):
    
    for key in dict.keys():
        
        if keysOfInterest != None and key not in keysOfInterest:
            continue        
            
        value = dict[key]
       
        print(Fore.RED + key, Fore.WHITE+':',value)