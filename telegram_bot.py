import os, sys, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USER_ID = 6840588025
WELCOME_IMAGE_URL = "https://i.postimg.cc/pr65RVVm/D6-F1-EDE3-E7-E8-4-ADC-AAFC-5-FB67-F86-BDE3.png"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
if not BOT_TOKEN: logger.critical("❌ BOT_TOKEN missing."); sys.exit(1)

class ShopBot:
    def __init__(self):
        self.products = {
            "1": {
                "name": "Dry Filtrato 🍫",
                "price": "3g 30\n5g 40\n10g 70\n15g 100\n25g 160\n35g 215\n50g 250\n100g 430\n200g 780",
                "description": "Dry filtrato a 120 micron con effetto potente e duraturo, e un odore vivace.",
                "video_file_id": "BAACAgQAAxkBAAICKGhtHmeAa3WA1B8UshA03xwIGRh6AAItHgACw-ZoUyEBRLZYiRBqNgQ"
            },
            "2": {
                "name": "Sciroppo al THC 🫗",
                "price": "x 1 150 ml 30€\nx 2 300 ml 40€\nx 5 750 ml 100€\nx 10 1,5 l 190€\nx 20 3 l 335€",
                "description": "\n Gusti: Lampone, Fragola, Menta, Limone\n\nUna formula composta con estratto di hashish a base di etanolo di alta qualità, emulsionato in uno sciroppo dolce per una stabilità e biodisponibilità superiore.\n\n💧 Da mescolare con qualsiasi tipo di bevanda! Consigliamo liquidi freddi e dolci per mascherare il sapore.\nOgni bottiglia contiene 300 mg di THC attivo in 150 ml di sciroppo. Scuotere la boccetta prima di ogni uso per distribuirlo bene.\n\n📐 Dosaggio consigliato (2 mg/ml):\n• 🟢 Principianti: 10–15 mg (5–7.5 ml circa)\n• 🟡 Regolari: 25–35 mg (12.5–17.5 ml)\n• 🔴 Esperti: 50+ mg (25 ml e oltre)",
                "video_file_id": "BAACAgQAAxkBAAIBCmhsFSRwLTrFoTt3ZbImNDzA8cKtAALKHQACU4xhU_j8jDMDFSiJNgQ"
            },
            "3_10": {
                "name": "Caramelle al THC 🇪🇸 - Formato 10",
                "caption": "📦 *Caramelle al THC 🇪🇸 - Formato 10 caramelle da 500mg*\nRuntz Gummies\nWhite Runtz Fruit Punch - “Ether” Runtz Green Apple - Original Runtz Berries - Pink Runtz Watermelon\n\nSmacker Gummies Sours (Mix Green Apple, Blue Raspberry, Cherry, Lemon & Watermelon)\n\nWarheads Sour Medicated Chewy Cubes\n(Mix Orange, Watermelon, Blue Raspberry, Black Cherry, Strawberry, Green Apple)\n\n1 - 20\n2 - 35\n3 - 50\n4 - 60\n5 - 70\n10 - 130\n\nQueste caramelle gommose hanno una consistenza densa stile orsetti Haribo, un ottimo sapore e un effetto sorprendentemente potente.",
                "video_file_id": "BAACAgQAAxkBAAPvaGwJdobhaO1RPvm1nrbxIKokTOIAAqgdAAJTjGFTqdTZCjgZEpU2BA"
            },
            "3_20": {
                "name": "Caramelle al THC 🇪🇸 - Formato 20",
                "caption": "📦 *Caramelle al THC 🇪🇸 - Formato 20 caramelle 600mg*\nRancher Gummies Original Flavors (Mix Strawberry, Green Apple, Blue Raspberry)\n\nRancher Gummies Sours (Mix Strawberry, Green Apple, Blue Raspberry)\n\nWarheads Sour Medicated Chewy Cubes\n(Mix Orange, Watermelon, Blue Raspberry, Black Cherry, Strawberry, Green Apple)\n\n1 - 25\n2 - 40\n3 - 55\n4 - 70\n5 - 80\n10 - 140\n\nQueste caramelle gommose hanno una consistenza densa stile orsetti Haribo, un ottimo sapore e un effetto sorprendentemente potente.",
                "video_file_id": "BAACAgQAAxkBAAPvaGwJdobhaO1RPvm1nrbxIKokTOIAAqgdAAJTjGFTqdTZCjgZEpU2BA"
            },
            "4": {
                "name": "THC Vapes Packwoods™ x Runtz 💨",
                "price": "1 - 45\n2 - 80\n3 - 110\n4 - 135\n5 - 160\n10 - 300",
                "description": "Con 1000mg di distillato Delta 9 THC, basta una decina di tiri per sentira una fattanza potente.",
                "special_note": "Dettaglio sotto i 5 pz non ancora disponibile. Tra poco.",
                "video_file_id": "BAACAgQAAxkBAAIBhGhsLZ3WwkXvnqI-G74L_hsWrg6YAAI8GQACw-ZgU0zEehfiSYpmNgQ"
            },
            "5": {
                "name": "THC Brownies",
                "caption": (
                    "📦 *THC Brownies*\n"
                    "💵 Prezzo:\n1pz 10€\n2pz 15€\n5pz 35€\n10pz 65€\n20pz 120€\n50pz 280€\n\n"
                    "📝 Descrizione: Brownie al cioccolato con 50mg di THC per pezzo, preparato con burro infuso e lecitina per un effetto potente e ben bilanciato.\n"
                    "*Offerta limitata*: Se aggiungi un singolo brownie a un ordine di min. 25€, ti costerà solo 5€ invece che 10€.\n\n"
                    "⚠️ Non consumate l’intero brownie (a meno che non abbiate una tolleranza alta).\n"
                    "Ogni brownie contiene 50 mg di THC; consigliamo di dividerlo con un amico o conservarne metà per dopo.\n"
                    "💡 Pro tip: Scaldatelo nel microonde per 10–20 secondi prima di mangiarlo: sarà caldo e ancora più buono!"
                ),
                "video_file_id": "BAACAgQAAxkBAAICzmhucsfJasY9h-D9-mTSUhFTYGisAAIcGgACeZJxUyMtK0Venf2aNgQ"
            },
            "6": {
                "name": "THC Cookies 🍪",
                "caption": (
                    "📦 *THC Cookies*\n"
                    "💵 Prezzo:\n1pz 8€\n2pz 14€\n5pz 30€\n10pz 55€\n20pz 100€\n50pz 230€\n\n"
                    "📝 Descrizione:\n"
                    "Biscotto morbido al cioccolato con 35mg di THC per pezzo, preparato con crumble di brownie e burro infuso per un gusto intenso e una consistenza chewy. "
                    "Effetto ben bilanciato, confezionato singolarmente per massima discrezione e freschezza."
                ),
                "video_file_id": "BAACAgQAAxkBAAIC2WhuyCwydopTi2xpCcoGIKe3YHoAA7YVAAJz7nFTWGJ8xrGDgw42BA"
            }
        }
        self.services = {
            "1": {
                "name": "Creazione Bot Telegram",
                "price": "€35/m",
                "description": "Sei un venditore o comunque sei interessato alla creazione di un bot simile? Posso aiutarti.",
                "photo_file_id": "AgACAgQAAxkBAAIBVmY0n9f5v1cAAQ1nUuH4QnX8h3QjAAJ8tzEbJ2FTkJ7yK5y1vN2BAAMCAANzAAMvBA"
            }
        }

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.delete_last_menu(context, update.effective_chat.id)
        kb = [
            [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data="shop")],
            [InlineKeyboardButton("💰 Pagamenti 💰", callback_data="payments")],
            [InlineKeyboardButton("📢 Canale Telegram 📢", url="https://t.me/+A3JnK9ALAmtiMjBk")],
            [InlineKeyboardButton("👥 Contattami 👥", callback_data="contact")],
            [InlineKeyboardButton("👨‍💻 Developer 👨‍💻", callback_data="developer")]
        ]
        msg = "🎉 Benvenuto sul bot Vetrina ItalianEdibles! 🇮🇹\n\nScopri un mondo di prodotti selezionati, pensati per un'esperienza unica e indimenticabile. Puoi esplorare, e contattarci in pochi semplici clic!"
        m = update.effective_message
        try:
            sent = await m.reply_photo(photo=WELCOME_IMAGE_URL, caption=msg, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
        except BadRequest:
            sent = await m.reply_text(text=msg, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id

    async def delete_last_menu(self, context, chat_id):
        msg_id = context.user_data.get("last_menu_msg_id")
        if msg_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
            context.user_data["last_menu_msg_id"] = None

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        q = update.callback_query
        await q.answer()
        d = q.data
        cid = q.message.chat.id
        await self.delete_last_menu(context, cid)
        if d == "back_to_main":
            await self.start(update, context)
            return
        if d == "shop":
            kb = [
                [InlineKeyboardButton("📱 Prodotti", callback_data="products")],
                [InlineKeyboardButton("🔧 Servizi", callback_data="services")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
            ]
            sent = await context.bot.send_message(chat_id=cid, text="🛍️ *SHOP*\n\nScegli una categoria:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d == "payments":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            payments_text = (
                "💰 *METODI DI PAGAMENTO*\n\n"
                "• 🏦 Bonifico istantaneo (0% commissione)\n"
                "• 📲 Hype / Revolut / Satispay (0% commissione)\n"
                "• 💸 Crypto LTC / BTC (-10% commissione)\n"
                "• 💵 Contanti (0% commissione)\n"
                "• 💳 PayPal (+10% commissione)\n"
                "• 💼 Carta prepagata/buono (+10% commissione)\n\n"
                "📦 *POLITICA DI RESHIP E ASSISTENZA*\n\n"
                "In caso di pacco smarrito o perso in transito di ordini è previsto il rimborso o rispedizione del materiale.\n"
                "Per resi o problemi sul prodotto, è obbligatorio fornire:\n"
                "• 🎥 Un video senza tagli dell’apertura del locker\n"
                "• 🎥 Un video senza tagli dell’apertura del pacco\n\n"
                "⚠️ In entrambi i video devono essere mostrati tutti i lati del pacco, per verificare che non sia stato manomesso.\n\n"
                "🔐 In caso di pacco manomesso/rubato dal corriere non ci sarà nessun rimborso o rispedizione a meno che non si ha pagato la fee di 30€ per spedizione stealth."
            )
            sent = await context.bot.send_message(chat_id=cid, text=payments_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d == "contact":
            kb = [
                [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
            ]
            sent = await context.bot.send_message(chat_id=cid, text="👥 *CONTATTAMI*\n\nClicca il pulsante qui sotto per contattarmi direttamente su Telegram:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d == "developer":
            kb = [
                [InlineKeyboardButton("✉️ Contattami su Telegram", url="https://t.me/ItalianEdibles")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
            ]
            sent = await context.bot.send_message(chat_id=cid, text="👨‍💻 *DEVELOPER*\n\nBot sviluppato da @ItalianEdibles\n\nContattami per progetti personalizzati!", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d in ["products", "back_to_products"]:
            kb = [
                [InlineKeyboardButton(self.products["1"]["name"], callback_data="product_1")],
                [InlineKeyboardButton(self.products["2"]["name"], callback_data="product_2")],
                [InlineKeyboardButton("Caramelle THC 🇪🇸 - Formato 10", callback_data="product_3_10"),
                 InlineKeyboardButton("Caramelle THC 🇪🇸 - Formato 20", callback_data="product_3_20")],
                [InlineKeyboardButton(self.products["4"]["name"], callback_data="product_4")],
                [InlineKeyboardButton(self.products["5"]["name"], callback_data="product_5")],
                [InlineKeyboardButton(self.products["6"]["name"], callback_data="product_6")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]
            ]
            sent = await context.bot.send_message(chat_id=cid, text="📱 *PRODOTTI DISPONIBILI*\n\nScegli un prodotto:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d in ["services", "back_to_services"]:
            kb = [[InlineKeyboardButton(s["name"], callback_data=f"service_{sid}")] for sid, s in self.services.items()] + [[InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]]
            sent = await context.bot.send_message(chat_id=cid, text="🔧 *SERVIZI DISPONIBILI*\n\nScegli un servizio:", reply_markup=InlineKeyboardMarkup(kb), parse_mode=ParseMode.MARKDOWN)
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d.startswith("product_3_"):
            k = d.replace("product_", "")
            p = self.products.get(k)
            if not p:
                await q.answer("❌ Prodotto non trovato!")
                return
            try:
                sent = await context.bot.send_video(chat_id=cid, video=p["video_file_id"], caption=p["caption"], parse_mode=ParseMode.MARKDOWN, supports_streaming=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            except BadRequest:
                sent = await context.bot.send_message(chat_id=cid, text=p["caption"], parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d == "product_5":
            p = self.products["5"]
            try:
                sent = await context.bot.send_video(chat_id=cid, video=p["video_file_id"], caption=p["caption"], parse_mode=ParseMode.MARKDOWN, supports_streaming=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            except BadRequest:
                sent = await context.bot.send_message(chat_id=cid, text=p["caption"], parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d == "product_6":
            p = self.products["6"]
            try:
                sent = await context.bot.send_video(chat_id=cid, video=p["video_file_id"], caption=p["caption"], parse_mode=ParseMode.MARKDOWN, supports_streaming=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            except BadRequest:
                sent = await context.bot.send_message(chat_id=cid, text=p["caption"], parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d in ["product_1", "product_2"]:
            pid = d.split("_")[1]
            p = self.products.get(pid)
            if not p:
                await q.answer("❌ Prodotto non trovato!")
                return
            caption = f"📦 *{p['name']}*\n💵 Prezzo:\n{p['price']}\n📝 Descrizione: {p['description']}"
            try:
                sent = await context.bot.send_video(chat_id=cid, video=p["video_file_id"], caption=caption, parse_mode=ParseMode.MARKDOWN, supports_streaming=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            except BadRequest:
                sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d == "product_4":
            p = self.products["4"]
            caption = f"📦 *{p['name']}*\n💵 Prezzo:\n{p['price']}\n📝 Descrizione: {p['description']}\n\n*{p['special_note']}*"
            try:
                sent = await context.bot.send_video(chat_id=cid, video=p["video_file_id"], caption=caption, parse_mode=ParseMode.MARKDOWN, supports_streaming=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            except BadRequest:
                sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            return
        if d.startswith("service_"):
            sid = d.split("_")[1]
            s = self.services.get(sid)
            if not s:
                await q.answer("❌ Servizio non trovato!")
                return
            caption = f"🛠️ *{s['name']}*\n💵 Prezzo:\n{s['price']}\n📝 Descrizione: {s['description']}"
            if s.get("video_file_id"):
                try:
                    sent = await context.bot.send_video(chat_id=cid, video=s["video_file_id"], caption=caption, parse_mode=ParseMode.MARKDOWN, supports_streaming=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]))
                    context.user_data["last_menu_msg_id"] = sent.message_id
                except BadRequest:
                    sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]))
                    context.user_data["last_menu_msg_id"] = sent.message_id
            elif s.get("photo_file_id"):
                try:
                    sent = await context.bot.send_photo(chat_id=cid, photo=s["photo_file_id"], caption=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]))
                    context.user_data["last_menu_msg_id"] = sent.message_id
                except BadRequest:
                    sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]))
                    context.user_data["last_menu_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Servizi", callback_data="back_to_services")]]))
                context.user_data["last_menu_msg_id"] = sent.message_id
            return

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        m = update.effective_message
        if m.from_user and m.from_user.id == ADMIN_USER_ID:
            if m.video:
                await m.reply_text(f"File ID del video:\n<code>{m.video.file_id}</code>", parse_mode=ParseMode.HTML)
                return
            if m.photo:
                await m.reply_text(f"File ID della foto:\n<code>{m.photo[-1].file_id}</code>", parse_mode=ParseMode.HTML)
                return
        t = m.text.lower() if m.text else ""
        if any(w in t for w in ["ciao", "salve"]):
            await m.reply_text("Ciao! 👋 Usa /start per iniziare.")
        elif "aiuto" in t or "help" in t:
            await m.reply_text("Usa /start per vedere il menu principale.")
        else:
            await m.reply_text("Non ho capito. Usa /start per vedere le opzioni disponibili.")

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
