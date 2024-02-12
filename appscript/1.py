function sendSlackMessageWithBlocks() {
  var token = ''; // 실제 토큰으로 대체
  var channelId = ''; // 채널 ID
  var blocks = [
        {
          "type": "divider"
        },
        {
          "type": "actions",
          "elements": [
            {
              "type": "radio_buttons",
              "options": [
                {
                  "text": {
                    "type": "plain_text",
                    "text": "짜장",
                    "emoji": true
                  },
                  "value": "value-0"
                },
                {
                  "text": {
                    "type": "plain_text",
                    "text": "짬뽕",
                    "emoji": true
                  },
                  "value": "value-1"
                }
              ],
              "action_id": "actionId-0"
            }
          ]
        },
        {
          "type": "actions",
          "elements": [
            {
              "type": "button",
              "text": {
                "type": "plain_text",
                "text": "Click Me",
                "emoji": true
              },
              "value": "click_me_123",
              "action_id": "actionId-0"
            }
          ]
        }
      ]

  var url = "https://slack.com/api/chat.postMessage";
  var payload = {
    "channel": channelId,
    "blocks": JSON.stringify(blocks)
  };

  var options = {
    "method": "post",
    "contentType": "application/json",
    "headers": {
      "Authorization": "Bearer " + token
    },
    "payload": JSON.stringify(payload),
    "muteHttpExceptions": true
  };

  var response = UrlFetchApp.fetch(url, options);
  var jsonResponse = JSON.parse(response.getContentText());
  
  if (jsonResponse.ok) {
    Logger.log("Message with blocks sent successfully");
  } else {
    Logger.log("Failed to send message. Error: " + jsonResponse.error);
  }
}
