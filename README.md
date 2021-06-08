# chatops-slack
Create a chatbot on Slack to practice ChatOps for DevOps guy :D

## Build the image
```sh
docker build -t chatbot .
```
## Run docker 
(Bot use token strings begin with xoxb-)
```sh
docker run -d --rm --name=chatbot \
-e="SLACK_API_TOKEN=<put_you_chatbot_api_token_here>" \
-v /var/run/docker.sock:/var/run/docker.sock \
chatbot
```
