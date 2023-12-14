import os
import discord
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the Discord client
client = discord.Client()

# Get the bot's token from environment variables
token = str(os.getenv('TOKEN'))

# Event handler for when the bot is ready
@client.event
async def on_ready():
    try:
        print("Logged in as a bot {0.user}".format(client))
    except Exception as error:
        pass

# Event handler for when a message is received
@client.event
async def on_message(message):
    # Extract user information, channel, and user message
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    # Print user activity to console
    print(f'{username}: {user_message} in channel: #{channel}')

    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message is in the "random" channel
    if channel == "random":
        if user_message.lower() == 'hello world':
            # Respond with 'hello' if the message is 'hello world'
            await message.channel.send('hello')
        elif user_message.lower() == ("tell me about your server"):
            # Provide EC2 server data if the message is 'tell me about your server'
            await message.channel.send(f"""your ec2 server data:\n
region:{ec2_metadata.region}\n
public ipv4 address:{ec2_metadata.public_ipv4}\n
availability zone:{ec2_metadata.availability_zone}\n
server instance:{ec2_metadata.instance_type}
""")
        else:
            # Respond with an error message for unrecognized commands
            await message.channel.send(f"I'm sorry, the command '{user_message}' is not a valid command")

# Run the bot with the provided token
client.run(token)
