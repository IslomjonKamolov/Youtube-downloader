import os
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandStart
from config import BOT_TOKEN
import yt_dlp as youtube_dl
from aiogram.types import CallbackQuery
import time
from functions import check_subscribe
from keyboard import channel_list, bot_watermark

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


@dp.message(CommandStart())
async def start(message: types.Message):
    is_sub = await check_subscribe(bot=bot, user_id=message.from_user.id)
    if not is_sub:
        await message.answer(
            "Botdan foydalanish uchun barcha kanallarga obuna bo'ling!!!",
            reply_markup=channel_list,
        )
        return
    await message.answer(
        "Assalomu aleykum men Youtubedan video yuklab beruvchi botman.\n<b>Mendan foydalanish uchun youtube video URLni yuboring!</b>",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "CHECK")
async def check_subscription(callback_query: CallbackQuery):
    check = await check_subscribe(user_id=callback_query.from_user.id, bot=bot)
    print(check)
    await callback_query.message.delete()
    if check:
        await callback_query.message.answer(
            "Assalomu aleykum men Youtubedan video yuklab beruvchi botman.\n<b>Mendan foydalanish uchun youtube video URLni yuboring!</b>",
            parse_mode="HTML",
        )
    else:
        await callback_query.message.answer(
            "Botdan foydalanish uchun barcha kanallarga obuna bo'ling!!!",
            reply_markup=channel_list,
        )
    await callback_query.answer()


@dp.message()
async def video_download(message: types.Message):
    is_sub = await check_subscribe(bot=bot, user_id=message.from_user.id)
    if not is_sub:
        await message.answer(
            "Botdan foydalanish uchun barcha kanallarga obuna bo'ling!!!",
            reply_markup=channel_list,
        )
        return
    url = message.text
    if not (url.startswith("http://") or url.startswith("https://")):
        await message.answer("Iltimos faqat <b>URL</b> yuboring!", parse_mode="HTML")
        return
    file_name = f"downloaded_video_{message.from_user.id}_{int(time.time())}.mp4"
    ydl_opts = {"format": "best", "outtmpl": file_name}
    sticker_message = await message.answer_sticker(
        "CAACAgIAAxkBAAEbu1tnLHXMZBEfiqblY5EaUcbb_mNRRQACIwADKA9qFCdRJeeMIKQGNgQ"
    )
    text_message = await message.answer("Yuklanmoqda... \n\nIltimos bir oz sabr qiling. Video yuklangach sizga yuboriladi.")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get("title", "Video")
            file_path = ydl.prepare_filename(info_dict)

        await message.answer_video(
            video=types.FSInputFile(file_path), caption=f"{video_title}\n\nYoutubedan videolarni sifati yuklab beruvchi bot: @python_testCode_bot",
            reply_markup = bot_watermark
        )
    except Exception as e:
        await sticker_message.delete()
        await text_message.delete()
        error_message = await message.answer_sticker('CAACAgIAAxkBAAEbu5ZnLIUN8UyvwqADnqptK-BiTLUT3QACDToAAgj_iEuF2_gYjopOAAE2BA')

        await message.answer(
            f"Xatolik yuz berdi: {str(e)}. Iltimos urlni tekshirib qayta harakat qilib ko'ring!"
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        await sticker_message.delete()
        await text_message.delete()


dp.include_router(router)

if __name__ == "__main__":
    dp.run_polling(bot)
