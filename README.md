# rps-discord-bot

<a href="https://raw.githubusercontent.com/VinEdw/rps-discord-bot/master/media/rps-move-diagram.svg" target="_blank"><img src="media/rps-move-diagram.svg" alt="extended rock paper scissors diagram"></a>

This bot allows you to play an extended version of rock paper scissors on your discord server.
Use the command `!rps` to initialize a game.
Use the command `!rps-diagram` to see the move diagram.

The game is inspired by this [art post](https://www.umop.com/rps15.htm) by David C. Lovelace.
Each move choice beats up to halfway across the circle.
The move options are the following:

- rock
- fire
- scissors
- snake
- human
- tree
- wolf
- sponge
- paper
- air
- water
- dragon
- devil
- lightning
- gun

The code is written in [Python](https://www.python.org/), and uses the [discord.py](https://discordpy.readthedocs.io/en/stable/) API wrapper.

## Setup for Self Hosting

If you wish to host the bot yourself, you will need to create a new application in the [discord developer portal](https://discord.com/developers/applications).
From there, you can get a bot token.
Be careful not to share this token with anyone.
This token will need to be copied into a new text file called `keys.py` as follows.

```py
TOKEN = "yourGibberishTokenHere"
```

Since the bot uses [discord.py](https://discordpy.readthedocs.io/en/stable/), you will need to follow their [installation instructions](https://discordpy.readthedocs.io/en/stable/intro.html). 
I recommend using a [virtual environment](https://discordpy.readthedocs.io/en/stable/intro.html#virtual-environments).
I usually name my virtual environments `.venv`, but use whatever you would like.

If you are running the bot on a Linux computer, you can use the `rps_bot.service` file.
This will start the discord bot on device startup, and restart the bot in case an error occurs.
Some edits would need to be made to the file though.

- `WorkingDirectory=` needs to have the directory where this repository is saved
- `miste` on the `User=` line needs to be replaced with the name of the user running the bot script
- `.venv` on the `ExecStart=` line needs to replaced with the name of your Python virtual environment

Once those edits are made, the following can help to setup and control the service.

1. Copy the file to `/etc/systemd/system/`
2. Start the service with `sudo systemctl start rps_bot`
3. Check that it is working with `sudo systemctl status rps_bot`
4. Enable start at boot with `sudo systemctl enable rps_bot`
5. Stop the bot with `sudo systemctl stop rps_bot`
6. Disable start at boot with `sudo systemctl disable rps_bot`
