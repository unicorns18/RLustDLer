import json
from interactions import Client
from helpers import logutils
import interactions
import os

logger = logutils.CustomLogger(__name__)

client = Client(
    token="MTI5ODM0Mzg2OTc3MTAyNjUxNA.GECUAM.HmJcCjf15d71PQJd5c6Ra3ZEYYkTK3Vz0F6EZA",
    intents=interactions.Intents.ALL,
    activity=interactions.Activity(
        name="Peekaboo", type=interactions.ActivityType.PLAYING
    ),
)

@client.listen()
async def on_ready():
    logger.info(f"We have logged in as {client.app.name}")
    logger.info(f"User ID: {client.app.id}")
    logger.info(f"Connected to {len(client.guilds)} guilds")
    logger.info(f"Connected to {client.guilds}")


if __name__ == '__main__':
    extensions = [
        f"extensions.{f[:-3]}"
        for f in os.listdir("extensions")
        if f.endswith(".py") and not f.startswith("_")
    ]
    for extension in extensions:
        try:
            client.load_extension(extension)
            logger.info(f"Loaded extension {extension}")
        except interactions.errors.ExtensionLoadException as e:
            logger.error(f"Failed to load extension {extension}.", exc_info=e)

    client.start()