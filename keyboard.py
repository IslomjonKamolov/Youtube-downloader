from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNELS, CHANNEL_URL

for url in CHANNEL_URL:
    channel_list = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ArGraV", url=url)],
            [InlineKeyboardButton(text="Tekshirish", callback_data="CHECK")],
        ],
    )

bot_watermark = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Youtubedan video yuklovchi bot.", url="https://t.me/Youtube_downloader_AGbot")],
    ],
)