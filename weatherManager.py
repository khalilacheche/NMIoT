
from threading import Thread
import time
#import time, uuid, urllib, urllib2
import hmac, hashlib
from base64 import b64encode
import json
class wtm (Thread):

    def __init__(self,win): #Intializing the request for the Yahoo Weather API
        ############### ALL COMMENTEND WAITING FOR API KEY ###############
        #Basic info
        """url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
        method = 'GET'
        app_id = 'your-app-id'
        consumer_key = 'your-consumer-key'
        consumer_secret = 'your-consumer-secret'
        concat = '&'
        query = {'location': 'lausanne,ch', 'format': 'json'}
        oauth = {
            'oauth_consumer_key': consumer_key,
            'oauth_nonce': uuid.uuid4().hex,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': str(int(time.time())),
            'oauth_version': '1.0'
        }
        #Prepare signature string (merge all params and SORT them)
        merged_params = query.copy()
        merged_params.update(oauth)
        sorted_params = [k + '=' + urllib.quote(merged_params[k], safe='') for k in sorted(merged_params.keys())]
        signature_base_str =  method + concat + urllib.quote(url, safe='') + concat + urllib.quote(concat.join(sorted_params), safe='')
        #Generate signature
        composite_key = urllib.quote(consumer_secret, safe='') + concat
        oauth_signature = b64encode(hmac.new(composite_key, signature_base_str, hashlib.sha1).digest())
        #Prepare Authorization header
        oauth['oauth_signature'] = oauth_signature
        auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k,v) for k,v in oauth.iteritems()])
        #Send request
        url = url + '?' + urllib.urlencode(query)
        request = urllib2.Request(url)
        request.add_header('Authorization', auth_header)
        request.add_header('X-Yahoo-App-Id', app_id)
        self.request=request"""
        Thread.__init__(self)
        self.win = win #keeping a reference to the window object so we can pass info to it
    def run(self):
        while True:
            #response = urllib2.urlopen(self.request).read().loads()
            with open('res.json','r') as file: #Reading from res.json as placeholder
                response=json.load(file)
            self.win.updateWeatherData(response["forecasts"])
            time.sleep(10) #Updating the weather every 10 seconds(for testing)
