"""Modmail Queue Cog entry point."""

from discord.ext import commands


class Queue(commands.Cog):
    """Main Cog for the Modmail Queue plugin."""

    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    """Register the Modmail Queue Cog with Modmail."""
    await bot.add_cog(Queue(bot))
