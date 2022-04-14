from Slack_Bot_Def import *
from datetime import datetime

Bot= Slack_Bot()
now = datetime.now()
date=datetime.today()

todaysdate=date.strftime("%d/%m/%Y")
current_time = now.strftime("%H:%M:%S")
timeprint=todaysdate+ "  :  " + current_time
Buffertext= "------------------------------------------------------------"

Bot.push_message(Buffertext)
Bot.push_message("Starting Sensing Session: "+ timeprint)