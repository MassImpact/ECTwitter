import twitter

# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information
# on Twitter's OAuth implementation.
CONSUMER_KEY = 'KML0Icl2OfUoxsBcoEV9PyCFq'
CONSUMER_SECRET = '	hUf37hMGsqUF7Ov32OYPGLgiyaMp7e7BF5wWnW5gxbcxHiiHzu'
OAUTH_TOKEN = '50905649-6VIFU85mSCh9D4AQpuuYsYiZdpnKSGnjbwjSBdKkv'
OAUTH_TOKEN_SECRET = '	IHS2gG3l4jHnx9ymtteG3wAPlrFmRlna6k38BVs3f5CCu'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)
# Nothing to see by displaying twitter_api except that it's now a
# defined variable
print twitter_api