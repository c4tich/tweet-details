import re
import twitter
import pdb


webAccess=False;
numericID=False;
validInput=False;

if not webAccess:
	print('This program will provide a tweet\'s detail\n')
	print('You will have to provide either: \n')
	print('\t Its identifier (i.e. 18 char long number)\n')
	print('\t Its URL (with or without https://)')

	print('\nPlease input the tweet ID or URL: ')
	#tweetID=input()
	# tweetID='https://www.twitter.com/MeninistTweet/status/123456789012345678'
	tweetID='123456789012345678'
	
print('The inputted ID is ' + tweetID)

# input validation
if(tweetID.isnumeric() and len(tweetID)==18):
	numericID=True
	validInput=True
else:
	# define a regex to match an https:// started tweet
	pattern='(https\:\/\/)?(www\.)?twitter\.com\/[A-za-z0-9_]{1,15}\/status\/[0-9]{18}'
	match=re.match(pattern,tweetID)
	# print(match)
	if match: 
		numericID=False
		validInput=True
	else:
		validInput=False;

if not validInput:
	print("Your input couldn't be parsed as any known identifiers \n")
	print("Please try again")
else:
	if numericID:
		print("Your input was successfully parsed as numID: "+ tweetID)
	else:
		tweetID=tweetID[len(tweetID)-18:len(tweetID)]
		print("Your input was successfully parsed as URL. Its numID is: "+ tweetID)

# validation
# details is a list with the 4 keys required for the twitter API: consumer, consumer secret, access token and access token secret. They must be in a file called logon.details one per line
details=[]
with open('logon.details') as fp:
	for line in fp:
		details.append(line)

# rstrip removes the newline character appended with each append operation
try:
	apiDetails=twitter.Api(consumer_key=details[0],
							consumer_secret=details[1],
							access_token_key=details[2],
							access_token_secret=details[3])
	print(apiDetails.VerifyCredentials())
except twitter.error.TwitterError as err:
# check if the credentials allowed the app to successfully login
	print('There was a problem validating your credentials: ' + str(err.message))
else:
	print('Your credentials were successfully validated')
	
	




