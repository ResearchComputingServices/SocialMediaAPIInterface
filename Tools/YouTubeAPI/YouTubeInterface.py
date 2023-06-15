import sqlite3
from SocialMediaAPIInterface.Tools.YouTubeAPI.youtube.youtube import *
import traceback
from SocialMediaAPIInterface.Tools.YouTubeAPI.youtube.utils import log_format
from SocialMediaAPIInterface.Tools.YouTubeAPI.youtube.setup_logger import logger
import SocialMediaAPIInterface.Tools.YouTubeAPI.youtube.config as config


####################################################################################################
#
####################################################################################################
def handle_state(yt):
    logger.debug("TO DO: Handle state")

    #Record in the database using API calls
    #If the job is completed set up the date as completed
    #Path of file
    #If the job is not completed due to out of quota set up as waiting
    #If the job is not completed due to an error set it up as  failed



####################################################################################################
#
####################################################################################################
def handle_new_job(jobDict, api_token, quota):

    response_list = []

    try:
        yt = Youtube(api_token, quota)
        if not yt.service:
            logger.error("The YouTube service was not created. Verify if the API key is valid or if the quota usage has been exceeded")
            print(yt.state.error_description)
            handle_state(yt)
            return response_list

        option = jobDict["option"]
        actions = jobDict["actions"]
        input = jobDict["input"]

        if option == "video":
            for action in actions:
                if action == "metadata":
                    response_list.append(yt.get_video_metadata_for_url(input))
                else:
                    response_list.append(yt.get_video_comments_for_url(input))

                # An error occurred while doing the above action or the quota exceeded we cannot continue executing actions
                if yt.state.error or yt.state.quota_exceeded:
                    break

        if option == "playlist":
            for action in actions:
                if action == "metadata":
                    response_list.append(yt.get_videos_metadata_from_playlist(input))
                else:
                    response_list.append(yt.get_videos_comments_from_playlist(input))

                # An error occurred while doing the above action or the quota exceeded we cannot continue executing actions
                if yt.state.error or yt.state.quota_exceeded:
                    break


        if option == "file":
            for action in actions:
                if action == "metadata":
                    response_list.append(yt.get_videos_metadata_from_file(input))
                else:
                    response_list.append(yt.get_videos_comments_from_file(input))

                # An error occurred while doing the above action or the quota exceeded we cannot continue executing actions
                if yt.state.error or yt.state.quota_exceeded:
                    break


        if option == "query":
            for action in actions:
                videos = jobDict["videos"]
                if action == "metadata":
                    response_list.append(yt.get_videos_metadata_from_query(input, videos))
                else:
                    response_list.append(yt.get_videos_comments_from_query(input, videos))

                # An error occurred while doing the above action or the quota exceeded we cannot continue executing actions
                if yt.state.error or yt.state.quota_exceeded:
                    break

    except:
        ex = traceback.format_exc()
        st = log_format("handle_new_job", ex)
        logger.error(st)
        yt.state.set_error_description(True, st)

    handle_state(yt)

    return response_list




####################################################################################################
#
####################################################################################################
def resume_job(jobDict, api_token, quota):

    response_list = []

    try:
        yt = Youtube(api_token, quota)
        if not yt.service:
            logger.error("The YouTube service was not created. Verify if the API key is valid or if the quota usage has been exceeded")
            print(yt.state.error_description)
            handle_state(yt)
            return response_list

        state = jobDict["state"]
        yt.state.from_dict_to_state(state)

        #Clean state error and quota from previous execution
        yt.state.error = False
        yt.state.error_description = ""
        yt.state.quota_exceeded = False

        #Resume retrieving videos
        if len(yt.state.actions)>0 and (config.ACTION_RETRIEVE_VIDEOS in yt.state.actions):
            videos_ids = yt.state.videos_ids
            if videos_ids:
                # Get data from YouTube API
                response_list.append(yt.videos.get_videos_and_videocreators(videos_ids))

        # Resume retrieving comments
        if len(yt.state.actions) > 0 and (config.ACTION_RETRIEVE_COMMENTS in yt.state.actions):
            videos_ids = yt.state.videos_ids
            if videos_ids:
                # Get data from YouTube API
                response_list.append(yt.comments.get_comments_and_commenters(videos_ids))

    except:
        ex = traceback.format_exc()
        st = log_format("handle_new_job", ex)
        logger.error(st)
        yt.state.set_error_description(True, st)

    handle_state(yt)

    return response_list


####################################################################################################
#
####################################################################################################
def PerformYouTubeAPICall(sqliteCursor, jobDict):
    listOfResponsesJSON = []

    #jobDict = GetYouTubeTableRow(sqliteCursor, jobDict['youtubeJobID'])
    #credentialsDict = GetCredentialsTableRow(sqliteCursor, jobDict['credentialsID'])

    jobDict = ""
    api_token = ""
    quota = 0

    if jobDict["status"] == "NewJob":
        listOfResponsesJSON = handle_new_job(jobDict, api_token, quota)
    else:
        listOfResponsesJSON = resume_job(jobDict, api_token, quota)


    return listOfResponsesJSON


####################################################################################################
#
####################################################################################################
def YouTubeInterface(dataBaseFilename, jobDict):

    logger.info('Performing YouTube job:', flush=True)
    logger.info(jobDict, flush=True)

    # Set up connection to database
    #dataBaseConnection = sqlite3.connect(dataBaseFilename)
    #dataBaseConnection.row_factory = sqlite3.Row
    #sqliteCursor = dataBaseConnection.cursor()

    # Set the job status to "IN PROG"
    #SetJobStatus(dataBaseConnection, sqliteCursor, jobDict['id'], '\'INPROG\'')

    # make the reddit API call
    sqliteCursor = None
    listOfResponsesJSON = PerformYouTubeAPICall(sqliteCursor, jobDict)



    # save the output to a file
    #filePath = SaveOutput(listOfResponsesJSON)

    # update the dataFilePath to "<filepath>" and the job status to "DONE"
    #SetOutputFilePath(dataBaseConnection, sqliteCursor, jobDict['id'], filePath)
    #SetJobStatus(dataBaseConnection, sqliteCursor, jobDict['id'], '\'DONE\'')

    return
