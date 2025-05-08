import os
import time
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

user_state = {}

# Função que simula "digitando..." antes de enviar a mensagem
async def typing_simulation(update, context, message):
    chat_id = update.effective_chat.id
    await context.bot.send_chat_action(chat_id, action="typing")  # Simula 'digitando...'
    time.sleep(1.5)  # Espera um tempo simulando a digitação
    await context.bot.send_message(chat_id=chat_id, text=message)

# Função que é chamada quando o usuário usa o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_state[chat_id] = 'etapa_1'
    await typing_simulation(update, context, "Oi gatinho! 😏")
    await typing_simulation(update, context, "Posso falar dos meus conteúdos e das chamadas? 😈🔥")

# Função que trata a mensagem do usuário e faz a transição entre etapas
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    texto = update.message.text
    estado = user_state.get(chat_id)

    if estado == 'etapa_1':
        # Etapa 1 - Aguardando qualquer resposta para ir para a Etapa 2
        user_state[chat_id] = 'etapa_2'
        await typing_simulation(update, context, "Imagem1")  # Envia imagem
        await typing_simulation(update, context, "No meu vip tem mais de 50 vídeos e fotos pra você aproveitar e atualizo todos os dias me mostrando todinha pra você")
        await context.bot.send_audio(chat_id=chat_id, audio=InputFile("audio1.mp3"))
        await typing_simulation(update, context, "Posso mandar uma amostra?")

    elif estado == 'etapa_2':
        # Etapa 2 - Aguardando qualquer resposta para ir para a Etapa 3
        user_state[chat_id] = 'etapa_3'
        await typing_simulation(update, context, "Imagem2")
        await context.bot.send_video(chat_id=chat_id, video=InputFile("video1.mp4"))
        await typing_simulation(update, context, "Se vc comprar agora, vai ganhar uma chamada de vídeo comigo, vou te chamar ❤️")
        await typing_simulation(update, context, "Copie a Chave Pix 'copia e cola' abaixo para realizar o pagamento 👇")

        # Aqui, você pode inserir o link de pagamento, dependendo da plataforma.
        # Exemplo:
        payment_link = "https://sualinkdepagamento.com"
        await typing_simulation(update, context, f"Aqui está o link para o pagamento: {payment_link}")

        # Espera 15 segundos (simulando o tempo de espera do cliente para pagar)
        time.sleep(15)
        await typing_simulation(update, context, "Link liberado! 😁")

        # Aqui seria a lógica de liberar o link de acesso após o pagamento (essa parte depende de integração externa)
        # Pode ser feito manualmente ou automaticamente com integração de plataformas de pagamento como Pushinpay.

    # Você pode adicionar mais etapas e mensagens conforme necessário.

# Função principal para rodar o bot
if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")  # Certifique-se de definir a variável de ambiente no Render
    app = ApplicationBuilder().token(token).build()

    # Adiciona os handlers para os comandos e mensagens
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Inicia o bot
    app.run_polling()
