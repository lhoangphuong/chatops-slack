import os
from slack import RTMClient
from slack import WebClient
from slack.errors import SlackApiError

def docker_ps_command():
    cmd = 'docker ps'
    print(f'Executing {cmd}')
    stream = os.popen(cmd)
    return stream.read()
    
class Conversation:
    def __init__(self, web_client, channel, user):
        self.web_client = web_client
        self.channel = channel
        self.user = user

    def msg(self, text):
        # self.web_client.chat_postEphemeral(
        #     channel= self.channel,
        #     user=self.user,
        #     text=text,
        #
        # )
        self.web_client.chat_postMessage(
            channel=self.channel,
            text=text,

        )

welcome = '''
Hi there <@{user}>. I'm your friendly neighbourhood DevOps bot.
Use _{me} docker ps to list all docker container
'''

commands = {
    'docker': docker_ps_command
}


@RTMClient.run_on(event="message")  # subscribe to 'message' events
def process_command(**payload):
    data = payload['data']
    web_client = payload['web_client']
    print(payload)
    # ignore service messages, like joining a channel
    is_service = 'subtype' in data and data['subtype'] is not None

    if not is_service and 'text' in data:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        text = data['text']  # get data from the event
        tokens = text.split()  # split it up by space characters
        me = tokens[0]  # user id of the cht bot
        # object to track the conversation state
        conv = Conversation(web_client, channel_id, user)
        if len(tokens) > 1:
            print(tokens)
            # first token is my userid, second will be the command e.g. logs
            command = tokens[1]
            print('received command ' + command)
            if command in commands:
                # get the actual command executor
                command_func = commands[command]
                try:
                    args = tokens[slice(2, len(tokens))]
                    # execute the command
                    result = command_func()
                    if result is not None:
                        # and return the value from the
                        # command back to the user
                        conv.msg(result)
                except Exception as e:
                    conv.msg(str(e))

            else:
                # show welcome message
                web_client.chat_postMessage(
                    conv.msg(welcome.format(user=user, me=me))
                )
        else:
            # show welcome message
            conv.msg(welcome.format(user=user, me=me))


def main():
    rtm_client = RTMClient(token=os.environ["SLACK_API_TOKEN"])
    rtm_client.start()


if __name__ == "__main__":
    main()
