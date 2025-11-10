import os, sys, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.error import BadRequest

# ───────────────────────── CONFIG ───────────────────────── #
BOT_TOKEN         = os.getenv("BOT_TOKEN")
ADMIN_USER_ID     = 6840588025
ADMIN_CONTACT     = "https://t.me/RegularDope"

WELCOME_IMAGE_URL = ""
WELCOME_TEXT = (
    "Benvenuto da Regular Dope!\n"
    "Un’esperienza pensata per farti rilassare, senza preoccupazioni né stress.\n"
    "Scopri un mondo di prodotti selezionati attraverso questa pratica vetrina e inizia l’avventura con /start."
)
TOS_TEXT = (
    "COME ORDINARE\n\n"
    "Per effettuare un ordine, scrivi a @RegularDope e compila la seguente scheda:\n\n"
    "INFORMAZIONI ORDINE:\n"
    "• Username Telegram\n"
    "• Prodotto/i\n"
    "• Quantità\n"
    "• Metodo di pagamento scelto\n\n"
    "INFORMAZIONI SPEDIZIONE:\n"
    "• Nome e Cognome\n"
    "• Num di Tel / Email\n"
    "• Indirizzo o punto di ritiro\n"
    "• Eventuali note o richieste speciali\n"
    "(Il nome e cognome non deve essere per forza reale.)\n\n"
    "POLITICA DI RESHIP E ASSISTENZA\n\n"
    "In caso di pacco smarrito in transito con valore inferiore a 150 €, è prevista automaticamente la piena rispedizione del materiale, se possibile, oppure il rimborso.\n\n"
    "Per resi o problemi sul prodotto è obbligatorio fornire:\n"
    "• Un video senza tagli dell’apertura del locker\n"
    "• Un video senza tagli dell’apertura del pacco\n\n"
    "In entrambi i video devono essere mostrati tutti i lati del pacco per verificare che non sia stato manomesso.\n\n"
    "In caso di pacco smarrito in transito con valore superiore a 150 €, è previsto automaticamente un rimborso o una rispedizione del 25%, a meno che non venga pagata un’assicurazione proporzionale al valore dell’ordine, che garantisce un rimborso o una rispedizione completa."
)
PAGAMENTI_TEXT = (
    "METODI DI PAGAMENTO\n\n"
    "• Bonifico istantaneo (0% commissione)\n"
    "• Crypto LTC / BTC (0% commissione)\n"
    "• Carta di credito/debito (10% commissione)\n"
    "• Contanti spediti (+5 €)\n"
    "• PayPal / Satispay (10% commissione)\n"
    "• Bonifico dal tabacchino (0% commissione)\n"
    "• Gift card crypto (Bitnovo, ecc.) (+10% commissione)\n"
    "• Buoni regalo (Amazon, ecc.) (+50% commissione)\n\n"
    "COSTO SPEDIZIONE:\n"
    "• Inpost 5€\n"
    "• Altri corrieri 10€"
)

# ──────────────────────── BOT DATA ──────────────────────── #

