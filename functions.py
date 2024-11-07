from config import CHANNELS


async def check_subscribe(bot, user_id):
    for channel in CHANNELS:
        chat_member = await bot.get_chat_member(
            chat_id=channel, user_id=user_id
        )
        if chat_member.status not in ["member", "administrator", "creator"]:
            return False
    return True
