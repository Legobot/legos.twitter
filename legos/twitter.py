from Legobot.Lego import Lego
import logging
import re

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
                    logger.debug('LINK: {}'.format(message['twitter_link']))
                    return True
            except Exception as e:
                logger.error('''Twitter lego failed to check the message text: 
                            {}'''.format(e))
                return False

    def handle(self, message):
        opts = self.set_opts(message)

        self.reply(message, "That's a twitter.com link.", opts)

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
