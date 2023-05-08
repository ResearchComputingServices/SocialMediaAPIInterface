import requests
from Utils import *
import sys

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
                        subRedditName = 'all',
                        category = 'hot',
                        timeFrame = '', 
                        numResponses = MAX_NUM_RESPONSES_TOTAL):

   
    urlString = API_BASE + 'r/'+subRedditName+'/'+category
    
    params = {}
    params['t'] = timeFrame

    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function does a keyword search of a subreddit
####################################################################################################
def GetSubredditKeywordSearch(headers, 
                              subreddit, 
                              keyword, 
                              sortType,
                              numResponses):
    
    urlString = API_BASE + 'r/'+subreddit + '/search/'
    
    params = {}
    params['q'] = keyword
    params['restrict_sr'] = True
    params['sort'] = sortType
    
    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns the comments for a given post
#################################################################################################### 
def GetCommentsFromPost(    headers, 
                            subReddit, 
                            postID,
                            sortType,
                            numResponses = MAX_NUM_RESPONSES_TOTAL):

    urlString = API_BASE + 'r/'+subReddit+'/comments/'+postID

    params = {}
    params['sort'] = sortType

    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns all comments/replies from a given user
####################################################################################################
def GetUserComments(headers, 
                    userName, 
                    sortType,
                    timeFrame,
                    numResponses = MAX_NUM_RESPONSES_TOTAL):
   
    urlString = API_BASE + 'user/'+userName+'/comments'
    
    params = {}
    params['sort'] = sortType
    params['t'] = timeFrame
    
    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns all comments/replies from a given user
####################################################################################################
def GetUserPosts(   headers, 
                    userName, 
                    sortType,
                    timeFrame,
                    numResponses = MAX_NUM_RESPONSES_TOTAL):

    urlString = API_BASE + 'user/' + userName + '/submitted' 
    
    params = {}
    params['sort'] = sortType
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

def ExtractCommandLineArgs(cmdLineArgs):
    
    optionsDict = {}
    
    numCmdLineArgs = len(cmdLineArgs)
    
    for i in range(1,numCmdLineArgs):

        option = cmdLineArgs[i]

        if option[0] != '-':
            continue
        
        if option == '-cred':
            i = i + 1
            optionsDict['credFilename'] = cmdLineArgs[i]
            
        elif option == '-subreddit':
            i = i + 1
            optionsDict['subReddit'] = cmdLineArgs[i]
        
        elif option == '-user':
            i = i + 1
            optionsDict['user'] = cmdLineArgs[i] 
        
        elif option == '-posts':
            i = i + 1
            optionsDict['getPosts'] = '' 
        
        elif option == '-commments':
            i = i + 1
            optionsDict['getComments'] = '' 
           
        elif option == '-t':
            i = i + 1
            optionsDict['timeFrame'] = cmdLineArgs[i] 
        
        elif option == '-s':
            i = i + 1
            optionsDict['sortBy'] = cmdLineArgs[i] 
        
        elif option == '-l':
            i = i + 1
            optionsDict['limit'] = cmdLineArgs[i] 
        
        elif option == '--keyword':
            i = i + 1
            optionsDict['keyword'] = cmdLineArgs[i] 
        
        else:
            print('[WARNING]: HandleCommandLineArgs: Unknown command line option:',option)        
        
    return optionsDict   

####################################################################################################
def HandleOptionsdict(optionsDict):
    
    credDict = GenerateCredentialsDict(optionsDict['credFilename'])
    header = GetAuthentifiedHeader(credDict)

    subRedditName =''
    sortBy = ''
    timeFrame = ''
    numResponses = MAX_NUM_RESPONSES_TOTAL
    
    if 'subreddit' in optionsDict.keys():
        subRedditName=optionsDict['subreddit']


    if 'getPosts' in optionsDict.keys():
        postsResponseList = GetSubredditPosts(  headers=header,
                                                subRedditName=subRedditName,
                                                category=optionsDict['sortBy'],
                                                timeFrame=optionsDict['timeFrame'],
                                                numResponses=optionsDict['limits'])



####################################################################################################

if __name__ == '__main__':
    optionsDict = ExtractCommandLineArgs(sys.argv)    
    
    for option in optionsDict.keys():
        print(option,':',optionsDict[option])
        
    HandleOptionsdict(optionsDict)