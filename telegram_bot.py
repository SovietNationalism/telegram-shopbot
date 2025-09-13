import os, sys, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.error import BadRequest

# ─────────────────────────  CONFIG  ───────────────────────── #

BOT_TOKEN         = os.getenv("BOT_TOKEN")
ADMIN_USER_ID     = 6840588025
WELCOME_IMAGE_URL = "https://i.postimg.cc/pr65RVVm/D6-F1-EDE3-E7-E8-4-ADC-AAFC-5-FB67-F86-BDE3.png"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
if not BOT_TOKEN:
    logger.critical("❌ BOT_TOKEN missing."); sys.exit(1)

# ─────────────────────────  BOT CLASS  ────────────────────── #

class ShopBot:
    def __init__(self):
        # --------------------  PRODUCTS -------------------- #
        self.products = {
            # UPDATED: THC Syrup content and video as requested
            "2": {
                "name": "Sciroppo al THC",
                "price": (
                    "x 1 150 ml 30€\n"
                    "x 2 300 ml 40€\n"
                    "x 5 750 ml 100€\n"
                    "x 10 1,5 l 190€\n"
                    "x 20 3 l 335€"
                ),
                "caption": (
                    "📦 Sciroppo al THC\n"
                    "💵 Prezzo:\n"
                    "x 1 150 ml 30€\n"
                    "x 2 300 ml 40€\n"
                    "x 5 750 ml 100€\n"
                    "x 10 1,5 l 190€\n"
                    "x 20 3 l 335€\n"
                    "📝 Descrizione: PER ORA DISPONIBILE SOLO SENZA L’ETICHETTA DAVANTI CHE DICE THC LEAN.\n"
                    "Composta da estratto di hashish a base di etanolo, emulsionato in uno sciroppo dolce per una stabilità e biodisponibilità superiore.\n"
                    "Da mescolare con qualsiasi tipo di bevanda! Consigliamo liquidi freddi e dolci per coprire il sapore.\n"
                    "Scuotere la boccetta prima di ogni uso per distribuirlo bene.\n"
                    "Gusti: Lampone, Limone\n"
                    "Per un aggiunta di 5€, un sapore a richiesta (es. cola, passion fruit, mela, etc) può essere preparato.\n"
                    "Dosaggio consigliato (2 mg/ml):\n"
                    "🟢 Principianti: 10–15 mg (5–7.5 ml circa)\n"
                    "🟡 Regolari: 25–35 mg (12.5–17.5 ml)\n"
                    "🔴 Esperti: 50 + mg (25 ml e oltre)\n"
                    "Ricordarsi che gli ml non equivalgono ai grammi."
                ),
                "video_file_id": "BAACAgQAAxkBAAKS92i91_6szBR9aZ6JT9zlvdo2IvyaAAJrGwACTNbwUa8t030MeXDoNgQ",
            },
            "4": {
                "name": "THC Vapes Packwoods™ x Runtz",
                "price": "1 - 45\n2 - 80\n3 - 110\n4 - 135\n5 - 160\n10 - 300",
                "description": "Con 1000 mg di distillato Delta-9 THC, basta una decina di tiri per sentire una fattanza potente.",
                "special_note": "DISPONIBILI",
                "video_file_id": "BAACAgQAAxkBAAJt7mihhlxYRspdIzS7kVFyqRg1uFbPAAImHwACprYJUfBkRTR9sNz2NgQ",
            },
            "5": {
                "name": "Brownies al THC",
                "caption": (
                    "DISPONIBILE\n\n"
                    "📦 *THC Brownies*\n"
                    "💵 Prezzo:\n1pz 10€\n2pz 15€\n5pz 35€\n10pz 65€\n20pz 120€\n50pz 280€\n\n"
                    "📝 Descrizione: Brownie al cioccolato con 50 mg di THC per pezzo, preparato "
                    "con burro infuso e lecitina per un effetto potente e ben bilanciato.\n"
                    "*Offerta limitata*: Se aggiungi un singolo brownie a un ordine di min. 25€, "
                    "ti costerà solo 5€ invece che 10€.\n\n"
                    "⚠️ Non consumate l’intero brownie (a meno che non abbiate una tolleranza alta).\n"
                    "Ogni brownie contiene 50 mg di THC; consigliamo di dividerlo con un amico o "
                    "conservarne metà per dopo.\n"
                    "💡 Pro tip: Scaldatelo nel microonde per 10–20 s prima di mangiarlo: sarà caldo "
                    "e ancora più buono!"
                ),
                "video_file_id": "BAACAgQAAxkBAAICzmhucsfJasY9h-D9-mTSUhFTYGisAAIcGgACeZJxUyMtK0Venf2aNgQ",
            },
            # Existing product kept as-is
            "9": {
                "name": "Filtrato Bufalo Plein",
                "caption": (
                    "📦 *DRY BUFALO PLEIN*\n"
                    "💵 Prezzo:\n"
                    "3g 30€\n5g 40€\n10g 75€\n15g 110€\n20g 140€\n25g 165€\n30g 200€\n50g 270€\n70g 350€\n100g 480€\n\n"
                    "📝 Descrizione: Ancora tenuto perfettamente, fumo di alta qualità ottimo per lavorare e da fumare, "
                    "sapore e botta intensa, un piacere da smistare."
                ),
                "video_file_id": "BAACAgQAAxkBAAKOtGi7QV3uU9iIQ3u2I-88q5Z1pg0WAALxGQACDXjZUUMGZqldPRkPNgQ",
            },
            # NEW PRODUCT: Citronella Kush 🍋 (with new prices/video and description)
            "10": {
                "name": "Citronella Kush",
                "caption": (
                    "📦 *Citronella Kush 🍋*\n"
                    "💵 Prezzo:\n"
                    "3.5 35€\n"
                    "5g 45€\n"
                    "8g 70€\n"
                    "10g 80€\n"
                    "15g 120€\n"
                    "28g 190€\n"
                    "40g 265€\n"
                    "50g 315 ➡️ 300€\n"
                    "70g 420 ➡️ 390€\n"
                    "100g 525 ➡️ 500€\n\n"
                    "📝 Descrizione: Una Calispain con genetica agrumata con note fresche e potenti. Fiori densi, ricchi di resina e molto appiccicosi. Effetto potente e duraturo, si distingue subito per qualità e intensità. DISPONIBILE."
                ),
                "video_file_id": "BAACAgQAAxkBAAKS62i91dzcV9hhhs-3exRZUUW_b3IsAAJoGwACTNbwUT6DVkPtLa1vNgQ",
            },
            # NEW PRODUCT: 500mg THC gummies 🍬
            "11": {
                "name": "Caramelle 500mg THC",
                "caption": (
                    "📦 *500mg THC gummies 🍬*\n"
                    "💵 Prezzo:\n"
                    "1 - 30\n"
                    "2 - 45\n"
                    "3 - 65\n"
                    "5 - 100\n"
                    "10 - 180\n\n"
                    "📝 Descrizione: Caramelle gommose in formato da 20 caramelle da 25 mg l’una. Effetto piacevole, rilassante e duraturo, molto divertenti e comode da consumare."
                ),
                "video_file_id": "BAACAgQAAxkBAAKS7Wi91fNzDA7W1_75bX38S9FEikHmAAJpGwACTNbwUW7wVWvB8GnfNgQ",
            },
            # NEW PRODUCT: PROMO CLIENTI (as a product entry)
            "12": {
                "name": "Promo sconto",
                "caption": (
                    "📦 *PROMO CLIENTI*\n\n"
                    "Vuoi fumare GRATIS? Ti basta portare clienti!\n"
                    "Ogni volta che un tuo amico compra da noi, tu guadagni!\n\n"
                    "Come funziona:\n"
                    "1️⃣ Invita un amico a ordinare da noi.\n"
                    "2️⃣ Quando compra, ci dice che lo hai inviato TU.\n"
                    "3️⃣ Tu guadagni subito 1g gratis di erba o hash (o 5€ di credito per gli altri prodotti) ogni volta che spende 40€.\n\n"
                    "Regole:\n"
                    "Il cliente deve comunicare il tuo @username al momento dell’ordine.\n"
                    "Se preferisci, puoi accumulare i crediti e spenderli quando vuoi.\n"
                    "I crediti valgono per qualsiasi altro prodotto (vape, edibili, sciroppi).\n\n"
                    "ALTRE OFFERTE \n"
                    "VALIDO FINO AL 12/01\n"
                    "10g dry + 1 THC Lean = 95\n"
                    "10g dry + 2 THC Lean = 105"
                ),
                "video_file_id": None
            },
        }

        # --------------------  ALTRO (ex-Servizi) -------------------- #
        self.services = {
            "1": {
                "name": "Creazione Bot Telegram",
                "price": "€35/m",
                "description": "Sei un venditore o comunque sei interessato alla creazione di un bot simile? Posso aiutarti.",
                "photo_file_id": "AgACAgQAAxkBAAIBVmY0n9f5v1cAAQ1nUuH4QnX8h3QjAAJ8tzEbJ2FTkJ7yK5y1vN2BAAMCAANzAAMvBA",
            },
            "2": {
                "name": "Tabaccheria",
                "price": (
                    "Juicy Jay’s Hemp Wraps – Red Alert\n"
                    "1 pacchetto 2€\n5 pacchetti 8.50€\n10 pacchetti 14.50€\n20 pacchetti 22€\n\n"
                    "⸻\n\n"
                    "RAW Cartine King Size Slim\n"
                    "1 cartina 1.20€\n5 cartine 5€\n10 cartine 8.50€\n25 cartine 20€\n\n"
                    "⸻\n\n"
                    "RAW Filtri Perforated Wide\n"
                    "1 pacchetto 1€\n5 pacchetti 4€\n10 pacchetti 7€\n25 pacchetti 15€\n\n"
                    "⸻\n\n"
                    "Kit RAW (cartine + filtri)\n"
                    "1 kit 1.80€\n5 kit 8€\n10 kit 15€\n25 kit 33.50€"
                ),
                "description": "Articoli da tabaccheria e rolling: wraps, cartine, filtri e kit RAW.",
                "video_file_id": "BAACAgQAAxkBAAJeEmiYv5PRrUWVT9DjsyUrMCVJEwr8AAJFHAACOErJUPkmL_O8v3O_NgQ",
            }
        }

        # Track users for broadcast (kept as in prior code)
        self.user_ids = set()

        # ------------------  REGOLAMENTO  ------------------ #
        self.rules_text = (
            "📦 Spedizioni in tutta Italia\n"
            "1. Scrivici in privato indicando prodotto, quantità e modalità di pagamento.\n"
            "2. Riceverai conferma con prezzo.\n"
            "3. Consegna rapida e gratuita (salvo eccezioni) tramite InPost o corriere a scelta.\n\n"
            "⸻\n\n"
            "🤝 Meet-up a Mantova / Consegna a mano\n"
            "Per sicurezza reciproca, i meet-up seguono regole precise. Se non le accetti, non si procede.\n\n"
            "🔍 Verifica obbligatoria (solo per meet-up)\n"
            "Per essere verificato invia:\n"
            "• Foto della tua carta d’identità (anche retro)\n"
            "• Foto di te con la somma in mano\n"
            "• Screenshot del tuo profilo Instagram attivo\n\n"
            "⚠️ Nessun meet-up sarà confermato senza verifica. La ragione di queste verifiche è prevenire rapine, "
            "perdite di tempo, ecc. A fine transazione tutto verrà eliminato per la vostra sicurezza.\n\n"
            "📋 Regole meet-up / delivery\n"
            "• Presentati da solo. Se porti qualcuno, deve essere verificato anche lui.\n"
            "• Contanti già contati e giusti, non garantiamo resto.\n"
            "• Si mostra e conta la somma prima del prodotto.\n"
            "• Il luogo lo scelgo io. Orario concordato in anticipo.\n"
            "• Nessuna tolleranza per perditempo o comportamenti sospetti.\n"
            "• Il rider è sempre armato. Non ci pensate nemmeno.\n\n"
            "⸻\n\n"
            "🚗 Delivery su Città Limitrofe\n\n"
            "Ordine minimo 50€\n"
            "Zone vicine a Mantova (entro 15 km) – 15/20€.\n"
            "Verona – 25€\n"
            "Brescia – 30€\n"
            "Modena – 25€\n"
            "Cremona – 35€\n"
            "Reggio Emilia – 35€\n"
            "Carpi – 30€\n"
            "Parma – 35€"
        )

    # ────────────────────  HELPER: relay  ─────────────────── #
    async def _relay_to_admin(self, context: ContextTypes.DEFAULT_TYPE, who, what: str) -> None:
        message = f"👤 {who.full_name} ({who.id})\n💬 {what}"
        logger.info(message)
        try:
            await context.bot.send_message(ADMIN_USER_ID, message)
        except Exception as e:
            logger.warning(f"Failed to relay to admin: {e}")

    # ────────────────────────  COMMANDS  ──────────────────────── #
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.user_ids.add(update.effective_user.id)
        await self.delete_last_menu(context, update.effective_chat.id)

        kb = [
            [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data="shop")],
            [InlineKeyboardButton("💬 Chat Clienti 💬", url="https://t.me/+a3rvmx13cjo5MjE0")],
            [InlineKeyboardButton("💰 Pagamenti 💰", callback_data="payments")],
            [InlineKeyboardButton("📋 Regolamento 📋", callback_data="rules")],
            [InlineKeyboardButton("📢 Canale Telegram 📢", url="https://t.me/+A3JnK9ALAmtiMjBk")],
            [InlineKeyboardButton("👥 Contattami 👥", callback_data="contact")],
            [InlineKeyboardButton("👨‍💻 Developer 👨‍💻", callback_data="developer")],
        ]
        msg = (
            "🎉 Benvenuto sul bot Vetrina ItalianEdibles! 🇮🇹\n\n"
            "Scopri un mondo di prodotti selezionati, pensati per un'esperienza unica e "
            "indimenticabile. Puoi esplorare e contattarci in pochi semplici clic!"
        )
        m = update.effective_message
        try:
            sent = await m.reply_photo(photo=WELCOME_IMAGE_URL, caption=msg, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
        except BadRequest:
            sent = await m.reply_text(text=msg, reply_markup=InlineKeyboardMarkup(kb))
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

    async def delete_last_menu(self, context, chat_id):
        msg_id = context.user_data.get("last_menu_msg_id")
        if msg_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
            context.user_data["last_menu_msg_id"] = None

    # ────────────────────────  CALLBACKS  ──────────────────────── #
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        q   = update.callback_query
        d   = q.data
        cid = q.message.chat.id
        self.user_ids.add(update.effective_user.id)

        await q.answer()

        if update.effective_user.id != ADMIN_USER_ID:
            await self._relay_to_admin(context, update.effective_user, f"Pressed button: {d}")

        await self.delete_last_menu(context, cid)

        # ---------- REGOLAMENTO ---------- #
        if d == "rules":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            sent = await context.bot.send_message(chat_id=cid, text=self.rules_text, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---------- TORNA AL MAIN ---------- #
        if d == "back_to_main":
            await self.start(update, context)
            return

        # ---------- SHOP ---------- #
        if d == "shop":
            kb = [
                [InlineKeyboardButton("📱 Prodotti", callback_data="products")],
                [InlineKeyboardButton("🔧 Altro", callback_data="services")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")],
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="🛍️ *SHOP*\n\nScegli una categoria:",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---------- PAGAMENTI ---------- #
        if d == "payments":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            payments_text = (
                "💰 *METODI DI PAGAMENTO*\n\n"
                "• 🏦 Bonifico istantaneo (0% commissione)\n"
                "• 📲 Hype / Revolut / Sumup / Tinaba (0% commissione)\n"
                "• 💸 Crypto LTC / BTC (-5% commissione)\n"
                "• 💶 Contanti spediti o in meet up (0% commissione)\n"
                "• 💳 PayPal / Satispay (+10% commissione)\n"
                "• 💼 Bonifico dal tabacchino (+10% commissione)\n"
                "• ✉️ Gift card prepagate/crypto (Bitnovo, Epipoli, Paysafecard, etc...) (+10% commissione)\n"
                "• 🏷️ Buoni regalo (+50% commissione)\n\n"
                "📦 *POLITICA DI RESHIP E ASSISTENZA*\n\n"
                "In caso di pacco smarrito in transito è previsto il rimborso o rispedizione del materiale.\n"
                "Per resi o problemi sul prodotto, è obbligatorio fornire:\n"
                "• 🎥 Un video senza tagli dell’apertura del locker\n"
                "• 🎥 Un video senza tagli dell’apertura del pacco\n\n"
                "⚠️ In entrambi i video devono essere mostrati tutti i lati del pacco, per verificare che non sia stato manomesso.\n\n"
            )
            sent = await context.bot.send_message(
                chat_id=cid,
                text=payments_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---------- CONTACT / DEVELOPER ---------- #
        if d in ("contact", "developer"):
            txt = (
                "👥 *CONTATTAMI*\n\nClicca il pulsante qui sotto per contattarmi direttamente su Telegram:"
                if d == "contact"
                else "👨‍💻 *DEVELOPER*\n\nBot sviluppato da @ItalianEdibles\n\nContattami per progetti personalizzati!"
            )
            kb = [
                [InlineKeyboardButton("✉️ Scrivimi", url="https://t.me/ItalianEdibles")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
            ]
            sent = await context.bot.send_message(chat_id=cid, text=txt, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---------- LISTA PRODOTTI ---------- #
        if d in ("products", "back_to_products"):
            kb = [
                [InlineKeyboardButton(self.products["2"]["name"], callback_data="product_2")],
                [InlineKeyboardButton(self.products["4"]["name"], callback_data="product_4")],
                [InlineKeyboardButton(self.products["5"]["name"], callback_data="product_5")],
                [InlineKeyboardButton(self.products["9"]["name"], callback_data="product_9")],
                [InlineKeyboardButton(self.products["10"]["name"], callback_data="product_10")],
                [InlineKeyboardButton(self.products["11"]["name"], callback_data="product_11")],
                [InlineKeyboardButton(self.products["12"]["name"], callback_data="product_12")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="📱 *PRODOTTI DISPONIBILI*\n\nScegli un prodotto:",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---------- LISTA ALTRO ---------- #
        if d in ("services", "back_to_services"):
            kb = [
                [InlineKeyboardButton(s["name"], callback_data=f"service_{sid}")]
                for sid, s in self.services.items()
            ] + [[InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="🔧 *ALTRO*\n\nScegli un elemento:",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---------- DETTAGLIO SINGOLO PRODOTTO ---------- #
        if d.startswith("product_"):
            key = d.split("_", 1)[1]
            prod = self.products.get(key)
            if not prod:
                await q.answer("❌ Prodotto non trovato!")
                return

            if "caption" in prod and prod["caption"]:
                caption = prod["caption"]
            elif key == "4":
                caption = (
                    f"📦 *{prod['name']}*\n"
                    f"💵 Prezzo:\n{prod['price']}\n"
                    f"📝 Descrizione: {prod['description']}\n\n"
                    f"*{prod['special_note']}*"
                )
            else:
                caption = (
                    f"📦 *{prod['name']}*\n"
                    f"💵 Prezzo:\n{prod.get('price','')}\n"
                    f"📝 Descrizione: {prod.get('description','')}"
                )

            kb_back = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ai Prodotti", callback_data="back_to_products")]])

            if prod.get("video_file_id"):
                try:
                    sent = await context.bot.send_video(chat_id=cid, video=prod["video_file_id"], caption=caption,
                                                        parse_mode=ParseMode.MARKDOWN, supports_streaming=True,
                                                        reply_markup=kb_back)
                    context.user_data["last_menu_msg_id"] = sent.message_id
                except BadRequest:
                    sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN,
                                                          reply_markup=kb_back)
                    context.user_data["last_menu_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN,
                                                      reply_markup=kb_back)
                context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---------- DETTAGLIO ALTRO ---------- #
        if d.startswith("service_"):
            sid = d.split("_", 1)[1]
            serv = self.services.get(sid)
            if not serv:
                await q.answer("❌ Elemento non trovato!")
                return

            caption = f"🛠️ *{serv['name']}*\n💵 Prezzo:\n{serv['price']}\n📝 Descrizione: {serv['description']}"
            kb_back = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Torna ad Altro", callback_data="back_to_services")]])

            if serv.get("video_file_id"):
                try:
                    sent = await context.bot.send_video(chat_id=cid, video=serv["video_file_id"], caption=caption,
                                                        parse_mode=ParseMode.MARKDOWN, supports_streaming=True,
                                                        reply_markup=kb_back)
                    context.user_data["last_menu_msg_id"] = sent.message_id
                except BadRequest:
                    if serv.get("photo_file_id"):
                        try:
                            sent = await context.bot.send_photo(chat_id=cid, photo=serv["photo_file_id"], caption=caption,
                                                                parse_mode=ParseMode.MARKDOWN, reply_markup=kb_back)
                            context.user_data["last_menu_msg_id"] = sent.message_id
                        except BadRequest:
                            sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN,
                                                                  reply_markup=kb_back)
                            context.user_data["last_menu_msg_id"] = sent.message_id
                    else:
                        sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN,
                                                              reply_markup=kb_back)
                        context.user_data["last_menu_msg_id"] = sent.message_id
            elif serv.get("photo_file_id"):
                try:
                    sent = await context.bot.send_photo(chat_id=cid, photo=serv["photo_file_id"], caption=caption,
                                                        parse_mode=ParseMode.MARKDOWN, reply_markup=kb_back)
                    context.user_data["last_menu_msg_id"] = sent.message_id
                except BadRequest:
                    sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN,
                                                          reply_markup=kb_back)
                    context.user_data["last_menu_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN,
                                                      reply_markup=kb_back)
                context.user_data["last_menu_msg_id"] = sent.message_id
            return

    # ────────────────────────  MESSAGES  ──────────────────────── #
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

# ──────────────────────────  MAIN  ────────────────────────── #
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