#!/bin/bash

# Running jenkins.war
(
    cd ~/Downloads
    java -jar jenkins.war &
)
#Giving time for jenkins to be fully connected
sleep 3

# running ngrok.exe
(
    cd /usr/bin/
    ngrok.exe http 8080 &
)
#Giving time for ngrok instance to fully connect
sleep 15
#Gets the url from ngrok instance
url="$(curl --silent --show-error http://127.0.0.1:4040/api/tunnels | sed -nE 's/.*public_url":"https:..([^"]*).*/\1/p')"
#Formats the url 
url="https://$url"
# Changes github webhook to reflect current url
info="$(cat Git_key)"
curl -L -X PATCH --insecure -H "Accept: application/vnd.github+json" -H "Authorization: Bearer $info" -H "X-Github-Api-Version: 2022-11-28" https://api.github.com/repos/Keith1039/Pygame-RPG/hooks/405886313/config -d '{"content_type":"json","url":''"'$url/github-webhook/'"}'
#Starts url in chrome
start chrome "$url" 