import os
import requests
from slack import RTMClient
from slack import WebClient
from slack.errors import SlackApiError

class Conversation:
    def __init__(self, web_client, channel, user):
        self.web_client = web_client
        self.channel = channel
        self.user = user

    def msg(self, text):
        self.web_client.chat_postMessage(
            channel=self.channel,
            text=text,
        )

def docker_ps_command(args):
    cmd = 'docker ps'
    print(f'Executing {cmd}')
    stream = os.popen(cmd)
    return stream.read()

def docker_image_command(args):
    cmd = 'docker image ls'
    print(f'Executing {cmd}')
    stream = os.popen(cmd)
    return stream.read()

def joke_of_the_day_command(args):
    cmd = 'curl -H "Accept: text/plain" https://icanhazdadjoke.com/'
    print(f'Executing {cmd}')
    stream = os.popen(cmd)
    return stream.read()

def howdoi_command(args):
    cmd = f'howdoi {args}'
    print(f'Executing {cmd}')
    stream = os.popen(cmd)
    return stream.read()

welcome_message = '''
Hi there <@{user}>. I'm your friendly neighbourhood DevOps bot. How I can help you with?

List all docker container
`{me} docker ps`\n

List all docker image
`{me} docker image ls`\n

Tell a joke             
`{me} tell a joke`\n

Ask me anything                    
`{me} howdoi` <you_question> \n
'''

remind_message = '''
Are you kidding me <@{user}>?
Give a valid input, please!?
'''

commands = {
#    "docker ps": docker_ps_command,
#    "docker image ls": docker_image_command,
    "tell a joke": joke_of_the_day_command,
    "howdoi" : howdoi_command
}

@RTMClient.run_on(event="message")  # subscribe to 'message' events
def process_command(**payload):
    data = payload['data']
    web_client = payload['web_client']
    # ignore service messages, like joining a channel
    is_service = 'subtype' in data and data['subtype'] is not None
    if not is_service and 'text' in data:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        text = data['text']  # get data from the event
        tokens = text.split()  # split it up by space characters
        me = tokens[0]  # user id of the chat bot

        # object to track the conversation state
        conv = Conversation(web_client, channel_id, user)
        if len(tokens) > 1 and me =='<@U024827Q18S>': # user id of the chat bot. might need to change if you use other chatbot :D
            print(tokens)
            # first token is my userid, ther rest will be the command + arguments e.g. tell a joke
            request = ' '.join(tokens[1:len(tokens)+1])
            print('Received request: ' + request)
            if any(s in request for s in commands):
                pool = (s for s in commands if s in request)
                for s in pool:
                    # get the actual command executor
                    command_func = commands[s]
                    args = request.replace(s, '')
                    try:
                        # execute the command
                        result = command_func(args)
                        if result is not None:
                            # and return the value from the
                            # command back to the user
                            conv.msg(result)
                    except Exception as e:
                        conv.msg(str(e))
            else:
                # show remind message
                web_client.chat_postMessage(
                    conv.msg(remind_message.format(user=user, me=me))
                )
        elif len(tokens) == 1 and me =='<@U024827Q18S>':
            # show welcome message
            conv.msg(welcome_message.format(user=user, me=me))

def main():
    rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"])
    rtm_client.start()


if __name__ == "__main__":
    main()
