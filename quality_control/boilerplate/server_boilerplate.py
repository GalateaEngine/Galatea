from sanic import Sanic, response, exceptions
from sanic_cors import CORS, cross_origin
from sanic_limiter import Limiter, get_remote_address
import argparse,json,logging,os,sys

# Setup
app = Sanic()
CORS(app)
limiter = Limiter(app,key_func=get_remote_address)

logger =logging.getLogger()   
config = {}

# Utils


def debug(msg):
    if config['debug'] == True:
        logger.info(msg)



# Routes


@app.route("/1", methods=['GET'])
@limiter.limit("")
async def test1(request):
    try:
        if(request.args["text"]):
            return response.text("Valid request")
    except:
        debug(( "Unexpected error:", sys.exc_info()[0]))
        raise exceptions.ServerError("Bad Request", status_code=401)

@app.route("/test2", methods=['POST'])
@limiter.limit("50/minute")
async def test2(request):
    try:
        if(request.args["text"]):
            return response.text("Valid request")
    except:
        debug(( "Unexpected error:", sys.exc_info()[0]))
        raise exceptions.ServerError("Bad Request", status_code=401)



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
