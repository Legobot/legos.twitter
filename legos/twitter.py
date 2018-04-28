from Legobot.Lego import Lego
import logging

logger = logging.getLogger(__name__)


class TweetExpander(Lego):
    def listening_for(self, message):
        if message['text'] is not None:
            try:
                return 'twitter.com' in message['text']
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
