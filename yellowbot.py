import json, urllib, urllib2, time
import hashlib, hmac

class YellowBot():

    def __init__(self, **args):

        assert args.get('api_key'),    "Missing api_key parameter"
        assert args.get('api_secret'), "Missing api_secret parameter"

        if not args.get("server"):
            args["server"] = 'www.yellowbot.com'

        self.api_base   = 'http://' + args['server'] + "/api/"
        self.api_key    = args['api_key']
        self.api_secret = args['api_secret']

        return None

    def call(self, method, **args):
        request = self._request(method, args)
        response = urllib2.urlopen(request)
        #print response.info()
        api_data = response.read()
        data = json.loads(api_data)
        return data

    def _request(self, method, args):
        args.update({
                'api_key': self.api_key,
                'api_ts' : str(int(time.time()))
                })
            
        args.update({
                'api_sig': self._signature(args)
                })

        r = urllib2.Request( url = self.api_base + method, data = urllib.urlencode(args) )
            
        return r
        
        
    def _signature(self, args):
            
        parameters = ""

        if args:
            for key in sorted(list(args.keys())):
                parameters += str(key) + str(args[key])
                    
        signature = hmac.new(self.api_secret, parameters, hashlib.sha256).hexdigest()
        return signature

