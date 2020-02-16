# FlaskRedirectorProtector
 Protect your servers with a secret header
 
 I previously blogged about hardening your azure domain front with a secret header.
 The same may be accomplished for standard redirectors as well.
 Reference: https://medium.com/@rvrsh3ll/hardening-your-azure-domain-front-7423b5ab4f64

 ## Examples:

 ### Allow traffic using a secret header

 python3 FlaskRedirectorProtector.py --port 80 --redirect_url https://www.google.com --teamserver "http://host:80/" --headerkey "1.5" --header "X-Aspnet-Version"

 curl -H "X-Aspnet-Version: 1.5" http://redirector/testing

 ### Allow traffic to a payload based on useragent
 python3 FlaskRedirectorProtector.py --port 8080 --serve_payloads --directory "files" --redirect_url https://www.google.com --useragent_whitelist "Chrome" --host "0.0.0.0"

### Disallow traffic to a payload based on useragent in blacklist.txt
python3 FlaskRedirectorProtector.py --port 8080 --serve_payloads --directory "files" --redirect_url https://www.google.com --useragent_blacklist - --host "0.0.0.0"

