from Utils import *
from RedditAPIInterface import *

####################################################################################################
# Main Script
# This Python script is used to test Reddit API commands
####################################################################################################

subreddit = 'python'

credDict = GenerateCredentialsDict('nicksCreds.dat')

header = GetAuthentifiedHeader(credDict)

topPostsResponseList = GetSubredditPosts(headers=header,
                                         subRedditName=subreddit,
                                         category='hot',
                                         timeFrame='all',
                                         params={},
                                         numResponses=5)

for topPostsResponse in topPostsResponseList:
    
    for aPost in topPostsResponse.json()['data']['children']:
    
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ POST DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        DisplayDict(aPost['data'], POST_KEYS_OF_INTEREST)
        input()


# for topPostsResponse in topPostsResponseList:
    
#     for aPost in topPostsResponse.json()['data']['children']:
    
#         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ POST DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#         DisplayDict(aPost['data'], POST_KEYS_OF_INTEREST)
#         input()

#         print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ USER DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#         userSearchList = GetUserPosts(  headers=header,
#                                         userName=aPost['data']['author'])
        
#         for userSearch in userSearchList:
#             print(userSearch.json())
#             input()

#         # Look at the comments for each post    
#         postID = aPost['data']['id']
#         postCommentsList = GetCommentsFromPost(header, subreddit, postID)
#         for postComment in postCommentsList:
#             for commentThread in postComment.json():
#                 for comment in commentThread['data']['children']:
#                     print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ COMMENT DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#                     DisplayDict(comment['data'],COMMENT_KEYS_OF_INTEREST)   
#                     ExtractRepliesFromComment(comment['data'])
#                     input()
       
#         # Look at other posts and comments by the user of the current top post
#         userCommentsList = GetUserComments(header, aPost['data']['author'])       
        
#         for userComment in userCommentsList:
#             for comment in userComment.json()['data']['children']:
#                 print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ USER COMMENT DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
#                 DisplayDict(comment['data'],COMMENT_KEYS_OF_INTEREST)
#                 input()

    
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