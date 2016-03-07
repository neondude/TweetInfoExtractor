# Prerequisites

## Replace: 
>*    Access Token key and secret by the users Access Token key and secret
>*    Consumer key and secret by the app's consumer key and secret

####   In auth_and_Secret.py file where line as shown bellow.
    TweetOuth=Tweetoauth('Access Token key','Access Token Secret','consumer key', 'consumer secret')
### Instruction to Execute
>Make sure that you are not under any proxy server and also make sure that internet access is available.

# To execute loadhashDB.py

>## Usage:
>> in command propmt navigate to directory containing loadhashDB.py
>
        python loadhashDB.py <operation> <username>
>>### Operations:
>>* init: Create an initial username.db file
>>* fetch: Fill in mission hashtags for username.db
>>* display: Display all the hastags without duplicates in command prompt
>
>>### Username
>>Twitter user name

# To execute ShowTweetData.py

>## Usage:
>> in command prompt navigate to directory containing ShowTweetData.py
>
        python ShowTweetData.py <tweet_id>
>>### tweetId
>> tweet id of an individual tweet
