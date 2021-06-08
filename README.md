# chatops-slack
Create a chatbot on Slack to practice ChatOps for DevOps guy :D

## Build the image
docker build -t chatbot .

## Run docker (need Slack xoxb token)
docker run --name=chatbot -d --rm -e="SLACK_API_TOKEN=<put_you_chatbot_api_token_here>" chatbot
