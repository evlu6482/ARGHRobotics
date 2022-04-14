

# init slack client with access token

# slack_token = os.environ['BOT_TOKEN']
slack_token="xoxb-2460326662768-3385353117349-JBiI9KzVzabTuoH1tL1cLGST"
client = WebClient(token=slack_token)
channelID='bot-commands'
# upload file
try:
    response= client.chat_postMessage(
        channel=channelID,
        text = "**********************************"
    )

    response = client.files_upload(    
        file='realsense.jpg',
        # initial_comment='This space ship needs some repairs I think...',
        channels=channelID
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")