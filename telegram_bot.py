import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

BOT_TOKEN = os.getenv("BOT_TOKEN")
WELCOME_IMAGE_URL = "https://i.postimg.cc/pr65RVVm/D6-F1-EDE3-E7-E8-4-ADC-AAFC-5-FB67-F86-BDE3.png"
ADMIN_USER_ID = 6840588025  # Only you receive file_id replies

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    logger.critical("❌ BOT_TOKEN environment variable is missing. Set it before running.")
    sys.exit(1)

class ShopBot:
    def __init__(self):
        self.products = {
            "1": {
                "name": "Dry Filtrato 🍫",
                "price": (
                    "3g 30\n"
                    "5g 40\n"
                    "10g 70\n"
                    "15g 100\n"
                    "25g 160\n"
                    "35g 215\n"
                    "50g 250\n"
                    "100g 420\n"
                    "200g 780"
                ),
                "description": "Dry con effetto potente e duraturo, e un odore vivace",
                "video_file_id": "BAACAgQAAxkBAAPCaGv91fParWTOjzMLqrdb2v-pB0wAAksWAAKdJ2FTkI7DxvBinmg2BA"
            },
            "2": {
                "name": "Sciroppo al THC 🫗",
                "price": (
                    "x 1 150 ml 30€\n"
                    "x 2 300 ml 40€\n"
                    "x 5 750 ml 100€\n"
                    "x 10 1,5 l 190€\n"
                    "x 20 3 l 335€"
                ),
                "description": (
                    "🇮🇹 SCIROPPO THC\n"
                    "🍇 Gusti: Lampone, Fragola, Menta, Limone\n\n"
                    "Una formula esclusiva, realizzata con estratto di hashish a base di etanolo di alta qualità, emulsionato in sciroppo al lampone per una stabilità e biodisponibilità superiore.\n\n"
                    "💧 Da mescolare con qualsiasi tipo di bevanda! Consigliamo liquidi fredde e dolci per mascherare il sapore.\n"
                    "Ogni bottiglia contiene 250 mg di THC attivo in 150 ml di sciroppo.\n\n"
                    "📐 Dosaggio consigliato (1.66 mg/ml):\n"
                    " • 🟢 Principianti: 10–15 mg (6–9 ml circa)\n"
                    " • 🟡 Regolari: 25–35 mg (15–20 ml)\n"
                    " • 🔴 Esperti: 50+ mg (30 ml e oltre)"
                ),
                "video_file_id": "BAACAgQAAxkBAAIBCmhsFSRwLTrFoTt3ZbImNDzA8cKtAALKHQACU4xhU_j8jDMDFSiJNgQ"
            },
            "3": {
                "name": "Caramelle al THC 🇪🇸",
                "video_file_id": "BAACAgQAAxkBAAPvaGwJdobhaO1RPvm1nrbxIKokTOIAAqgdAAJTjGFTqdTZCjgZEpU2BA",
            },
            "4": {
                "name": "THC VAPE PACKWOODS x Runtz",
                "price": "1 - 45\n2 - 80\n3 - 110\n4 - 135\n5 - 160\n10 - 300",
                "description": "1000mg distillato Delta 9 THC",
                "special_note": "Dettaglio sotto i 5 pz non ancora disponibile. Tra poco."
            }
        }
        self.services = {
            "1": {
                "name": "Servizio 1",
                "price": "€25.00",
                "description": "Descrizione del servizio 1",
                "photo_file_id": "AgACAgQAAxkBAAIBVmY0n9f5v1cAAQ1nUuH4QnX8h3QjAAJ8tzEbJ2FTkJ7yK5y1vN2BAAMCAANzAAMvBA"
            }
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

        message = update.effective_message
        try:
            await message.reply_photo(
                photo=WELCOME_IMAGE_URL,
                caption=welcome_message,
                reply_markup=reply_markup
            )
        except BadRequest as e:
            logger.warning(f"❌ Impossibile inviare l'immagine di benvenuto: {e}")
            await message.reply_text(text=welcome_message, reply_markup=reply_markup)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        data = query.data
        chat_id = query.message.chat.id

        async def safe_edit_or_send(text, keyboard, parse_mode=ParseMode.MARKDOWN):
            msg = query.message
            if getattr(msg, "photo", None):
                try:
                    await msg.delete()
                except Exception:
                    pass
                await context.bot.send_message(
                    chat_id=msg.chat.id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=parse_mode
                )
            else:
                try:
                    await query.edit_message_text(
                        text=text,
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        parse_mode=parse_mode
                    )
                except BadRequest:
                    await context.bot.send_message(
                        chat_id=msg.chat.id,
                        text=text,
                        reply_markup=InlineKeyboardMarkup(keyboard),
                        parse_mode=parse_mode
                    )

        async def delete_product_service_msgs():
            for key in ["product_msg_id", "service_msg_id"]:
                msg_id = context.user_data.get(key)
                if msg_id:
                    try:
                        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                    except Exception:
                        pass
                    context.user_data[key] = None

        if data in ["back_to_products"]:
            msg_id = context.user_data.get("product_msg_id")
            if msg_id:
                try:
                    await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                except Exception:
                    pass
                context.user_data["product_msg_id"] = None

        if data in ["back_to_services"]:
            msg_id = context.user_data.get("service_msg_id")
            if msg_id:
                try:
                    await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
                except Exception:
                    pass
                context.user_data["service_msg_id"] = None

        if data in ["back_to_main", "back_to_shop"]:
            await delete_product_service_msgs()

        if data == "shop":
            await safe_edit_or_send(
                "🛍️ *SHOP*\n\nScegli una categoria:",
                [
                    [InlineKeyboardButton("📱 Prodotti", callback_data="products")],
                    [InlineKeyboardButton("🔧 Servizi", callback_data="services")],
                    [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
                ]
            )
        elif data == "payments":
            await safe_edit_or_send(
                "💰 *METODI DI PAGAMENTO*\n\n"
                "• 💰 Crypto (0% commissione)\n"
                "• 💵 Contanti (0% commissione)\n"
                "• 🏦 Bonifico istantaneo (0% commissione)\n"
                "• 💳 PayPal (+10% commissione)\n\n"
                "Scegli il metodo che preferisci al momento dell'ordine.",
                [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            )
        elif data == "contact":
            await safe_edit_or_send(
                "👥 *CONTATTAMI*\n\nClicca il pulsante qui sotto per contattarmi direttamente su Telegram:",
                [
                    [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
                    [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
                ]
            )
        elif data == "developer":
            await safe_edit_or_send(
                "👨‍💻 *DEVELOPER*\n\n"
                "Bot sviluppato da @ItalianEdibles\n\n"
                "Contattami per progetti personalizzati!",
                [
                    [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
                    [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
                ]
            )
        elif data == "back_to_main":
            try:
                await query.message.delete()
            except Exception:
                pass
            await self.start(update, context)
        elif data == "products":
            keyboard = [
                [InlineKeyboardButton(f"{self.products['1']['name']}", callback_data="product_1")],
                [InlineKeyboardButton(f"{self.products['2']['name']}", callback_data="product_2")],
                [
                    InlineKeyboardButton("Caramelle THC 🇪🇸 - Formato 10", callback_data="product_3_format_10"),
                    InlineKeyboardButton("Caramelle THC 🇪🇸 - Formato 20", callback_data="product_3_format_20")
                ],
                [InlineKeyboardButton(f"{self.products['4']['name']}", callback_data="product_4")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")]
            ]
            await safe_edit_or_send(
                "📱 *PRODOTTI DISPONIBILI*\n\nScegli un prodotto:",
                keyboard
            )
        elif data == "services":
            keyboard = [
                [InlineKeyboardButton(f"{s['name']}", callback_data=f"service_{sid}")]
                for sid, s in self.services.items()
            ]
            keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")])
            await safe_edit_or_send(
                "🔧 *SERVIZI DISPONIBILI*\n\nScegli un servizio:",
                keyboard
            )
        elif data.startswith("product_3_format_"):
            format_id = data.split("_")[-1]
            product = self.products["3"]
            if format_id == "10":
                caption = (
                    "📦 *Caramelle al THC 🇪🇸 - Formato 10 caramelle da 500mg*\n"
                    "Runtz Gummies\nWhite Runtz Fruit Punch - “Ether” Runtz Green Apple - Original Runtz Berries - Pink Runtz Watermelon\n\n"
                    "Smacker Gummies Sours (Mix Green Apple, Blue Raspberry, Cherry, Lemon & Watermelon)\n\n"
                    "Warheads Sour Medicated Chewy Cubes\n(Mix Orange, Watermelon, Blue Raspberry, Black Cherry, Strawberry, Green Apple)\n\n"
                    "1 - 20\n2 - 35\n3 - 50\n4 - 60\n5 - 70\n10 - 130"
                )
            elif format_id == "20":
                caption = (
                    "📦 *Caramelle al THC 🇪🇸 - Formato 20 caramelle 600mg*\n"
                    "Rancher Gummies Original Flavors (Mix Strawberry, Green Apple, Blue Raspberry)\n\n"
                    "Rancher Gummies Sours (Mix Strawberry, Green Apple, Blue Raspberry)\n\n"
                    "Warheads Sour Medicated Chewy Cubes\n(Mix Orange, Watermelon, Blue Raspberry, Black Cherry, Strawberry, Green Apple)\n\n"
                    "1 - 25\n2 - 40\n3 - 55\n4 - 70\n5 - 80\n10 - 140"
                )
            else:
                caption = "Formato non trovato."
            # Send video if available
            if product.get("video_file_id"):
                try:
                    sent = await context.bot.send_video(
                        chat_id=query.message.chat.id,
                        video=product["video_file_id"],
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        supports_streaming=True
                    )
                    context.user_data["product_msg_id"] = sent.message_id
                except BadRequest as e:
                    logger.warning(f"Errore invio video prodotto: {e}")
                    sent = await context.bot.send_message(
                        chat_id=query.message.chat.id,
                        text=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    context.user_data["product_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(
                    chat_id=query.message.chat.id,
                    text=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
                context.user_data["product_msg_id"] = sent.message_id

            await safe_edit_or_send(
                f"Hai selezionato: Caramelle THC 🇪🇸 - Formato {format_id}",
                [[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]
            )
        elif data == "product_1" or data == "product_2":
            product_id = data.split("_")[1]
            product = self.products.get(product_id)
            if not product:
                await query.answer("❌ Prodotto non trovato!")
                return
            video_file_id = product.get("video_file_id")
            photo_file_id = product.get("photo_file_id")
            caption = (
                f"📦 *{product['name']}*\n"
                f"💵 Prezzo:\n{product['price']}\n"
                f"📝 Descrizione: {product['description']}"
            )
            if video_file_id:
                try:
                    sent = await context.bot.send_video(
                        chat_id=query.message.chat.id,
                        video=video_file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        supports_streaming=True
                    )
                    context.user_data["product_msg_id"] = sent.message_id
                except BadRequest as e:
                    logger.warning(f"Errore invio video prodotto: {e}")
                    sent = await context.bot.send_message(
                        chat_id=query.message.chat.id,
                        text=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    context.user_data["product_msg_id"] = sent.message_id
            elif photo_file_id:
                try:
                    sent = await context.bot.send_photo(
                        chat_id=query.message.chat.id,
                        photo=photo_file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    context.user_data["product_msg_id"] = sent.message_id
                except BadRequest as e:
                    logger.warning(f"Errore invio immagine prodotto: {e}")
                    sent = await context.bot.send_message(
                        chat_id=query.message.chat.id,
                        text=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    context.user_data["product_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(
                    chat_id=query.message.chat.id,
                    text=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
                context.user_data["product_msg_id"] = sent.message_id

            await safe_edit_or_send(
                f"Hai selezionato: {product['name']}",
                [[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]
            )
        elif data == "product_4":
            product = self.products["4"]
            lines = product["price"].split("\n")
            caption_lines = []
            for line in lines:
                qty = int(line.split(" - ")[0])
                if qty < 5:
                    caption_lines.append(f"~~{line}~~")
                else:
                    caption_lines.append(line)
            caption = (
                f"📦 *{product['name']}*\n"
                f"💵 Prezzo:\n" + "\n".join(caption_lines) +
                f"\n📝 Descrizione: {product['description']}\n\n*{product['special_note']}*"
            )
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=caption,
                parse_mode=ParseMode.MARKDOWN
            )
            await safe_edit_or_send(
                f"Hai selezionato: {product['name']}",
                [[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]
            )
        elif data.startswith("service_"):
            service_id = data.split("_")[1]
            service = self.services.get(service_id)
            if not service:
                await query.answer("❌ Servizio non trovato!")
                return
            video_file_id = service.get("video_file_id")
            photo_file_id = service.get("photo_file_id")
            caption = (
                f"🛠️ *{service['name']}*\n"
                f"💵 Prezzo:\n{service['price']}\n"
                f"📝 Descrizione: {service['description']}"
            )
            if video_file_id:
                try:
                    sent = await context.bot.send_video(
                        chat_id=query.message.chat.id,
                        video=video_file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        supports_streaming=True
                    )
                    context.user_data["service_msg_id"] = sent.message_id
                except BadRequest as e:
                    logger.warning(f"Errore invio video servizio: {e}")
                    sent = await context.bot.send_message(
                        chat_id=query.message.chat.id,
                        text=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    context.user_data["service_msg_id"] = sent.message_id
            elif photo_file_id:
                try:
                    sent = await context.bot.send_photo(
                        chat_id=query.message.chat.id,
                        photo=photo_file_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    context.user_data["service_msg_id"] = sent.message_id
                except BadRequest as e:
                    logger.warning(f"Errore invio immagine servizio: {e}")
                    sent = await context.bot.send_message(
                        chat_id=query.message.chat.id,
                        text=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )
                    context.user_data["service_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(
                    chat_id=query.message.chat.id,
                    text=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
                context.user_data["service_msg_id"] = sent.message_id

            await safe_edit_or_send(
                f"Hai selezionato: {service['name']}",
                [[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]
            )
        elif data == "back_to_shop":
            await safe_edit_or_send(
                "🛍️ *SHOP*\n\nScegli una categoria:",
                [
                    [InlineKeyboardButton("📱 Prodotti", callback_data="products")],
                    [InlineKeyboardButton("🔧 Servizi", callback_data="services")],
                    [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
                ]
            )
        elif data == "back_to_products":
            keyboard = [
                [InlineKeyboardButton(f"{self.products['1']['name']}", callback_data="product_1")],
                [InlineKeyboardButton(f"{self.products['2']['name']}", callback_data="product_2")],
                [
                    InlineKeyboardButton("Caramelle THC 🇪🇸 - Formato 10", callback_data="product_3_format_10"),
                    InlineKeyboardButton("Caramelle THC 🇪🇸 - Formato 20", callback_data="product_3_format_20")
                ],
                [InlineKeyboardButton(f"{self.products['4']['name']}", callback_data="product_4")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")]
            ]
            await safe_edit_or_send(
                "📱 *PRODOTTI DISPONIBILI*\n\nScegli un prodotto:",
                keyboard
            )
        elif data == "back_to_services":
            keyboard = [
                [InlineKeyboardButton(f"{s['name']}", callback_data=f"service_{sid}")]
                for sid, s in self.services.items()
            ]
            keyboard.append([InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_shop")])
            await safe_edit_or_send(
                "🔧 *SERVIZI DISPONIBILI*\n\nScegli un servizio:",
                keyboard
            )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message

        # Only admin receives file_id replies for both images and videos
        if message.from_user and message.from_user.id == ADMIN_USER_ID:
            if message.video:
                await message.reply_text(
                    f"File ID del video:\n<code>{message.video.file_id}</code>",
                    parse_mode=ParseMode.HTML
                )
                return
            if message.photo:
                # Telegram sends photos as a list of sizes, last is highest quality
                file_id = message.photo[-1].file_id
                await message.reply_text(
                    f"File ID della foto:\n<code>{file_id}</code>",
                    parse_mode=ParseMode.HTML
                )
                return

        text = message.text.lower() if message.text else ""
        if any(word in text for word in ["ciao", "salve"]):
            await message.reply_text("Ciao! 👋 Usa /start per iniziare.")
        elif "aiuto" in text or "help" in text:
            await message.reply_text("Usa /start per vedere il menu principale.")
        else:
            await message.reply_text("Non ho capito. Usa /start per vedere le opzioni disponibili.")

def main():
    logger.info("Avvio del bot...")
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        bot = ShopBot()

        app.add_handler(CommandHandler("start", bot.start))
        app.add_handler(CallbackQueryHandler(bot.button_handler))
        app.add_handler(MessageHandler(filters.ALL, bot.handle_message))

        app.run_polling()
        logger.info("Bot terminato.")
    except Exception as e:
        logger.exception(f"❌ Errore critico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
