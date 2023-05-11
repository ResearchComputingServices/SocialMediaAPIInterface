import argparse

MAXIMUM = 1000

parser = argparse.ArgumentParser(   prog='ProgramName',
                                    description='What the program does',
                                    epilog='Text at the bottom of help')

# Positional Argument. Mandatory 
parser.add_argument('credFilename', help = 'File containing reddit API creditentials.')

# Optional Argument.

# Return options
parser.add_argument('--sortBy',default='top')
parser.add_argument('--timeFrame',default='all')
parser.add_argument('--limit', type=int,default=MAXIMUM)

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
argparse_dict = vars(args)

#print(argparse_dict)
