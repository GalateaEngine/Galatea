from sanic import Sanic, response, exceptions
from sanic_cors import CORS, cross_origin
from sanic_limiter import Limiter, get_remote_address
from classifier import classify as classify_emotion
import argparse
import json
import logging
import os
import sys
# Setup

app = Sanic()
CORS(app, automatic_options=True)
limiter = Limiter(app, key_func=get_remote_address)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
config = {}

# Utils


def debug(msg):
    if config.get("debug","False") == True:
        logger.debug(msg)

# Routes


@app.route("/", methods=['GET'])
@limiter.limit("")
async def classify(request):
    try:
        if(request.args["text"]):
            return response.json({"classification": classify_emotion(request.args["text"])})
    except:
        debug(("Unexpected error:", sys.exc_info()[0]))
        raise exceptions.ServerError(
            "Bad Request,missing 'text' paramerter", status_code=401)


@app.route("/add", methods=['POST'])
async def add(request):
    try:
        if(request.json["text"] and request.json["emotions"] and config.get("add_dataset",True)):
            with open(config.get("dataset_file","./emotion_dataset.csv"), 'a') as f:
                # Concatination is faster than join
                csv = (request.json.get('text')+";" +
                       request.json["emotions"].get('anger', "0")+";" +
                       request.json["emotions"].get('boredom', "0")+";" +
                       request.json["emotions"].get('empty', "0")+";" +
                       request.json["emotions"].get('enthusiasm', "0")+";" +
                       request.json["emotions"].get('fear', "0")+";" +
                       request.json["emotions"].get('happiness', "0")+";" +
                       request.json["emotions"].get('hate', "0")+";" +
                       request.json["emotions"].get('love', "0")+";" +
                       request.json["emotions"].get('neutral', "0")+";" +
                       request.json["emotions"].get('anger', "0")+";" +
                       request.json["emotions"].get('relief', "0")+";" +
                       request.json["emotions"].get('sadness', "0")+";" +
                       request.json["emotions"].get('worry', "0"))

                f.write(csv+'\n')

            return response.text("ok")
    except:
        debug(("Unexpected error:", sys.exc_info()[0]))
        raise exceptions.ServerError(
            "Bad Request: 'text' or 'emotions' doesnt exist in json", status_code=401)


@app.route("/download_dataset", methods=['GET'])
@limiter.limit("")
async def serve(request):
    try:
        if (config["allow_download_dataset"]):
            return await response.file(config["dataset_file"])
        else:
            raise exceptions.ServerError("Option not enabled", status_code=401)

    except:
        debug(("Unexpected error:", sys.exc_info()[0]))
        raise exceptions.ServerError("Bad key", status_code=401)



@app.route("/heartbeat", methods=['GET'])
@limiter.limit("")
async def classify(request):
    return response.json({"status":"alive"})

# Run statement


def run(new_config):
    global config
    config.update(new_config)
    if(config['gzip_enabled'] == True):
        from sanic_compress import Compress
        Compress(app)

    app.run(
        host=config['host'], port=int(
            config['port']), workers=int(
            config['workers']), debug=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emotion Classification Microservice')
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
    parser.add_argument('-a', '--add_dataset', metavar='true/false', type=bool, default="false",
                        help='allow ingestion of new samples via /add')
    parser.add_argument('-dataset', '--dataset_file', metavar='path/to/file', type=str, default="./emotion_dataset.csv",
                        help='where to save the dataset file, only relevant if --add/-a is true')
    parser.add_argument('-download', '--allow_download_dataset', metavar='true/false', type=bool, default="false",
                        help='allow /download_dataset to serve the dataset (defined in --dataset)')
    
    args = parser.parse_args()
    config = {}
    if(args.config_file):
        config = json.load(
            open(str(args.config_file)))
    config.update(vars(args))
    run(config)