class ShopBot:
    def __init__(self):
        # --- (Any layout with file ID can be changed live by admin) --- #
        self.products = {
            "packwoods": {
                "name": "THC Vapes Packwoods™ x Runtz",
                "price": (
                    "1 - 45\n"
                    "2 - 80\n"
                    "3 - 120\n"
                    "4 - 145\n"
                    "5 - 160\n"
                    "10 - 300\n"
                    "12 - 350\n"
                    "20 - 550"
                ),
                "description": "Con 1000 mg di distillato Delta-9 THC in ogni pennetta, basta una dozzina di tiri per sentire un effetto potente e duraturo.",
                "video_file_id": "",  # Fill as needed
            },
        }
        self.categories = {
            "dry": [
                # Insert products for DRY later
            ],
            "weed": [
                # Insert products for WEED later
            ]
        }
        self.user_ids = set()

    async def _relay_to_admin(self, context, who, what):
        message = f"👤 {who.full_name} ({who.id})\n💬 {what}"
        logger.info(message)
        try:
            await context.bot.send_message(ADMIN_USER_ID, message)
        except Exception as e:
            logger.warning(f"Failed to relay to admin: {e}")

    async def delete_last_menu(self, context, chat_id):
        msg_id = context.user_data.get("last_menu_msg_id")
        if msg_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
            context.user_data["last_menu_msg_id"] = None

    # ──────────────────────────  COMMANDS  ────────────────────────── #
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.user_ids.add(update.effective_user.id)
        await self.delete_last_menu(context, update.effective_chat.id)

        kb = [
            [InlineKeyboardButton("🛍️ SHOP", callback_data="shop")],
            [InlineKeyboardButton("💳 PAGAMENTI", callback_data="pagamenti")],
            [InlineKeyboardButton("📜 T.O.S.", callback_data="tos")],
            [InlineKeyboardButton("📦 ORDINA QUI", url=ADMIN_CONTACT)],
            [InlineKeyboardButton("💬 CHAT CLIENTI", callback_data="chat_clienti")],
        ]
        m = update.effective_message
        try:
            sent = await m.reply_photo(photo=WELCOME_IMAGE_URL, caption=WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
        except BadRequest:
            sent = await m.reply_text(text=WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id

    async def broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_USER_ID:
            await update.message.reply_text("❌ Non sei autorizzato a usare questo comando.")
            return
        if not context.args:
            await update.message.reply_text("❗ Usa correttamente: /broadcast <messaggio>")
            return
        message = " ".join(context.args)
        count = 0
        for uid in list(self.user_ids):
            try:
                await context.bot.send_message(uid, f"📢 {message}")
                count += 1
            except Exception as e:
                logger.warning(f"Impossibile inviare a {uid}: {e}")
        await update.message.reply_text(f"✅ Messaggio inviato a {count} utenti.")

    # ──────────────────────────  CALLBACKS  ────────────────────────── #
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        q   = update.callback_query
        d   = q.data
        cid = q.message.chat.id
        self.user_ids.add(update.effective_user.id)
        await q.answer()

        if update.effective_user.id != ADMIN_USER_ID:
            await self._relay_to_admin(context, update.effective_user, f"Pressed button: {d}")
        await self.delete_last_menu(context, cid)

        # Main menu buttons
        if d in ("back_to_main", "main"):
            await self.start(update, context)
            return

        if d == "shop":
            kb = [
                [
                    InlineKeyboardButton("DRY", callback_data="cat_dry"),
                    InlineKeyboardButton("WEED", callback_data="cat_weed")
                ],
                [InlineKeyboardButton("PACKWOODS X RUNTZ", callback_data="prod_packwoods")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="Scegli una categoria:",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "pagamenti":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=PAGAMENTI_TEXT,
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "tos":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=TOS_TEXT,
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "chat_clienti":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="In arrivo!",
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # --- Category lists (empty for now) --- #
        if d in ("cat_dry", "cat_weed"):
            cat = "dry" if d == "cat_dry" else "weed"
            prods = self.categories.get(cat, [])
            kb = [
                [InlineKeyboardButton(p["name"], callback_data=f"prod_{cat}_{i}")]
                for i, p in enumerate(prods)
            ] + [[InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]]
            txt = "Nessun prodotto disponibile." if not prods else "Scegli un prodotto:"
            sent = await context.bot.send_message(
                chat_id=cid,
                text=txt,
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # PACKWOODS direct
        if d == "prod_packwoods":
            prod = self.products["packwoods"]
            caption = f"📦 *{prod['name']}*\n💵 Prezzo:\n{prod['price']}\n📝 Descrizione: {prod['description']}"
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]]
            if prod.get("video_file_id"):
                try:
                    sent = await context.bot.send_video(
                        chat_id=cid,
                        video=prod["video_file_id"],
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        supports_streaming=True,
                        reply_markup=InlineKeyboardMarkup(kb)
                    )
                    context.user_data["last_menu_msg_id"] = sent.message_id
                except BadRequest:
                    sent = await context.bot.send_message(
                        chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb)
                    )
                    context.user_data["last_menu_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(
                    chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb)
                )
                context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # Category products (expand as needed, keeping admin features)
        if d.startswith("prod_dry_") or d.startswith("prod_weed_"):
            cat = "dry" if d.startswith("prod_dry_") else "weed"
            idx = int(d.rsplit("_", 1)[1])
            prods = self.categories.get(cat, [])
            if 0 <= idx < len(prods):
                prod = prods[idx]
                caption = prod["caption"] if "caption" in prod and prod["caption"] else f"📦 *{prod['name']}*"
                kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data=f"cat_{cat}")]]
                if prod.get("video_file_id"):
                    try:
                        sent = await context.bot.send_video(
                            chat_id=cid,
                            video=prod["video_file_id"],
                            caption=caption,
                            parse_mode=ParseMode.MARKDOWN,
                            supports_streaming=True,
                            reply_markup=InlineKeyboardMarkup(kb)
                        )
                        context.user_data["last_menu_msg_id"] = sent.message_id
                    except BadRequest:
                        sent = await context.bot.send_message(
                            chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb)
                        )
                        context.user_data["last_menu_msg_id"] = sent.message_id
                else:
                    sent = await context.bot.send_message(
                        chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb)
                    )
                    context.user_data["last_menu_msg_id"] = sent.message_id
            else:
                await q.answer("❌ Prodotto non trovato!")
            return

    # ──────────────────────── MESSAGES ──────────────────────── #
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        m   = update.effective_message
        usr = update.effective_user
        self.user_ids.add(usr.id)
        if usr and usr.id != ADMIN_USER_ID:
            txt = (
                m.text or m.caption or
                (f"<{type(m.effective_attachment).__name__}>" if m.effective_attachment else "<no text>")
            )
            await self._relay_to_admin(context, usr, txt)
        if usr and usr.id == ADMIN_USER_ID:
            if m.video:
                await m.reply_text(f"File ID del video:\n<code>{m.video.file_id}</code>", parse_mode=ParseMode.HTML); return
            if m.photo:
                await m.reply_text(f"File ID della foto:\n<code>{m.photo[-1].file_id}</code>", parse_mode=ParseMode.HTML); return
        t = m.text.lower() if m.text else ""
        if any(w in t for w in ("ciao", "salve")):
            await m.reply_text("Ciao! 👋 Usa /start per iniziare.")
        elif "aiuto" in t or "help" in t:
            await m.reply_text("Usa /start per vedere il menu principale.")
        else:
            await m.reply_text("Non ho capito. Usa /start per vedere le opzioni disponibili.")

# ────────────────────────── MAIN ────────────────────────── #
def main():
    logger.info("Avvio del bot...")
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        bot = ShopBot()
        app.add_handler(CommandHandler("start", bot.start))
        app.add_handler(CommandHandler("broadcast", bot.broadcast))
        app.add_handler(CallbackQueryHandler(bot.button_handler))
        app.add_handler(MessageHandler(filters.ALL, bot.handle_message))
        app.run_polling()
        logger.info("Bot terminato.")
    except Exception as e:
        logger.exception(f"❌ Errore critico: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()
