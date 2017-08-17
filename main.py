import re
# pip install python-twitter
import twitter
from datetime import datetime


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
	# tweetID='https://twitter.com/agarzon/status/894307341952311296'
	# tweetID = 'https://twitter.com/JaviGlezLazaro/status/873528247132336129'
	tweetID = 'https://twitter.com/uribevidalali/status/890040309924724738'#emojis
	# tweetID = 'https://twitter.com/uribevidalali/status/898278209632034816'
	# tweetID='893922771843076096' #->este tweet da error tweetdeck
	# tweetID = 'https://twitter.com/c4tich/status/877471175881969664' # tweet con ubicación y sin coordenadas
	# un tweet con emojis da error
	# tweetID = '893922215682605056' # -> web client y da error

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
# details is a list with the 4 keys required for the twitter API: consumer, consumer secret, access token and access token secret. They must be in a file called logon.details, one per line
details=[]
with open('logon.details') as fp:
	for line in fp:
		details.append(line)

# rstrip removes the newline character appended with each append operation
try:
	apiDetails=twitter.Api(consumer_key=details[0].rstrip(),
							consumer_secret=details[1].rstrip(),
							access_token_key=details[2].rstrip(),
							access_token_secret=details[3].rstrip())
	#print(apiDetails.VerifyCredentials())
except twitter.error.TwitterError as err:
# check if the credentials allowed the app to successfully login
	print('There was a problem validating your credentials: ' + str(err.message))
else:
	print('Your credentials were successfully validated')

# validation of provided ID and get of tweet object
#try:
tweet=apiDetails.GetStatus(status_id=int(tweetID))
print('\n\n')
print('Content details:')
print('\tContent of the tweet: ')
print('\t\t<<'+str(tweet.text)+'>>')
if tweet.user.verified:
	cv=' (cuenta verificada)'
else:
	cv=''
print('\tAuthor:')
print('\t\t@'+tweet.user.screen_name+', '+tweet.user.name+cv)
d=datetime.strptime(tweet.created_at,'%a %b %d %H:%M:%S %z %Y')
print('Publication details:')
print('\tDate of publication: ' + str(d.day)+'/'+str(d.month)+'/'+str(d.year))
regex=re.compile('<a href=\\\"http[s]?://[a-zA-z\./\" rel=]*>([a-zA-Z ]*)</a>')
client=regex.match(tweet.source)
print('\tClient: '+client.group(1))
print('Location information:')
if(tweet.coordinates):
	print('\tLatitude: ' + str(tweet.coordinates['coordinates'][1]))
	print('\tLongitude: ' + str(tweet.coordinates['coordinates'][0]))
else:
	print('\tNo exact coordinates available')
if(tweet.place):
	print("\tPublished from: " + tweet.place['full_name'] + ' (' + tweet.place['country_code'] + ')' + ' ('+ tweet.place['place_type'] + ')')
else:
	print('\tNo approximate location data available')
# except Exception as exc:
# 	print('There was a problem with the provided identifier: ')# + str(exc.message))
