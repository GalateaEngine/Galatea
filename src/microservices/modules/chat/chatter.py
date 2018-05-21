import chatterbot
import logging
import trainer
import badWordFiltering as badwords
'''
TODO:
DICTIONARY FIXING
'''


class Model(object):

    config = {}

    chatbot = None
    logger = None

    def debug(self, msg):
        if self.config.get("debug", True) == True:
            self.logger.debug(msg)

    def train(self, question, answer, remove=False):
        if(type(question) == str and type(answer) == str):
            self.chatbot.train([question.lower(), answer.lower()], remove)
            return True
        else:
            return None

    def reply(self, question, id=0):
        return str(self.chatbot.get_response(question, id))

    def __init__(self, name, config, personality="normal"):
        self.config = config

        #logging.basicConfig(level=logging.DEBUG)
        #self.logger = logging.getLogger(__name__)
        self.chatbot = chatterbot.ChatBot(name,
                                          filters=[
                                              "chatterbot.filters.RepetitiveResponseFilter"],
                                          logic_adapters=[
                                              {
                                                  "import_path": "chatterbot.logic.BestMatch",
                                                  "statemlanguageent_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                                                  "response_selection_method": "chatterbot.response_selection.get_first_response"
                                              },
                                              {
                                                  'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                                                  'threshold': 0.65,
                                                  'default_response': '...'
                                              }
                                          ],

                                          #storage_adapter="chatterbot.storage.MongoDatabaseAdapter",

                                          database='database_'+name
                                          )
        self.chatbot.set_trainer(trainer.SingleShotTrainer)
