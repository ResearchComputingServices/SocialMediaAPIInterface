from youtube import *
from youtube.videos import Videos

# Example 1
yt = Youtube("Test_API_KEY")
yt.comments.get_comments_for_ids([12,34,22])

#Example 2
vid = Videos(yt)
vid.get_videos_by_id([12, 34, 32, "vidid02"])

print("wait")