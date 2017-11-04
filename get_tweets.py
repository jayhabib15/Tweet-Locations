import requests
import re
import sys
from twython import TwythonStreamer
from twython import Twython

class MyStreamer(TwythonStreamer):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, query):
        TwythonStreamer.__init__(self, consumer_key, consumer_secret, access_token, access_token_secret)
        self.query=query

    def on_success(self, data):
        '''
        Acquires the tweet data if the query is present in the tweet
        '''
        if 'text' in data and 'coordinates' in data and data['coordinates']!=None:
            if self.query in data['text']:
                print(data['text'])
                self.writing_file(data['coordinates'])

    def writing_file(self,data):
        '''
        Writes tweet data to a file "coords."
        '''
        with open ('coords','a') as fout:
            print((data['coordinates']),file=fout)

    def on_error(self, status_code, data):
        '''
        If the provided coordinates fail, this returns an error
        '''
        print(status_code)

        # if you want to stop trying to get data because of the error?
        self.disconnect()



#Variables that contains the user credentials to access Twitter API


if __name__ == '__main__':
    access_token = "75616984-igpLwP7gNjoqIukwIuulEvvCHreVQ0zpcBFa3PfNq"
    access_token_secret = "iA2UXVQ6EIkonYOJn3fd1nrp7Du4pJRxdYvZ4ITMDdCYN"
    consumer_key = "VQ7MC2eUFNU9pDPWCbhl6pfDc"
    consumer_secret = "bv8sXsYC1AO9efWbFjN7MtpRMrcuREctd7Fm2OIvExyoFqgrUb"
    stream = MyStreamer(consumer_key, consumer_secret, access_token, access_token_secret, query=sys.argv[1])
    stream.statuses.filter(locations="-179,19,-67,71")
