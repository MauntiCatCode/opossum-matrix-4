from bot import Bot

from .characters import Characters
from .admin import Admin
from .movement import Movement

def setup(bot: Bot):
    bot.add_cog(Characters())
    bot.add_cog(Admin(bot.data_path))
    bot.add_cog(Movement())