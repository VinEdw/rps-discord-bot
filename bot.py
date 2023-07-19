from __future__ import annotations
import logging
import discord
from discord.ext import commands
import rps
import keys

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")

class OpponentView(discord.ui.View):
    def __init__(self, *, user: discord.Member|discord.User, timeout: float = 180):
        super().__init__(timeout=timeout)
        self.user = user
        self.add_move_select()
        self.message: discord.message.Message
        self.user_move: str

    def add_move_select(self):
        select_options = [discord.SelectOption(label=label, emoji=icon) for label, icon in zip(rps.options, rps.option_icons)]
        move_select = discord.ui.Select(options=select_options, placeholder="Make your move")
        move_select.callback = self.move_select_callback
        self.move_select = move_select
        self.add_item(move_select)

    async def move_select_callback(self, interaction: discord.interactions.Interaction):
        self.user_move = self.move_select.values[0]
        await interaction.response.defer()
        await self.try_finish()
        logger.info(f"{self.user} selected {self.user_move}")

    def check_finished(self):
        return hasattr(self, "user_move")

    async def try_finish(self):
        if self.check_finished():
            await self.disable()
            self.stop()

    async def disable(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self):
        await self.disable()
        await self.message.reply("RPS game timed out")
        logger.info(f"{self.user} did not respond in time, so the game timed out")

    async def interaction_check(self, interaction: discord.interactions.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message(
                    f"Hey. You can't make a move for another user! Feel free to start your own game though.",
                    ephemeral=True)
            logger.info(f"{interaction.user} tried to interact with a view meant for {self.user}")
            return False
        return True

class ChallengerView(OpponentView):
    def __init__(self, *, user: discord.Member | discord.User, timeout: float = 180):
        super().__init__(user=user, timeout=timeout)
        self.add_opponent_select()
        self.opponent: discord.Member|discord.User

    def add_opponent_select(self):
        opponent_select = discord.ui.UserSelect(placeholder="Challenge an opponent")
        opponent_select.callback = self.opponent_select_callback
        self.opponent_select = opponent_select
        self.add_item(opponent_select)

    async def opponent_select_callback(self, interaction: discord.interactions.Interaction):
        self.opponent = self.opponent_select.values[0]
        await interaction.response.defer()
        await self.try_finish()
        logger.info(f"{self.user} challenged {self.opponent}")

    def check_finished(self):
        return super().check_finished() and hasattr(self, "opponent")


@bot.command(name="rps",
             help="Play extended rock paper scissors.")
async def play_rps(ctx: commands.context.Context):
    challenger = ctx.author
    logger.info(f"{challenger} started a game")
    challenger_name = challenger.display_name
    initial_msg = (f"Hi {challenger_name}! " \
            "So, you want to play some rock paper scissors? " \
            "Please choose your move and a user to challenge.")
    view_1 = ChallengerView(user=challenger)
    view_1.message = await ctx.reply(initial_msg, view=view_1)
    timed_out = await view_1.wait()
    if timed_out: return
    opponent = view_1.opponent
    opponent_name = opponent.display_name
    if opponent == bot.user:
        bot_move = rps.random_option()
        winner = rps.get_winner("I", bot_move, "You", view_1.user_move)
        winner_str = "It's a draw!" if winner is None else f"{winner} win!"
        bot_msg = (f"Wait, you want to play against me? " \
                "Okay.\n\n" \
                f"I choose {bot_move}.\n" \
                f"You chose {view_1.user_move}.\n\n" \
                f"{rps.comparison_string(bot_move, view_1.user_move)}\n\n" \
                f"{winner_str}")
        await view_1.message.reply(bot_msg)
    elif opponent == challenger:
        await view_1.message.reply("Umm...\n\nYou can't play against yourself. Silly goose.")
    else:
        followup_msg = (f"{opponent.mention}, " \
                f"you have been challenged to a duel by {challenger_name}. " \
                "Please choose your move.")
        view_2 = OpponentView(user=opponent, timeout=600)
        view_2.message = await view_1.message.reply(followup_msg, view=view_2)
        timed_out = await view_2.wait()
        if timed_out: return
        winner = rps.get_winner(challenger_name, view_1.user_move, opponent_name, view_2.user_move)
        winner_str = "It's a draw!" if winner is None else f"{winner} wins!"
        final_msg = (f"{challenger_name} chose {view_1.user_move}.\n" \
                f"{opponent_name} chose {view_2.user_move}.\n\n" \
                f"{rps.comparison_string(view_1.user_move, view_2.user_move)}\n\n" \
                f"{winner_str}")
        await view_2.message.reply(final_msg)
    logger.info(f"Game between {challenger} and {opponent} finished")

@bot.command(name="rps-diagram",
             help="Show a diagram of what beats what.")
async def send_diagram(ctx: commands.context.Context):
    diagram = discord.File("media/ultimate-rps.webp")
    await ctx.reply(file=diagram)

bot.run(keys.TOKEN, log_handler=None)
