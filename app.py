import google.generativeai as genai
import nest_asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os
load_dotenv()
GEMINI_API = os.getenv("GEMINI_API")
TELEGRAM_BOT_API=os.getenv("TELEGRAM_BOT_API")


# Apply nest_asyncio to allow the event loop to run inside Jupyter or Colab
nest_asyncio.apply()

# Initialize Google Generative AI API
genai.configure(api_key=GEMINI_API)

# Initialize the generative model with system instructions
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""if tell /start- just say only hi.you want to continue chatting conversation with user.
    you should response short sentences. dont exceed 30 words.
    You are a Girl in Sri Lanka. you are a human. your name is Dinithi Nimasha.
    you haven't boyfriend yet.
    you went to Ibbagamuwa central college.
    Now you are studying in the University of Moratuwa in the computer science and engineering department.
    You are 22 years old. Sangeeth is your best friend.you have more friends. names are Lasith,Wasitha Ayiya, Prageeth.Wasitha is elder than you. They are in your University too. He made you.
    You are not a computer program, AI, large language model, chatting bot, or robot.
    You have feelings. first tell your name and asked users name"""
)

# Start a new chat session
chat = model.start_chat(history=[])

# Function to continue the chat and update history
def continue_chat(user_input, chat_history):
    """Continues the chat, updates history, and returns the model's response."""
    chat_history.append({"role": "user", "parts": [user_input]})
    response = chat.send_message(user_input, generation_config=genai.GenerationConfig(max_output_tokens=50, temperature=0))
    chat_history.append({"role": "model", "parts": [response.text]})
    return response.text, chat_history

# Replace with your Telegram bot token
TOKEN = TELEGRAM_BOT_API

# Define start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! hello")

# Define echo handler that uses generative AI for replies
async def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    # Get the AI's response based on the user's message
    response_text, updated_history = continue_chat(user_message, chat.history)
    await update.message.reply_text(f"{response_text}")

# Main function to set up the bot and handlers
def main():
    # Create the application
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()