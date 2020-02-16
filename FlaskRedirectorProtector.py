
from flask import Flask, render_template, redirect, make_response, jsonify, request, send_from_directory
import flask
import requests
import argparse
import os

app = Flask(__name__)

method_requests_mapping = {
    'GET': requests.get,
    'HEAD': requests.head,
    'POST': requests.post,
    'PUT': requests.put,
    'DELETE': requests.delete,
    'PATCH': requests.patch,
    'OPTIONS': requests.options,
}

@app.before_request
def log_request():
  # Logging
    ip = flask.request.remote_addr
    request = flask.request.base_url
    ua = flask.request.headers.get('User-Agent')
    with open("access.log", "a") as log:
        log.write("ip: " + ip + "," + " User-Agent: " + ua + "," + " Request: " + request)
        log.write('\n')


@app.route("/files/<path:filename>")
def fileserve(filename):
    ua = flask.request.headers.get('User-Agent')
    if useragent_whitelist is not None:
        if useragent_whitelist in ua:
          if os.path.isfile(directory + "/" + filename): 
            return send_from_directory(directory=directory, filename=filename)
          else:
            return redirect(redirect_url, code=302)
    elif useragent_blacklist is True:
        with open('blacklist.txt','r') as f:
            for x in f:
                x = x.rstrip()
                if ua == x:
                    return redirect(redirect_url, code=302)
                else:
                  if os.path.isfile(directory + "/" + filename): 
                    return send_from_directory(directory=directory, filename=filename)
                  else:
                    return redirect(redirect_url, code=302)
    else:
        return redirect(redirect_url, code=302)
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=method_requests_mapping.keys())
def teamserver(path):
    if header:
        if headerkey in flask.request.headers.get(header):
            url = teamserver + path
            requests_function = method_requests_mapping[flask.request.method]
            ip = flask.request.remote_addr
            request = flask.request.base_url
            ua = flask.request.headers.get('User-Agent')
            with open("access.log", "a") as log:
                log.write("Secret Cookie Requested from: " + ip)
                log.write('\n')
            request = requests_function(url, stream=True, params=flask.request.args)
            response = flask.Response(flask.stream_with_context(request.iter_content()),
                              content_type=request.headers['content-type'],
                              status=request.status_code)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return redirect(redirect_url, code=302)
    return redirect(redirect_url, code=302)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Protect your redirector/teamserver")
    parser.add_argument('--teamserver', help="Teamserver to forward to. Example: http://ip:port/", required=False)
    parser.add_argument('--host', help="Host to listen on.", default="0.0.0.0", required=True)
    parser.add_argument('--port', help="Port to listen on.", required=True)
    parser.add_argument('--header', help="Header to allow traffic. Example: 'X-Aspnet-Version'", required=False)
    parser.add_argument('--headerkey', help="Header key. Example: '1.5'", required=False)
    parser.add_argument('--redirect_url', help="Redirect URL.", required=True)
    parser.add_argument('--serve_payloads', action='store_true', help="Switch: Serve Payloads from files folder", required=False)
    parser.add_argument('--directory', help="Custom payload directory", default="files", required=False)
    parser.add_argument('--useragent_whitelist', help="Custom Useragent to allow.",required=False)
    parser.add_argument('--useragent_blacklist', action='store_true', help="Custom Useragent file to disallow.", required=False)
    args = parser.parse_args()
    port = int(args.port)
    useragent_whitelist = args.useragent_whitelist
    useragent_blacklist = args.useragent_blacklist
    serve_payloads = args.serve_payloads
    directory = args.directory
    redirect_url = args.redirect_url
    teamserver = args.teamserver
    headerkey = args.headerkey
    header = args.header
    host = args.host
    app.debug = False
    app.run(host=host,port=port)