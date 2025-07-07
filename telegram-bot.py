import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Enable logging

logging.basicConfig(
format=’%(asctime)s - %(name)s - %(levelname)s - %(message)s’,
level=logging.INFO
)
logger = logging.getLogger(**name**)

# Your bot token from BotFather

import os
BOT_TOKEN = os getenv ('8053361541:AAFn_VBu7syZhOkR9Nxy7vc0-0NQYzRzz3g')

class ShopBot:
def **init**(self):
self.products = {
“1”: {“name”: “Prodotto 1”, “price”: “€10.00”, “description”: “Descrizione del prodotto 1”},
“2”: {“name”: “Prodotto 2”, “price”: “€15.00”, “description”: “Descrizione del prodotto 2”},
“3”: {“name”: “Prodotto 3”, “price”: “€20.00”, “description”: “Descrizione del prodotto 3”},
}

```
    self.services = {
        "1": {"name": "Servizio 1", "price": "€25.00", "description": "Descrizione del servizio 1"},
        "2": {"name": "Servizio 2", "price": "€30.00", "description": "Descrizione del servizio 2"},
    }

async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    
    # Create inline keyboard
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data='shop')],
        [InlineKeyboardButton("💰 Pagamenti 💰", callback_data='payments')],
        [InlineKeyboardButton("👥 Contattami 👥", callback_data='contact')],
        [InlineKeyboardButton("👨‍💻 Developer 👨‍💻", callback_data='developer')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"🤖 Benvenuto nello Shop Bot.\n\n🛍️ Qui troverai una vasta selezione di servizi."
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )

async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'shop':
        await self.show_shop(query)
    elif query.data == 'payments':
        await self.show_payments(query)
    elif query.data == 'contact':
        await self.show_contact(query)
    elif query.data == 'developer':
        await self.show_developer(query)
    elif query.data == 'back_to_main':
        await self.show_main_menu(query)
    elif query.data.startswith('product_'):
        product_id = query.data.split('_')[1]
        await self.show_product_details(query, product_id)
    elif query.data.startswith('service_'):
        service_id = query.data.split('_')[1]
        await self.show_service_details(query, service_id)

async def show_shop(self, query) -> None:
    """Show shop options."""
    keyboard = [
        [InlineKeyboardButton("📱 Prodotti", callback_data='products')],
        [InlineKeyboardButton("🔧 Servizi", callback_data='services')],
        [InlineKeyboardButton("⬅️ Indietro", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🛍️ **SHOP**\n\nScegli una categoria:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_payments(self, query) -> None:
    """Show payment options."""
    keyboard = [
        [InlineKeyboardButton("💳 Carta di Credito", callback_data='credit_card')],
        [InlineKeyboardButton("💰 PayPal", callback_data='paypal')],
        [InlineKeyboardButton("🏦 Bonifico", callback_data='bank_transfer')],
        [InlineKeyboardButton("⬅️ Indietro", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="💰 **PAGAMENTI**\n\nScegli un metodo di pagamento:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_contact(self, query) -> None:
    """Show contact information."""
    keyboard = [
        [InlineKeyboardButton("📧 Email", url='mailto:your-email@example.com')],
        [InlineKeyboardButton("📞 Telefono", callback_data='phone')],
        [InlineKeyboardButton("⬅️ Indietro", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="👥 **CONTATTAMI**\n\nCome preferisci essere contattato?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_developer(self, query) -> None:
    """Show developer information."""
    keyboard = [
        [InlineKeyboardButton("🌐 GitHub", url='https://github.com/yourusername')],
        [InlineKeyboardButton("💼 LinkedIn", url='https://linkedin.com/in/yourprofile')],
        [InlineKeyboardButton("⬅️ Indietro", callback_data='back_to_main')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="👨‍💻 **DEVELOPER**\n\nBot sviluppato da [Your Name]\n\nContattami per progetti personalizzati!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_main_menu(self, query) -> None:
    """Show main menu."""
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data='shop')],
        [InlineKeyboardButton("💰 Pagamenti 💰", callback_data='payments')],
        [InlineKeyboardButton("👥 Contattami 👥", callback_data='contact')],
        [InlineKeyboardButton("👨‍💻 Developer 👨‍💻", callback_data='developer')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🤖 Benvenuto nello Shop Bot.\n\n🛍️ Qui troverai una vasta selezione di servizi.",
        reply_markup=reply_markup
    )

async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages."""
    message_text = update.message.text.lower()
    
    if "ciao" in message_text or "salve" in message_text:
        await update.message.reply_text("Ciao! 👋 Usa /start per iniziare.")
    elif "aiuto" in message_text or "help" in message_text:
        await update.message.reply_text("Usa /start per vedere il menu principale.")
    else:
        await update.message.reply_text("Non ho capito. Usa /start per vedere le opzioni disponibili.")
```

def main() -> None:
“”“Start the bot.”””
# Create the Application
application = Application.builder().token(BOT_TOKEN).build()

```
# Create bot instance
bot = ShopBot()

# Register handlers
application.add_handler(CommandHandler("start", bot.start))
application.add_handler(CallbackQueryHandler(bot.button_handler))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

# Run the bot until the user presses Ctrl-C
application.run_polling(allowed_updates=Update.ALL_TYPES)
```

if **name** == ‘**main**’:
main()