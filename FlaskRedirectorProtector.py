
import flask
import requests
import argparse
import logging
from logging.handlers import RotatingFileHandler

app = flask.Flask(__name__)

method_requests_mapping = {
    'GET': requests.get,
    'HEAD': requests.head,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'PATCH': requests.patch,
    'OPTIONS': requests.options,
}


@app.route('/<path:path>', methods=method_requests_mapping.keys())
def proxy(path):
    url = teamserver + path
    requests_function = method_requests_mapping[flask.request.method]
    if headerkey in flask.request.headers.get(header):
        remote_addr = flask.request.remote_addr
        base_url = flask.request.base_url
        app.logger.warning("Secret Cookie Requested from:" + remote_addr + " to " + url )
        request = requests_function(url, stream=True, params=flask.request.args)
        response = flask.Response(flask.stream_with_context(request.iter_content()),
                          content_type=request.headers['content-type'],
                          status=request.status_code)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return redirect(redirect_url, code=302)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Protect your redirector/teamserver")
    parser.add_argument('--teamserver', help="Teamserver to forward to. Example: http://ip:port/", required=False)
    parser.add_argument('--port', help="Port to listen on", required=True)
    parser.add_argument('--header', help="Header to allow traffic. Example: 'X-Aspnet-Version'", required=True)
    parser.add_argument('--headerkey', help="Header key. Example: '1.5'", required=True)
    parser.add_argument('--redirect_url', help="Redirect URL.", required=True)
    args = parser.parse_args()
    port = int(args.port)
    redirect_url = args.redirect_url
    teamserver = args.teamserver
    headerkey = args.headerkey
    header = args.header
    handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.debug = False
    app.run(host="0.0.0.0",port=port)