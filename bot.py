import discord
import responses
import random
from dotenv import dotenv_values

QUOTES = []

# TODO: Make quote class and standardize output message with this class
# TODO: Make "Guess the author of the quote"-game
# TODO: Handle @person (maybe handled with quote class already?)
# TODO: Text to speech option for quotes


async def send_message(message, user_message, is_private=False):
    try:
        if user_message[:5] == 'quote':
            if len(user_message) > 5:
                keyphrase = user_message.split()[1].lower()
                await pomp_quote(message, keyphrase, is_private=is_private)
            else:
                await pomp_quote(message, is_private=is_private)
        else:
            response = responses.get_response(user_message)
            if response is not None:
                await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


async def pomp_quote(message, keyphrase=None, is_private=False):
    global QUOTES
    keyphrase_quotes = []

    if keyphrase is not None:
        for quote in QUOTES:
            if keyphrase in quote[0].lower():
                keyphrase_quotes.append(quote)

        if len(keyphrase_quotes) > 0:
            response, author = keyphrase_quotes[random.randint(
                0, len(keyphrase_quotes)-1)]

            await message.author.send(response) if is_private else await message.channel.send(response)
        else:
            await send_message(message, 'keyphrase is not in quotes', is_private=is_private)
    else:
        response, author = QUOTES[random.randint(0, len(QUOTES)-1)]

        await message.author.send(response) if is_private else await message.channel.send(response)


def is_quote(msg_content: str):
    if ("~" in msg_content or "-" in msg_content) and "\"" in msg_content:
        return True


def run_discord_bot():
    config = dotenv_values(".env")
    TOKEN = config["DISCORD_TOKEN"]
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        quotes_channel = client.get_channel(856255327094571028)
        async for msg in quotes_channel.history(limit=None):
            if is_quote(msg.content):
                QUOTES.append((msg.content, msg.author))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: "{user_message}" ({channel})')

        if channel == "quotes":
            if is_quote(message.content):
                QUOTES.append((message.content, message.author))

        if channel == "quote-bot-kanaal":
            is_private = False
            if user_message[0] == '?':
                is_private = True
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=is_private)

    client.run(TOKEN)
