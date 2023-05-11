import sys

import argparse
import requests

from Utils import *

####################################################################################################
# Objects which are passed back as children in the response to a GET request contain objects.
# Each object has a unique name made up of a TYPE and an ID36 id. The TYPE is one of the following:
#
#   t1_	    Comment
#   t2_	    Account
#   t3_	    Link
#   t4_	    Message
#   t5_	    Subreddit
#   t6_	    Award

####################################################################################################
# This function returns a header with authorization TOKEN 
####################################################################################################
def GetAuthentifiedHeader(  credDict,
                            headerKey = 'User-Agent',
                            headerValue = 'MyAPI/0.0.1'):
    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth( credDict['CLIENT_ID'],
                                        credDict['SECRET_TOKEN'])
       
    # setup our header info, which gives reddit a brief description of our app
    headers = {headerKey: headerValue}

    # send our request for an OAuth token
    resp = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, 
                        data=credDict, 
                        headers=headers)
    
    # Check if there was an error message returned
    Check4ResponseError(resp, True)

    # convert response to JSON and pull access_token value
    TOKEN = resp.json()['access_token']

    # add authorization to our headers dictionary
    headers['Authorization'] = f"bearer {TOKEN}"

    return headers

####################################################################################################
# This function returns the top (numResponses) posts in the subreddit (subRedditName)
####################################################################################################
def GetSubredditPosts(  headers, 
                        subredditID = 'all',
                        sortBy = 'hot',
                        timeFrame = '', 
                        numResponses = MAX_NUM_RESPONSES_TOTAL):

   
    urlString = API_BASE + 'r/'+subredditID+'/'+category
    
    params = {}
    params['t'] = timeFrame

    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function does a keyword search of a subreddit
####################################################################################################
def GetSubredditKeywordSearch(  headers, 
                                subredditID, 
                                keyword, 
                                sortBy,
                                timeFrame,
                                numResponses):
    
    urlString = API_BASE + 'r/'+subredditID + '/search/'
    
    params = {}
    params['q'] = keyword
    params['restrict_sr'] = True
    params['sort'] = sortBy
    params['timeFrame'] = timeFrame
    
    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns the comments for a given post
#################################################################################################### 
def GetCommentsFromPost(    headers, 
                            subredditID, 
                            postID,
                            sortBy,
                            numResponses = MAX_NUM_RESPONSES_TOTAL):

    urlString = API_BASE + 'r/'+subredditID+'/comments/'+postID

    params = {}
    params['sort'] = sortBy

    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns all comments/replies from a given user
####################################################################################################
def GetUserComments(headers, 
                    userID, 
                    sortBy,
                    timeFrame,
                    numResponses = MAX_NUM_RESPONSES_TOTAL):
   
    urlString = API_BASE + 'user/'+userID+'/comments'
    
    params = {}
    params['sort'] = sortBy
    params['t'] = timeFrame
    
    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns all comments/replies from a given user
####################################################################################################
def GetUserPosts(   headers, 
                    userID, 
                    sortBy,
                    timeFrame,
                    numResponses = MAX_NUM_RESPONSES_TOTAL):

    urlString = API_BASE + 'user/' + userID + '/submitted' 
    
    params = {}
    params['sort'] = sortBy
    params['t'] = timeFrame
    
    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function performs a GET call from requests as defined by it's arguments
####################################################################################################
def RequestGet(urlString, header, params, numResultsRequested = 100):
        
    responseList = []
    
    print('API Call: ', urlString)
    
    if numResultsRequested > MAX_NUM_RESPONSES_TOTAL:
        numResultsRequested = MAX_NUM_RESPONSES_TOTAL
    
    # calculate floor division
    performNumRequests = numResultsRequested // MAX_NUM_RESPONSES_PER_REQUEST + 1
    
    afterID = ''   
    numResponsesRemaining = numResultsRequested
    for i in range(0, performNumRequests):
        
        params['after'] = afterID        
        params['limit'] = numResponsesRemaining
        numResponsesRemaining = numResponsesRemaining - MAX_NUM_RESPONSES_PER_REQUEST
        
        resp = requests.get(url=urlString,
                            headers = header,
                            params = params,
                            timeout=REQUEST_GET_TIMEOUT)

        responseList.append(resp)
        # if not Check4ResponseError(resp):
        #     if len(resp.json()['data']['children']) > 0:
        #         responseList.append(resp)
        #         afterID = resp.json()['data']['children'][-1]['data']['name']
        
    return responseList

####################################################################################################
# This block of code is the command line interface for working with the functions in this library
####################################################################################################

# Example run: python RedditAPIInterface.py -cred nicksCreds.dat -subreddit python -keyword IDE

