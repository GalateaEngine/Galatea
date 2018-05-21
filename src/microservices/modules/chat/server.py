from sanic import Sanic, response, exceptions
from sanic_cors import CORS, cross_origin
from sanic_limiter import Limiter, get_remote_address
import argparse
import json
import logging
import os
import sys
import chatter
import badWordFiltering as badwords
'''
switch to mongodb based solution
'''
sys.path.append("..")
# Setup
app = Sanic()
CORS(app, automatic_options=True)
limiter = Limiter(app, key_func=get_remote_address)

logger = logging.getLogger()
config = {}
chatbots = None
# Utils


def debug(msg):
    if config['debug'] == True:
        logger.info(msg)


def get_request_userid(request):
    return request.ip


# Routes


@app.route("/", methods=['POST', ''])
@limiter.limit("15/minute", key_func=get_request_userid)
async def chat(request):
    try:
        if(request.json["statement"] and request.json['userid']):
            reply = chatbots[config["personas"].index(request.json["persona"])].reply(
                request.json["statement"])
            return response.json({"response": reply})
    except:
        debug(("Unexpected error:", sys.exc_info()[0]))
        raise exceptions.ServerError(
            "Bad Request missing json 'statement' or 'userid'", status_code=401)


@app.route("/train", methods=['POST'])
@limiter.limit("", key_func=get_request_userid)
async def chat(request):
    try:
        if(request.json["statement"] and request.json["response"] and request.json['userid']):
            persona = config["personas"].index(request.json["persona"])
            if(request.json["bad_response"] == ""):
                pass
            if (badwords.hasBadWords(request.json["statement"])==False):
                chatbots[persona].train(request.json["statement"],
                                        request.json["response"],
                                        request.json.get("bad_response", ""))
            nsfw=""
            if(badwords.hasBadWords(request.json["statement"]) or badwords.hasBadWords(request.json["response"])) :
                nsfw="nsfw"
            if(request.json["bad_response"] == False):
                with open(config.get("dataset_file", "./chat_dataset"+nsfw+".csv"), 'a') as f:
                    # Concatination is faster than join
                    csv = (request.json.get('statement')+";" +
                           request.json.get('response')+";" +
                           request.json.get('persona')+";" +
                           request.json.get('userid'))

                    f.write(csv+'\n')
            return response.json({"status": "ok"})
    except:
        debug(("Unexpected error:", sys.exc_info()[0]))
        raise exceptions.ServerError("Bad Request", status_code=401)


@app.route("/heartbeat", methods=['GET'])
@limiter.limit("")
async def classify(request):
    return response.json({"status": "alive"})

# Run statement


def run(new_config):
    global config
    global chatbots
    config.update(new_config)
    if(config['gzip_enabled'] == True):
        from sanic_compress import Compress
        Compress(app)

    chatbots = [chatter.Model(i, {}) for i in config["personas"]]
    app.run(
        host=config['host'], port=int(
            config['port']), workers=int(
            config['workers']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Demo Server')
    parser.add_argument('-C', '--config_file', metavar='path/to/config', type=str,
                        help='path to the config file')
    parser.add_argument('-P', '--port', metavar='XXXX', type=int, default="5000",
                        help='port of the server')
    parser.add_argument('-H', '--host', metavar='X.X.X.X', type=str, default="0.0.0.0",
                        help='''host of the server
                        (127.0.0.1 for localhost)
                        (0.0.0.0 for entire network)''')
    parser.add_argument('-W', '--workers', metavar='X', type=int, default="2",
                        help='workers of the server')
    parser.add_argument('-D', '--debug', metavar='true/false', type=bool, default="false",
                        help='debug logging')
    parser.add_argument('-gzip', '--gzip_enabled', metavar='true/false', type=bool, default="false",
                        help='output compression')
    parser.add_argument('--personas', metavar='strings',  nargs='+', default=["default"],
                        help='personas to initialize  Ex. (-p galatea sophia.portuguese tom_sawyer  )')

    args = parser.parse_args()
    config = {}
    if(args.config_file):
        config = json.load(
            open(
                os.path.join(
                    os.path.abspath(
                        os.path.dirname("__file__")), str(
                        args.config_file))))
    config.update(vars(args))
    run(config)
