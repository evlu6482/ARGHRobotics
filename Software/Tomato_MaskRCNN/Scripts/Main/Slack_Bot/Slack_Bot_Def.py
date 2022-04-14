
import os
import slack_sdk  
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Slack_Bot():

    def __init__(self):
        #init stuff
        
        slack_token = os.environ['SLACK_BOT_TOKEN']
        
        print(slack_token)
        
        self.client = WebClient(token=slack_token)
        self.channelID='bot-commands'
        # self.channelID='general'

    def push_message(self,message):
        response= self.client.chat_postMessage(
           channel=self.channelID,
           text=message

        )
        

        return


    def push_image(self,path_to_file):
        response = self.client.files_upload(  
            file=path_to_file,
            channels=self.channelID 
        )
        return