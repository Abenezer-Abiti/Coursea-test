import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = "8663914505:AAF8pL-4OYn51SnB0z2dTwgES-WRYt92gvo"

symbols = ['🍎','🍌','🍇','🍉']
games = {}

def create_board():
    cards = symbols * 4
    random.shuffle(cards)
    return cards

def keyboard(board, show):
    buttons = []
    for i in range(0, len(board), 4):
        row = []
        for j in range(4):
            if i+j < len(board):
                text = board[i+j] if show[i+j] else "❓"
                row.append(InlineKeyboardButton(text, callback_data=str(i+j)))
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    board = create_board()

    games[user] = {
        "board": board,
        "show": [False]*len(board),
        "first": None
    }

    await update.message.reply_text(
        "🧠 Memory Game",
        reply_markup=keyboard(board, games[user]["show"])
    )

async def click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user.id
    game = games[user]
    i = int(query.data)

    if game["show"][i]:
        return

    game["show"][i] = True

    if game["first"] is None:
        game["first"] = i
    else:
        first = game["first"]
        if game["board"][first] != game["board"][i]:
            await query.edit_message_reply_markup(
                reply_markup=keyboard(game["board"], game["show"])
            )

            import asyncio
            await asyncio.sleep(1)

            game["show"][first] = False
            game["show"][i] = False

        game["first"] = None

    await query.edit_message_reply_markup(
        reply_markup=keyboard(game["board"], game["show"])
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(click))

print("Bot running...")
app.run_polling()