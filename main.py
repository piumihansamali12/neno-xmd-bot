import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CONFIGURATION ---
TOKEN = "8002779453:AAET2iWxRlqxioMrjvEZW1N4jBdw2VcHJPg"
CHANNEL_ID = -1002340798135 

# පින්තූර ගබඩා කරන තැන
IMG_DB = {
    "#piumi_hansamali": [],
    "#Yureni_Noshika": [],
    "#shanudrie_priyasad": [],
    "#sugar_lips": [],
    "#random": []
}

# Channel එකට අලුතින් පින්තූරයක් දැමූ විට එය Bot විසින් අල්ලා ගැනීම
async def track_channel_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.photo:
        caption = update.channel_post.caption or ""
        file_id = update.channel_post.photo[-1].file_id
        
        # Caption එකේ ඇති Hashtag එක අනුව පින්තූරය අදාළ Category එකට දානවා
        for tag in IMG_DB.keys():
            if tag.lower() in caption.lower():
                IMG_DB[tag].append(file_id)
                logging.info(f"Added new photo to {tag}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👑 Piumi Hansamali", callback_query_data='#piumi_hansamali'),
         InlineKeyboardButton("💃 Yureni Noshika", callback_query_data='#Yureni_Noshika')],
        [InlineKeyboardButton("🌟 Shanudrie", callback_query_data='#shanudrie_priyasad'),
         InlineKeyboardButton("🍭 Sugar Lips", callback_query_data='#sugar_lips')],
        [InlineKeyboardButton("🎲 Random Mix", callback_query_data='#random')],
        [InlineKeyboardButton("📊 Stats", callback_query_data='stats')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_msg = "👋 *SL Queen Bot* වෙත සාදරයෙන් පිළිගනිමු!\n\nපහත Buttons භාවිතා කර Model කෙනෙක් තෝරන්න."
    
    if update.message:
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "stats":
        stats_text = "📊 දැනට පද්ධතියේ ඇති පින්තූර ගණන:\n"
        for tag, photos in IMG_DB.items():
            stats_text += f"\n{tag}: {len(photos)}"
        await query.message.reply_text(stats_text)
        return

    if data == "main_menu":
        await start(update, context)
        return

    if data in IMG_DB:
        if not IMG_DB[data]:
            await query.message.reply_text(f"⚠️ {data} සඳහා තවම පින්තූර නැත. පසුව උත්සාහ කරන්න.", 
                                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_query_data="main_menu")]]))
        else:
            photo_to_send = random.choice(IMG_DB[data])
            keyboard = [
                [InlineKeyboardButton("➡️ Next", callback_query_data=data)],
                [InlineKeyboardButton("⬅️ Back to Menu", callback_query_data="main_menu")]
            ]
            await query.message.reply_photo(photo=photo_to_send, caption=f"✨ Model: {data}", reply_markup=InlineKeyboardMarkup(keyboard))
            try:
                await query.message.delete()
            except:
                pass

def main():
    # Application එක සාදා පණ ගැන්වීම
    app = Application.builder().token(TOKEN).build()
    
    # Handler එකතු කිරීම
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, track_channel_posts))
    
    print("Bot is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
