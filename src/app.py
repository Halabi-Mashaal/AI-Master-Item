import os
import asyncio
import logging
from flask import Flask, request, Response
from teams_integration.teams_bot import MasterItemBot
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
from botbuilder.schema import Activity

app = Flask(__name__)

# Initialize bot and adapter
settings = BotFrameworkAdapterSettings(app_id="", app_password="")
adapter = BotFrameworkAdapter(settings)
bot = MasterItemBot()

logging.basicConfig(level=logging.DEBUG)

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

    logging.debug(f"Activity: {activity}")

    if 'service_url' in activity.additional_properties:
        activity.service_url = activity.additional_properties['service_url']

    async def turn_call(turn_context):
        await bot.on_message_activity(turn_context)

    async def messages_async():
        logging.debug("Starting process_activity")
        logging.debug(f"Service URL: {activity.service_url}")
        
        task = await adapter.process_activity(activity, auth_header, turn_call)
        
        logging.debug("Finished process_activity")
        return task

    try:
        asyncio.run(messages_async())
        return Response(status=201)
    except Exception as e:
        return Response(status=500, response=str(e))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
