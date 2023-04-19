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
    Check4ResponseError(resp)

    # convert response to JSON and pull access_token value
    TOKEN = resp.json()['access_token']

    # add authorization to our headers dictionary
    headers['Authorization'] = f"bearer {TOKEN}"

    return headers

####################################################################################################
# This function returns the top <N> posts in the subreddit <SR>
####################################################################################################
def GetTopPosts(    headers, 
                    subRedditName, 
                    params = {}, 
                    numResponses = MAX_NUM_RESPONSES_TOTAL):

    urlString = API_BASE + 'r/'+subRedditName+'/top'

    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns the comments for a given post
#################################################################################################### 
def GetCommentsFromPost(    headers, 
                            subRedditName, 
                            postID,
                            params = {}, 
                            numResponses = MAX_NUM_RESPONSES_TOTAL):

    urlString = API_BASE + 'r/'+subRedditName+'/comments/'+postID

    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns all comments/replies from a given user
####################################################################################################
def GetUserComments(headers, 
                    userName, 
                    params = {}, 
                    numResponses = MAX_NUM_RESPONSES_TOTAL):
   
    urlString = API_BASE + 'user/'+userName+'/comments'
    
    return RequestGet(urlString=urlString,
                      header=headers,
                      params=params,
                      numResultsRequested=numResponses)

####################################################################################################
# This function returns replies to a comment 
####################################################################################################
def ExtractRepliesFromComment(comment):
        
    replies = {}
    
    if 'replies' in comment.keys():
        replies = comment['replies']
                
        for reply in replies['data']['children']:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ REPLY DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            DisplayDict(reply['data'], COMMENT_KEYS_OF_INTEREST)
            input()


    return replies

####################################################################################################
# This function does a keyword search of a subreddit
####################################################################################################
def GetSubredditKeywordSearch(headers, subreddit, keyword, numResponses):
    urlString = API_BASE + 'r/'+subreddit + '/search/'
    
    params={'q':keyword, 'restrict_sr': True}
    
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
        
        if not Check4ResponseError(resp):
            if len(resp.json()['data']['children']) > 0:
                responseList.append(resp)
                afterID = resp.json()['data']['children'][-1]['data']['name']
        
    return responseList

####################################################################################################
# Main Script
# This Python script is used to test Reddit API commands
####################################################################################################

subreddit = 'python'

credDict = GenerateCredentialsDict('nicksCreds.dat')

header = GetAuthentifiedHeader(credDict)

topPostsResponseList = GetTopPosts(headers=header,
                                   subRedditName=subreddit,
                                   numResponses=25)

for topPostsResponse in topPostsResponseList:
    for aPost in topPostsResponse.json()['data']['children']:
    
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ POST DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        DisplayDict(aPost['data'], POST_KEYS_OF_INTEREST)
        input()

    # Look at the comments for each post    
    # comments = GetCommentsFromPost(header, subreddit, postID)
        
    # for comment in comments.json():
    #     for reply in comment['data']['children']:
    #         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ COMMENT DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #         DisplayDict(reply['data'],COMMENT_KEYS_OF_INTEREST)   
    #         ExtractRepliesFromComment(reply['data'])
    #         input()
       
    # Look at other posts and comments by the user of the current top post
      
    # userComments = GetUserComments(header, aPost['data']['author'])       
    # Check4ResponseError(userComments)
    # for comment in userComments.json()['data']['children']:
    #     print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ USER COMMENT DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #     DisplayDict(comment['data'])
    #     input()

    
# keywordSearchResponseList = GetSubredditKeywordSearch(header, 'python', 'python', 500)

# counter = 0

# for keywordSearch in keywordSearchResponseList:

#     for result in keywordSearch.json()['data']['children']:
#         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ KEYWORD DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#         counter += 1
#         print(counter)
#         DisplayDict(result['data'],POST_KEYS_OF_INTEREST)
#         afterID = result['data']['name']

#     input()