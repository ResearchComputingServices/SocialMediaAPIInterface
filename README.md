# SocialMediaAPIInterface

# Reddit API

## Subreddit Post Dict Keys of Interest
| Key      | Description |
| ----------- | ----------- |
| author_fullname | type + ID36 of the author ex. <type>_<ID36> T3_12j68f7|
| author | username of the posts autho |
| created_utc | unix epoch time of creation|
| created | unix epoch time of creation |
| downs | ??? |
| name | Type + ID36 of the post| 
| score | ??? |
| selftext | the text in the post |
| subreddit | name of the subreddit the post is under |
| title | title of the post |
| upvote_ratio | ??? |
| ups | number of up votes |
| view_count | Number of unique visits |
| id | ID36 of post|
| num_comments | The number of replies (including nested ie. replies to replies) |
| num_crossposts | Number of other subreddits where this is post is also posted|
  
## Comment Dict Keys of Interest
| Key      | Description |
| ----------- | ----------- |
| subreddit_id | ??? |
| subreddit | Name of the subreddit where the original post was made|
| replies | contains a data dict with all the replies to this comment|
| id | ??? |
| author | Username of the comments author|
| parent_id | type + ID36 of comment/post being replied too |
| score | comment score |
| author_fullname | type + author ID36|
| body | Text of the reply (raw text) |
| name | ??? |
| body_html | Text of reply with html tags |
| created | Unix epoch time or creation |
| link_id | type + ID36 of the original post |
| controversiality | ??? |
| depth | how many replies deep (ex. a reply to a reply has depth 1) |
| ups | number of upvotes |

