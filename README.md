# FlaskRedirectorProtector
 Protect your servers with a secret header
 
 I previously blogged about hardening your azure domain front with a secret header.
 The same may be accomplished for standard redirectors as well.
 Reference: https://medium.com/@rvrsh3ll/hardening-your-azure-domain-front-7423b5ab4f64

 Example:

 python3 flask_redirector.py --port 80 --redirect_url https://www.google.com --teamserver "http://host:80/" --headerkey "1.5" --header "X-Aspnet-Version"

 curl -H "X-Aspnet-Version: 1.5" http://redirector/testing