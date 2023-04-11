CLIENT_ID = '_-W7ANd6UN4EXexvgHn8DA'
SECRET_TOKEN = 'kpBdT1f-nRHM_kxdBzmxoOnDo_96FA'
USERNAME = 'nickshiell'
PASSWORD = 'Q!w2e3r4'

# This Python script is used to test Reddit API commands

import requests

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, 
                                   SECRET_TOKEN)

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyAPI/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, 
                    data=data, 
                    headers=headers)


# Check if there was an error message returned
if 'error' in res.json().keys():  
    print('Error Code:', res.json()['error'])
    print('Error Msg:',res.json()['error_description'])
    input('Press ENTER to continue...')


# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers['Authorization'] = f"bearer {TOKEN}"

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)