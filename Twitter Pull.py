import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine
import json
import twitter
 
def oauth_login():
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://dev.twitter.com/docs/auth/oauth for more information
    # on Twitter's OAuth implementation.
 
    CONSUMER_KEY = 'KML0Icl2OfUoxsBcoEV9PyCFq'
    CONSUMER_SECRET = 'hUf37hMGsqUF7Ov32OYPGLgiyaMp7e7BF5wWnW5gxbcxHiiHzu'
    OAUTH_TOKEN = '50905649-6VIFU85mSCh9D4AQpuuYsYiZdpnKSGnjbwjSBdKkv'
    OAUTH_TOKEN_SECRET = 'IHS2gG3l4jHnx9ymtteG3wAPlrFmRlna6k38BVs3f5CCu'
 
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
 
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
 
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
 
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
 
        if wait_period > 3600: # Seconds
            print >> sys.stderr, 'Too many retries. Quitting.'
            raise e
 
        # See https://dev.twitter.com/docs/error-codes-responses for common codes
 
        if e.e.code == 401:
            print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
            return None
        elif e.e.code == 404:
            print >> sys.stderr, 'Encountered 404 Error (Not Found)'
            return None
        elif e.e.code == 429:
            print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
            if sleep_when_rate_limited:
                print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print >> sys.stderr, '...ZzZ...Awake now and trying again.'
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % \
                (e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e
 
    # End of nested helper function
 
    wait_period = 2
    error_count = 0
 
    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError, e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
        except BadStatusLine, e:
            error_count += 1
            print >> sys.stderr, "BadStatusLine encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise
 
# Sample usage
 
twitter_api = oauth_login()
 
# See https://dev.twitter.com/docs/api/1.1/get/users/lookup for
# twitter_api.users.lookup
 
response = make_twitter_request(twitter_api.users.lookup,
                                screen_name="ColeSF")
 
print json.dumps(response, indent=1)