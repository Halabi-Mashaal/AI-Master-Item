import os
from flask import Flask, request, Response
from teams_integration.teams_bot import MasterItemBot
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity

app = Flask(__name__)

# Initialize bot and adapter
settings = BotFrameworkAdapterSettings(app_id="", app_password="")
adapter = BotFrameworkAdapter(settings)
bot = MasterItemBot()

@app.route('/')
def home():
    return "Master Item AI Agent is running!"

@app.route("/api/messages", methods=["POST"])
def messages():
    """
    Endpoint for Microsoft Teams messages.
    """
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    async def turn_call(turn_context):
        await bot.on_message_activity(turn_context)

    try:
        task = adapter.process_activity(activity, auth_header, turn_call)
        task.result()
        return Response(status=201)
    except Exception as e:
        return Response(status=500, response=str(e))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
