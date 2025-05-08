from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_state[chat_id] = 'esperando_nome'
    await context.bot.send_message(chat_id=chat_id, text="Olá! Qual é o seu nome?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    texto = update.message.text
    estado = user_state.get(chat_id)

    if estado == 'esperando_nome':
        user_state[chat_id] = 'esperando_opiniao'
        await context.bot.send_photo(chat_id=chat_id, photo='https://via.placeholder.com/300x200.png?text=Imagem+legal')
        await context.bot.send_audio(chat_id=chat_id, audio=InputFile("audio.mp3"))
        await context.bot.send_message(chat_id=chat_id, text=f"Legal, {texto}! O que achou da imagem e do áudio?")

    elif estado == 'esperando_opiniao':
        await context.bot.send_message(chat_id=chat_id, text="Valeu! Isso é tudo por agora 😊")
        user_state[chat_id] = 'fim'

async def main():
    import os
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
