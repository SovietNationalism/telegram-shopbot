import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.critical("❌ BOT_TOKEN environment variable is not set. Exiting.")
    sys.exit(1)

class ShopBot:
    def __init__(self):
        # Welcome image URL - using the provided image
        self.welcome_image_url = "https://i.postimg.cc/pr65RVVm/D6-F1-EDE3-E7-E8-4-ADC-AAFC-5-FB67-F86-BDE3.png"
        
        # Product and service images - replace with your actual URLs
        self.products = {
            "1": {
                "name": "Prodotto 1", 
                "price": "€10.00", 
                "description": "Descrizione del prodotto 1",
                "image_url": "https://example.com/product1.jpg"
            },
            "2": {
                "name": "Prodotto 2", 
                "price": "€15.00", 
                "description": "Descrizione del prodotto 2",
                "image_url": "https://example.com/product2.jpg"
            },
            "3": {
                "name": "Prodotto 3", 
                "price": "€20.00", 
                "description": "Descrizione del prodotto 3",
                "image_url": "https://example.com/product3.jpg"
            },
        }

        self.services = {
            "1": {
                "name": "Servizio 1", 
                "price": "€25.00", 
                "description": "Descrizione del servizio 1",
                "image_url": "https://example.com/service1.jpg"
            },
            "2": {
                "name": "Servizio 2", 
                "price": "€30.00", 
                "description": "Descrizione del servizio 2",
                "image_url": "https://example.com/service2.jpg"
            },
        }

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data="shop")],
            [InlineKeyboardButton("💰 Pagamenti 💰", callback_data="payments")],
            [InlineKeyboardButton("👥 Contattami 👥", callback_data="contact")],
            [InlineKeyboardButton("👨‍💻 Developer 👨‍💻", callback_data="developer")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        welcome_message = (
            "🎉 Benvenuto sul bot Vetrina ItalianEdibles! 🇮🇹\n\n"
            "Scopri un mondo di prodotti selezionati, pensati per farti avere un'esperienza "
            "unica e indimenticabile. Qui puoi esplorare, acquistare e contattarci in pochi semplici clic!"
        )
        
        try:
            # Send single message with both image and buttons
            await update.message.reply_photo(
                photo=self.welcome_image_url,
                caption=welcome_message,
                reply_markup=reply_markup
            )
        except BadRequest as e:
            logger.warning(f"Couldn't send welcome image: {e}")
            # Fallback to text only if image fails
            await update.message.reply_text(
                text=welcome_message,
                reply_markup=reply_markup
            )

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
            
        try:
            # Try to send product image with details
            await query.message.reply_photo(
                photo=product['image_url'],
                caption=(
                    f"📦 **{product['name']}**\n\n"
                    f"💵 Prezzo: {product['price']}\n"
                    f"📝 Descrizione: {product['description']}\n\n"
                    "Usa /start per effettuare un ordine"
                ),
                parse_mode="Markdown"
            )
        except BadRequest as e:
            logger.warning(f"Couldn't send product image: {e}")
            # Fallback to text only if image fails
            await query.message.reply_text(
                text=(
                    f"📦 **{product['name']}**\n\n"
                    f"💵 Prezzo: {product['price']}\n"
                    f"📝 Descrizione: {product['description']}\n\n"
                    "Usa /start per effettuare un ordine"
                ),
                parse_mode="Markdown"
            )
        
        # Show back button
        keyboard = [[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Hai selezionato: {product['name']}",
            reply_markup=reply_markup
        )

    async def show_service_details(self, query, service_id: str) -> None:
        service = self.services.get(service_id)
        if not service:
            await query.answer("Servizio non trovato!")
            return
            
        try:
            # Try to send service image with details
            await query.message.reply_photo(
                photo=service['image_url'],
                caption=(
                    f"🛠️ **{service['name']}**\n\n"
                    f"💵 Prezzo: {service['price']}\n"
                    f"📝 Descrizione: {service['description']}\n\n"
                    "Usa /start per richiedere il servizio"
                ),
                parse_mode="Markdown"
            )
        except BadRequest as e:
            logger.warning(f"Couldn't send service image: {e}")
            # Fallback to text only if image fails
            await query.message.reply_text(
                text=(
                    f"🛠️ **{service['name']}**\n\n"
                    f"💵 Prezzo: {service['price']}\n"
                    f"📝 Descrizione: {service['description']}\n\n"
                    "Usa /start per richiedere il servizio"
                ),
                parse_mode="Markdown"
            )
        
        # Show back button
        keyboard = [[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"Hai selezionato: {service['name']}",
            reply_markup=reply_markup
        )

    async def show_payments(self, query) -> None:
        payment_methods = (
            "💰 **METODI DI PAGAMENTO**\n\n"
            "• 💰 Crypto (0% commissione)\n"
            "• 💵 Contanti (0% commissione)\n"
            "• 🏦 Bonifico istantaneo (0% commissione)\n"
            "• 💳 PayPal (+10% commissione)\n\n"
            "Scegli il metodo che preferisci al momento dell'ordine."
        )
        
        keyboard = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=payment_methods,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_contact(self, query) -> None:
        keyboard = [
            [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text="👥 **CONTATTAMI**\n\nClicca il pulsante qui sotto per contattarmi direttamente su Telegram:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def show_developer(self, query) -> None:
        text = (
            "👨‍💻 **DEVELOPER**\n\n"
            "Bot sviluppato da @ItalianEdibles\n\n"
            "Contattami per progetti personalizzati!"
        )
        
        keyboard = [
            [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=text,
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
        welcome_message = (
            "🎉 Benvenuto sul bot Vetrina ItalianEdibles! 🇮🇹\n\n"
            "Scopri un mondo di prodotti selezionati, pensati per farti avere un'esperienza "
            "unica e indimenticabile. Qui puoi esplorare, acquistare e contattarci in pochi semplici clic!"
        )
        
        try:
            # Edit to show image and menu
            await query.message.reply_photo(
                photo=self.welcome_image_url,
                caption=welcome_message,
                reply_markup=reply_markup
            )
        except BadRequest as e:
            logger.warning(f"Couldn't send welcome image: {e}")
            # Fallback to text only if image fails
            await query.edit_message_text(
                text=welcome_message,
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
    logger.info("Starting bot initialization...")
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        bot = ShopBot()

        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CallbackQueryHandler(bot.button_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

        logger.info("Bot starting polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("Bot stopped")
    except Exception as e:
        logger.exception(f"❌ Bot crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()