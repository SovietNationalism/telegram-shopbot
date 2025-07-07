import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_IMAGE_URL = "https://i.postimg.cc/pr65RVVm/D6-F1-EDE3-E7-E8-4-ADC-AAFC-5-FB67-F86-BDE3.png"

# === LOGGER ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    logger.critical("❌ BOT_TOKEN environment variable is missing. Set it before running.")
    sys.exit(1)

# === BOT CLASS ===
class ShopBot:
    def __init__(self):
        self.products = {
            "1": {"name": "Prodotto 1", "price": "€10.00", "description": "Descrizione del prodotto 1", "image_url": "https://example.com/product1.jpg"},
            "2": {"name": "Prodotto 2", "price": "€15.00", "description": "Descrizione del prodotto 2", "image_url": "https://example.com/product2.jpg"},
            "3": {"name": "Prodotto 3", "price": "€20.00", "description": "Descrizione del prodotto 3", "image_url": "https://example.com/product3.jpg"},
        }

        self.services = {
            "1": {"name": "Servizio 1", "price": "€25.00", "description": "Descrizione del servizio 1", "image_url": "https://example.com/service1.jpg"},
            "2": {"name": "Servizio 2", "price": "€30.00", "description": "Descrizione del servizio 2", "image_url": "https://example.com/service2.jpg"},
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
            "Scopri un mondo di prodotti selezionati, pensati per un'esperienza unica e indimenticabile. "
            "Puoi esplorare, acquistare e contattarci in pochi semplici clic!"
        )

        try:
            await update.message.reply_photo(
                photo=WELCOME_IMAGE_URL,
                caption=welcome_message,
                reply_markup=reply_markup
            )
        except BadRequest as e:
            logger.warning(f"❌ Impossibile inviare l'immagine di benvenuto: {e}")
            await update.message.reply_text(text=welcome_message, reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        match query.data:
            case "shop": await self.show_shop(query)
            case "payments": await self.show_payments(query)
            case "contact": await self.show_contact(query)
            case "developer": await self.show_developer(query)
            case "back_to_main": await self.show_main_menu(query)
            case "products": await self.show_products(query)
            case "services": await self.show_services(query)
            case _ if query.data.startswith("product_"):
                await self.show_product_details(query, query.data.split("_")[1])
            case _ if query.data.startswith("service_"):
                await self.show_service_details(query, query.data.split("_")[1])
            case "back_to_shop": await self.show_shop(query)
            case "back_to_products": await self.show_products(query)
            case "back_to_services": await self.show_services(query)

    async def show_shop(self, query):
        keyboard = [
            [InlineKeyboardButton("📱 Prodotti", callback_data="products")],
            [InlineKeyboardButton("🔧 Servizi", callback_data="services")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        await query.edit_message_text(
            text="🛍️ *SHOP*\n\nScegli una categoria:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    async def show_products(self, query):
        keyboard = [
            [InlineKeyboardButton(f"{p['name']} - {p['price']}", callback_data=f"product_{pid}")]
            for pid, p in self.products.items()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")])
        await query.edit_message_text(
            text="📱 *PRODOTTI DISPONIBILI*\n\nScegli un prodotto:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    async def show_services(self, query):
        keyboard = [
            [InlineKeyboardButton(f"{s['name']} - {s['price']}", callback_data=f"service_{sid}")]
            for sid, s in self.services.items()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")])
        await query.edit_message_text(
            text="🔧 *SERVIZI DISPONIBILI*\n\nScegli un servizio:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    async def show_product_details(self, query, product_id):
        product = self.products.get(product_id)
        if not product:
            await query.answer("❌ Prodotto non trovato!")
            return

        try:
            await query.message.reply_photo(
                photo=product['image_url'],
                caption=(
                    f"📦 *{product['name']}*\n"
                    f"💵 Prezzo: {product['price']}\n"
                    f"📝 Descrizione: {product['description']}\n\n"
                    "Usa /start per effettuare un ordine"
                ),
                parse_mode="Markdown"
            )
        except BadRequest as e:
            logger.warning(f"Errore invio immagine prodotto: {e}")
            await query.message.reply_text(
                f"📦 *{product['name']}*\n💵 Prezzo: {product['price']}\n📝 Descrizione: {product['description']}\n\nUsa /start per ordinare",
                parse_mode="Markdown"
            )

        await query.edit_message_text(
            text=f"Hai selezionato: {product['name']}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]])
        )

    async def show_service_details(self, query, service_id):
        service = self.services.get(service_id)
        if not service:
            await query.answer("❌ Servizio non trovato!")
            return

        try:
            await query.message.reply_photo(
                photo=service['image_url'],
                caption=(
                    f"🛠️ *{service['name']}*\n"
                    f"💵 Prezzo: {service['price']}\n"
                    f"📝 Descrizione: {service['description']}\n\n"
                    "Usa /start per richiedere il servizio"
                ),
                parse_mode="Markdown"
            )
        except BadRequest:
            await query.message.reply_text(
                f"🛠️ *{service['name']}*\n💵 Prezzo: {service['price']}\n📝 Descrizione: {service['description']}\n\nUsa /start per richiedere il servizio",
                parse_mode="Markdown"
            )

        await query.edit_message_text(
            text=f"Hai selezionato: {service['name']}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]])
        )

    async def show_payments(self, query):
        text = (
            "💰 *METODI DI PAGAMENTO*\n\n"
            "• 💰 Crypto (0% commissione)\n"
            "• 💵 Contanti (0% commissione)\n"
            "• 🏦 Bonifico istantaneo (0% commissione)\n"
            "• 💳 PayPal (+10% commissione)\n\n"
            "Scegli il metodo che preferisci al momento dell'ordine."
        )
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]), parse_mode="Markdown")

    async def show_contact(self, query):
        keyboard = [
            [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
        ]
        await query.edit_message_text(
            text="👥 *CONTATTAMI*\n\nClicca il pulsante qui sotto per contattarmi direttamente su Telegram:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    async def show_developer(self, query):
        text = (
            "👨‍💻 *DEVELOPER*\n\n"
            "Bot sviluppato da @ItalianEdibles\n\n"
            "Contattami per progetti personalizzati!"
        )
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
            ]),
            parse_mode="Markdown"
        )

    async def show_main_menu(self, query):
        await self.start(query, None)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text.lower()
        if any(word in text for word in ["ciao", "salve"]):
            await update.message.reply_text("Ciao! 👋 Usa /start per iniziare.")
        elif "aiuto" in text or "help" in text:
            await update.message.reply_text("Usa /start per vedere il menu principale.")
        else:
            await update.message.reply_text("Non ho capito. Usa /start per vedere le opzioni disponibili.")

# === MAIN ===
def main():
    logger.info("Avvio del bot...")
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        bot = ShopBot()

        app.add_handler(CommandHandler("start", bot.start))
        app.add_handler(CallbackQueryHandler(bot.button_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))

        app.run_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("Bot terminato.")
    except Exception as e:
        logger.exception(f"❌ Errore critico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()