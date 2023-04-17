import requests
from Utils import *

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
def GetTopPosts(   headers, 
                    subRedditName, 
                    numberOfPosts = 25):

    urlString = API_BASE + 'r/'+subRedditName+'/top'

    print('API Call: ', urlString)

    resp = requests.get(    urlString,
                            headers=headers,
                            params={'limit':str(numberOfPosts)})
    
    return resp

####################################################################################################
# This function returns the comments for a given post
#################################################################################################### 
def GetCommentsFromPost(    headers, 
                            subRedditName, 
                            postID):

    urlString = API_BASE + 'r/'+subRedditName+'/comments/'+postID

    print('API Call: ', urlString)

    resp = requests.get(    urlString,
                            headers=headers)
    
    return resp

####################################################################################################
# This function returns all comments/replies from a given user
####################################################################################################
def GetUserComments(headers, userName):
    urlString = API_BASE + 'user/'+userName+'/comments'
    
    print('API Call: ', urlString)

    resp = requests.get(    urlString,
                            headers=headers)
    
    return resp

####################################################################################################
# This function does a keyword search of a subreddit
####################################################################################################
def GetSubredditKeywordSearch(headers, subreddit, keyword):
    urlString = API_BASE + 'r/'+subreddit + '/search/'
    
    print('API Call: ', urlString)

    resp = requests.get(    urlString,
                            headers=headers,
                            params={'q':keyword, 'restrict_sr': True, 'limit' : 1000, })
    
    return resp

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
# Main Script
# This Python script is used to test Reddit API commands
####################################################################################################

subreddit = 'python'

credDict = GenerateCredentialsDict('nicksCreds.dat')

header = GetAuthentifiedHeader(credDict)

# topPostsResponse = GetTopPosts(header, subreddit, 25)

# Check4ResponseError(topPostsResponse)

# for aPost in topPostsResponse.json()['data']['children']:
   
#     authorID = ExtractID36(aPost['data']['author_fullname'])
#     postID = ExtractID36(aPost['data']['name'])    

#     ups = aPost['data']['ups']
#     downs = aPost['data']['downs']

    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ POST DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print('authorID: ', authorID)
    # print('postID: ', postID)
    # print('up votes: ', ups)
    # print('down votes: ', downs)
    # DisplayDict(aPost['data'], POST_KEYS_OF_INTEREST)

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

keywordSearch = GetSubredditKeywordSearch(header, 'python', 'learn')
Check4ResponseError(keywordSearch)

print(len( keywordSearch.json()['data']['children']))
input()

for result in keywordSearch.json()['data']['children']:
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ KEYWORD DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    DisplayDict(result['data'])
    input()
