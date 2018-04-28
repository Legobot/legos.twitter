from Legobot.Lego import Lego
import logging
import re
import requests
from bs4 import BeautifulSoup as bs

logger = logging.getLogger(__name__)


class TweetExpander(Lego):
    def listening_for(self, message):
        if message['text'] is not None:
            try:
                expr = re.compile(
                    'https://twitter.com/[a-zA-Z0-9]*/status/[0-9]*')
                match = re.search(expr, message['text'])
                if match is not None:
                    message['twitter_link'] = match.group()
                    return True
            except Exception as e:
                logger.error('''Twitter lego failed to check the message text: 
                            {}'''.format(e))
                return False

    def handle(self, message):
        opts = self.set_opts(message)
        self.reply(message, self._get_tweet(message['twitter_link']), opts)

    def _get_tweet(self, twitter_link):
        url = 'https://publish.twitter.com/oembed?url=' + twitter_link
        r = requests.get(url)
        s = bs(r.json()['html'], 'html.parser')
        s.get_text().replace('\n', '').replace("\'", "'")
        logger.debug('TWEET TEXT: {}'.format(s))
        return s.find('p').contents[0]

    def set_opts(self, message):
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
            return opts
        except IndexError:
            logger.error('''Cloud not identify message source in message: 
                        {}'''.format(message))

    def get_name(self):
        return 'twitter'

    def get_help(self):
        return 'On the roadmap.'
