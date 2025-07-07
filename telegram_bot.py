import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Your bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

class ShopBot:
    def __init__(self):
        self.products = {
            "1": {"name": "Prodotto 1", "price": "€10.00", "description": "Descrizione del prodotto 1"},
            "2": {"name": "Prodotto 2", "price": "€15.00", "description": "Descrizione del prodotto 2"},
            "3": {"name": "Prodotto 3", "price": "€20.00", "description": "Descrizione del prodotto 3"},
        }

        self.services = {
            "1": {"name": "Servizio 1", "price": "€25.00", "description": "Descrizione del servizio 1"},
            "2": {"name": "Servizio 2", "price": "€30.00", "description": "Descrizione del servizio 2"},
        }

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data="shop")],
            [InlineKeyboardButton("💰 Pagamenti 💰", callback_data="payments")],
            [InlineKeyboardButton("👥 Contattami 👥", callback_data="contact")],
            [InlineKeyboardButton("👨‍💻 Developer 👨‍💻", callback_data="developer")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_message = "🤖 Benvenuto nello Shop Bot.\n\n🛍️ Qui troverai una vasta selezione di servizi."
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        
        if query.data == "shop":
            await self.show_shop(query)
        elif query.data == "payments":
            await self.show_payments(query)
        elif query.data == "contact":
            await self.show_contact(query)
        elif query.data == "developer":
            await self.show_developer(query)
        elif query.data == "back_to_main":
            await self.show_main_menu(query)
        elif query.data == "products":
            await self.show_products(query)
        elif query.data == "services":
            await self.show_services(query)
        elif query.data.startswith("product_"):
            product_id = query.data.split("_")[1]
            await self.show_product_details(query, product_id)
        elif query.data.startswith("service_"):
            service_id = query.data.split("_")[1]
            await self.show_service_details(query, service_id)
        elif query.data == "back_to_shop":
            await self.show_shop(query)
        elif query.data == "back_to_products":
            await self.show_products(query)
        elif query.data == "back_to_services":
            await self.show_services(query)

    async def show_shop(self, query) -> None:
        keyboard = [
            [InlineKeyboardButton("📱 Prodotti", callback_data="products")],
            [InlineKeyboardButton("🔧 Servizi", callback_data="services")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🛍️ **SHOP**\n\nScegli una categoria:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_products(self, query) -> None:
        keyboard = []
        for product_id, product in self.products.items():
            keyboard.append([InlineKeyboardButton(
                f"{product['name']} - {product['price']}",
                callback_data=f"product_{product_id}"
            )])
        
        keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="📱 **PRODOTTI DISPONIBILI**\n\nScegli un prodotto:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_services(self, query) -> None:
        keyboard = []
        for service_id, service in self.services.items():
            keyboard.append([InlineKeyboardButton(
                f"{service['name']} - {service['price']}",
                callback_data=f"service_{service_id}"
            )])
        
        keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="🔧 **SERVIZI DISPONIBILI**\n\nScegli un servizio:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_product_details(self, query, product_id: str) -> None:
        product = self.products.get(product_id)
        if not product:
            await query.answer("Prodotto non trovato!")
            return
            
        text = (
            f"📦 **{product['name']}**\n\n"
            f"💵 Prezzo: {product['price']}\n"
            f"📝 Descrizione: {product['description']}\n\n"
            "Usa /start per effettuare un ordine"
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_service_details(self, query, service_id: str) -> None:
        service = self.services.get(service_id)
        if not service:
            await query.answer("Servizio non trovato!")
            return
            
        text = (
            f"🛠️ **{service['name']}**\n\n"
            f"💵 Prezzo: {service['price']}\n"
            f"📝 Descrizione: {service['description']}\n\n"
            "Usa /start per richiedere il servizio"
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_payments(self, query) -> None:
        keyboard = [
            [InlineKeyboardButton("💳 Carta di Credito", callback_data="credit_card")],
            [InlineKeyboardButton("💰 PayPal", callback_data="paypal")],
            [InlineKeyboardButton("🏦 Bonifico", callback_data="bank_transfer")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="💰 **PAGAMENTI**\n\nScegli un metodo di pagamento:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_contact(self, query) -> None:
        keyboard = [
            [InlineKeyboardButton("📧 Email", url="mailto:your-email@example.com")],
            [InlineKeyboardButton("📞 Telefono", callback_data="phone")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="👥 **CONTATTAMI**\n\nCome preferisci essere contattato?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_developer(self, query) -> None:
        keyboard = [
            [InlineKeyboardButton("🌐 GitHub", url="https://github.com/yourusername")],
            [InlineKeyboardButton("💼 LinkedIn", url="https://linkedin.com/in/yourprofile")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="👨‍💻 **DEVELOPER**\n\nBot sviluppato da [Your Name]\n\nContattami per progetti personalizzati!",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_main_menu(self, query) -> None:
        keyboard = [
            [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data="shop")],
            [InlineKeyboardButton("💰 Pagamenti 💰", callback_data="payments")],
            [InlineKeyboardButton("👥 Contattami 👥", callback_data="contact")],
            [InlineKeyboardButton("👨‍💻 Developer 👨‍💻", callback_data="developer")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text="🤖 Benvenuto nello Shop Bot.\n\n🛍️ Qui troverai una vasta selezione di servizi.",
            reply_markup=reply_markup
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message_text = update.message.text.lower()
        
        if "ciao" in message_text or "salve" in message_text:
            await update.message.reply_text("Ciao! 👋 Usa /start per iniziare.")
        elif "aiuto" in message_text or "help" in message_text:
            await update.message.reply_text("Usa /start per vedere il menu principale.")
        else:
            await update.message.reply_text("Non ho capito. Usa /start per vedere le opzioni disponibili.")

def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")
        
    application = Application.builder().token(BOT_TOKEN).build()
    bot = ShopBot()

    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CallbackQueryHandler(bot.button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()