def ExtractCommandLineArgs():
    
    parser = argparse.ArgumentParser(   prog='ProgramName',
                                        description='What the program does',
                                        epilog='Text at the bottom of help')

    # Positional Argument. Mandatory 
    parser.add_argument('credFilename', help = 'File containing reddit API creditentials.')

    # Optional Argument.

    # Return options
    parser.add_argument('--sortBy',default='top')
    parser.add_argument('--timeFrame',default='all')
    parser.add_argument('--limit', type=int,default=MAX_NUM_RESPONSES_TOTAL)

    # Items
    items = parser.add_mutually_exclusive_group(required=True)
    items.add_argument('--subreddit',default='python')
    items.add_argument('--user',default='')
    items.add_argument('--post',default='')

    # Actions
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--keyword',default='',help='Search the given SUBREDDIT for KEYWORD')
    actions.add_argument('--getPosts',type=int,default=0,choices=[0,1],help='Return posts from  SUBREDDIT or USER')
    actions.add_argument('--getComments',type=int,default=0,choices=[0,1],help='Return posts from  POST or USER')

    args = parser.parse_args()
       
    return vars(args)

####################################################################################################
#
####################################################################################################
def HandleOptionsDict(optionsDict):
     
    # All the get functions will return a JSON data structure containing the results
    responseJSON = None 
    
    # this code generates the authentication required to use the other API functions
    credDict = GenerateCredentialsDict(optionsDict['credFilename'])
    header = GetAuthentifiedHeader(credDict)

    print(credDict)
    print(header)
    input()

    # This block of code calls the actually API command set in the optionsDict
    if len(optionsDict['subreddit']) > 0:
        
        ######################################################################################
        # TODO: Put this into a function
        if optionsDict['getPosts']: 
            responseJSON = GetSubredditPosts(   headers=header,
                                                subredditID=optionsDict['subRedditID'],
                                                sortBy=optionsDict['sortBy'],
                                                timeFrame=optionsDict['timeFrame'],
                                                numResponses=optionsDict['limit'])
        elif len(optionsDict['keyword']) > 0:
            responseJSON = GetSubredditKeywordSearch(   headers=header,
                                                        subredditID=optionsDict['subRedditID'],
                                                        keyword=optionsDict['keyword'],
                                                        sortBy=optionsDict['sortBy'],
                                                        timeFrame=optionsDict['timeFrame'],
                                                        numResponses=optionsDict['limit'])
        else:
            print('[WARNING]: HandleOptionsdict: No ACTION specified for subreddit')  
        ######################################################################################
    elif 'userID' in optionsDict.keys():
        ######################################################################################
        # TODO: Put this into a function
        if 'getPosts' in optionsDict.keys():
            responseJSON = GetUserPosts(headers=header,
                                        userID=optionsDict['userID'],
                                        sortBy=optionsDict['sortBy'],
                                        timeFrame=optionsDict['timeFrame'],
                                        numResponses=optionsDict['limit'])
        
        elif 'getComments' in optionsDict.keys():
            responseJSON = GetUserComments( headers=header,
                                            userID=optionsDict['userID'],
                                            sortBy=optionsDict['sortBy'],
                                            timeFrame=optionsDict['timeFrame'],
                                            numResponses=optionsDict['limit'])
        else:
            print('[WARNING]: HandleOptionsdict: No ACTION specified for user')
        ######################################################################################
    elif 'postID' in optionsDict.keys():
        ######################################################################################
        # TODO: Put this into a function
        responseJSON = GetCommentsFromPost( headers=header,
                                            subRedditID=optionsDict['subRedditID'],
                                            postID=optionsDict['postID'],
                                            sortBy=optionsDict['sortBy'],
                                            numResponses=optionsDict['limit'])
        ######################################################################################
    else:
        print('[WARNING]: HandleOptionsdict: No ITEM ID specified.')  

    return responseJSON

####################################################################################################
# This is the command line interface
####################################################################################################
if __name__ == '__main__':
    
    # turn the list of command line args into a dictionary
    optionsDict = ExtractCommandLineArgs()    

    
    r = HandleOptionsDict(optionsDict)

####################################################################################################
# This is the function called by the scheduler to handle a job specified by the webApp
####################################################################################################
def RedditJobWebAppInterface(optionsDict):
    
    # Perform the Get Request speficied by the options dictionary
    responseJSON = HandleOptionsDict(optionsDict)
    
    # This function will be common to all the social media API tools (tasked to Jazmin)
    # GenerateOutputFile(responseJSON)    
    
    # This function will update the DB about the final status of the job, and the location of the results
    # (common to all tool)
    # UpdateDataBase()    
    
      