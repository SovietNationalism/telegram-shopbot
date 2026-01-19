import os, sys, logging, json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.error import BadRequest
from pathlib import Path

# ───────────────────────── CONFIG ───────────────────────── #
BOT_TOKEN         = os.getenv("BOT_TOKEN")
ADMIN_USER_ID     = 8219761049
ADMIN_CONTACT     = "https://t.me/RegularDope"
REQUIRED_GROUP_ID = -1003514626970  # put the actual group ID here
REQUIRED_GROUP_LINK = "https://t.me/+xwCcckoNERw2MWU0"
USERS_FILE = "users.json"
SUGGESTIONS_FILE = "suggestions.json"

WELCOME_IMAGE_URL = "https://i.postimg.cc/5yBdW1BK/IMG-0466.jpg"
WELCOME_TEXT = (
    "Benvenuto da Regular Dope!\n"
    "Un’esperienza pensata per farti rilassare, senza preoccupazioni né stress.\n"
    "Scopri un mondo di prodotti selezionati. Controlla ogni bottone!"
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
    "(Il nome e cognome non deve essere per forza reale.)\n"
)

TOS_TERMS_TEXT = (
    "POLITICA DI RESHIP E ASSISTENZA\n\n"
    "In caso di pacco smarrito in transito con valore inferiore a 150 €, è prevista automaticamente la piena rispedizione del materiale, se possibile, oppure il rimborso.\n\n"
    "Per resi o problemi sul prodotto è obbligatorio fornire:\n"
    "• Un video senza tagli dell’apertura del locker\n"
    "• Un video senza tagli dell’apertura del pacco\n\n"
    "In entrambi i video devono essere mostrati tutti i lati del pacco per verificare che non sia stato manomesso."
)

PAGAMENTI_TEXT = (
    "METODI DI PAGAMENTO\n\n"
    "• Bonifico istantaneo (0% commissione)\n"
    "• Crypto LTC / BTC (0% commissione)\n"
    "• Contanti spediti (+5 €)\n"
    "• Bonifico dal tabacchino (0% commissione)\n"
    "• Gift card Bitnovo (+10% commissione)\n"
    "• Buoni regalo (Amazon, ecc.) (+50% commissione)\n\n"
    "COSTO SPEDIZIONE:\n"
    "• Inpost GRATUITA\n"
    "• Altri corrieri 10€\n"
    "Il pacco arriva in 2-3 giorni lavorativi in genere, 3-4 per le isole."
)

# ────────────────── LOGGER SETUP ────────────────── #
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─────────────────────── BOT CLASS ─────────────────────── #
class ShopBot:
    def __init__(self):
        self.products = {
            "packwoods": {
                "name": "THC Vapes Dabwoods™",
                "price": (
                    "1 - 45€\n"
                    "2 - 80€\n"
                    "3 - 115€\n"
                    "4 - 145€\n"
                    "5 - 165€\n"
                    "10 - 300€\n"
                ),
                "description": "Con 1000 mg di distillato Delta-9 THC in ogni pennetta, basta una dozzina di tiri per sentire un effetto potente e duraturo.",
                "video_file_id": "BAACAgQAAxkBAAECyH1pbiqrGG8sR6bpaNlzAbJFgtdGyAAC8xkAApIBcFNkjhQrxUtMRjgE",
                "photo_file_ids": [],
            },
            "funghetti": {
                "caption": (
                    "📦 *Funghi Psylocibe Cubensis*\n"
                    "3.5g 45€\n"
                    "5g 65€\n"
                    "10g 105€\n15g 125€\n20g 160€\n"
                    "Una miscela di varietà classiche e potenti, McKennai, Golden Teacher, e Jedi Mind Fuck.\n"
                    "Effetto profondo e duraturo, ideale per esplorare nuove dimensioni. Disponibili subito per chi cerca un'esperienza "
                    "autentica e coinvolgente.\n"
                    "Dosaggi:\n0.25-1 g effetto lieve | 1-2.5 g effetto medio | 2.5-5 g effetto forte"
                ),
                "video_file_id": "BAACAgQAAxkBAAI9gmk_9B6WfvUiC8Q6FWDumJqt_cZQAALaGgAC3ykBUjFj1UkcKnyCNgQ",  # Fill as needed
                "photo_file_ids": [],
            },
            "sciroppo": {
                "name": "Sciroppo al THC",
                "caption": (
                    "Formato 100 ml 200 mg\n"
                    "x 1 30€\n"
                    "x 2 45€\n"
                    "x 5 80€\n"
                    "x 10 145€\n"
                    "Formato 50 100mg\n"
                    "x 2 - 35€\n"
                    "x 4 - 60€\n"
                    "x 10 - 105€\n\n"
                    "Composta da estratto di hashish a base di etanolo, emulsionato in uno sciroppo al lampone (o ciliega a scelta) per una stabilità e biodisponibilità superiore.\n"
                ),
                "video_file_id": "BAACAgQAAxkBAALA8WlM8ils5hJW6qELQ3rDIHhXlJFOAAKpGgACScdoUvDEPR-NjqSKNgQ",  # metti qui il file_id del video se ce l'hai, altrimenti lascia vuoto
                "photo_file_ids": [],
            },
            "neve": {
                "name": "C0CA",
                "caption": (
                    "📦 *Coca*\n\n"
                    "💵 Prezzi:\n"
                    "1g 70€\n"
                    "2g 135€\n"
                    "5g 260€\n"
                    "10g 450€\n"
                    "20g 820€\n\n"
                    "📝 Descrizione:\n"
                    "Merce sana con purezza del 94/95%, niente merda aggiunta.\n"
                    "Effetto potente e piacevole, qualità notevole dal primo uso."
                ),
                "video_file_id": "BAACAgQAAxkBAAJvOmlGs1caV_VuaAiwlLIXZIqd35FfAAKoHgAC0Tc4UosrKq7yuDT1NgQ",
                "photo_file_ids": [],
            },
        }
        self.categories = {
            "hash": [
                {
                    "name": "Filtered 120u",
                    "caption": (
                        "📦 *Filtrato 120u*\n"
                        "5g 40€\n"
                        "10g 70€\n"
                        "15g 100€\n"
                        "20g 130€\n"
                        "30g 170€\n"
                        "40g 200€\n"
                        "50g 230€\n"
                        "100g 420€\n"
                        "200g 805€\n"
                        "Un dry sift commerciale di buona qualità.\n"
                        "Fumo dall'aroma intenso e naturale, facile da lavorare e piacevole da fumare in ogni modo. Colpisce con una botta potente e duratura, lasciando un effetto rilassante e pulito."
                    ),
                    "video_file_id": "BAACAgQAAxkBAAECjLVpao2jGcI4aklKWAp6J9wnyZ8TyAACsBgAAnNpWFP5FyMj6qMDczgE",
                    "photo_file_ids": [],
                },
                {
                    "name": "Frozen",
                    "caption": (
                        "📦 *Frozen Sift*\n\n"
                        "VIDEO DA VETRATO - Quando arriva il materiale sará fornito curato. Questo Frozen arriva verso il 23-26 gen.\n"
                        "3g 40€\n"
                        "5g 60€\n"
                        "10g 110€\n"
                        "15g 155€\n"
                        "20g 200€\n"
                        "25g 235€\n"
                        "35g 315€\n"
                        "50g 425€\n"
                        "100g 800€"
                    ),
                    "video_file_id": "BAACAgQAAxkBAAECyXdpbi6VuNKXrFW1JGK4YDqGVYnquAAC9RkAApIBcFN_FukpFg1sLTgE",
                    "photo_file_ids": [],
                },
            ],
            "weed": [
                # Add WEED category products here later the same way
            ]
        }
        self.weed_video_file_id = "BAACAgQAAxkBAAEC045pbmuZIYKe8DwaSiFCahi4aTzPrwACJhsAApIBeFOi6C9CEsJSXTgE"
        self.weed_overview = (
            "🌿 *OG KUSH*\n"
            "Out of stock - in arrivo tra il 26 gennaio.\n"
            "Una strain classica, ottima Calispain dall'odore intenso e fresco. Fiori compatti e resinosi, estremamente "
            "appiccicosi al tatto. L’effetto è forte, persistente e si fa notare subito per purezza e carattere.\n\n"
            "5g 40€\n"
            "10g 75€\n"
            "15g 110€\n"
            "20g 135€\n"
            "30g 175€\n"
            "40g 200€\n"
            "50g 235€\n"
            "100g 420€\n"
        )
        self.user_ids = set()
        self.suggestions = []

        # Load persistent data
        try:
            if Path(USERS_FILE).exists():
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.user_ids = set(data)
        except Exception as e:
            logger.warning(f"Could not load {USERS_FILE}: {e}")

        try:
            if Path(SUGGESTIONS_FILE).exists():
                with open(SUGGESTIONS_FILE, "r", encoding="utf-8") as f:
                    self.suggestions = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load {SUGGESTIONS_FILE}: {e}")
            
    def _save_users(self):
        try:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(list(self.user_ids), f)
        except Exception as e:
            logger.warning(f"Could not save {USERS_FILE}: {e}")

    def _save_suggestions(self):
        try:
            with open(SUGGESTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.suggestions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Could not save {SUGGESTIONS_FILE}: {e}")

    async def _relay_to_admin(self, context, who, what):
        message = f"👤 {who.full_name} ({who.id})\n💬 {what}"
        logger.info(message)
        try:
            await context.bot.send_message(ADMIN_USER_ID, message)
        except Exception as e:
            logger.warning(f"Failed to relay to admin: {e}")
    
    async def _ask_to_join_group(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
        text = (
            "Per vedere i prodotti devi prima entrare nel gruppo privato.\n"
            "Unisciti qui e poi torna nel bot."
        )
        kb = [[InlineKeyboardButton("🔑 Entra nel gruppo", url=REQUIRED_GROUP_LINK)],
              [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
        sent = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(kb)
        )
        return sent

    async def _is_member_of_required_group(self, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
        try:
            member = await context.bot.get_chat_member(chat_id=REQUIRED_GROUP_ID, user_id=user_id)
            return member.status in ("member", "administrator", "creator")
        except BadRequest:
            # user not found or bot not in group
            return False
        except Exception as e:
            logger.warning(f"Error checking group membership: {e}")
            return False

    async def delete_last_menu(self, context, chat_id):
        msg_id = context.user_data.get("last_menu_msg_id")
        if msg_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
            context.user_data["last_menu_msg_id"] = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.user_ids.add(update.effective_user.id)
        self._save_users()
        await self.delete_last_menu(context, update.effective_chat.id)
        kb = [
            [InlineKeyboardButton("🛍️ SHOP", callback_data="shop")],
            [InlineKeyboardButton("💳 PAGAMENTI", callback_data="pagamenti")],
            [InlineKeyboardButton("📜 COME ORDINARE", callback_data="tos")],
            [InlineKeyboardButton("📦 ORDINA QUI", url=ADMIN_CONTACT)],
            [InlineKeyboardButton("💬 CHAT CLIENTI", url="https://t.me/+xwCcckoNERw2MWU0")],
            [InlineKeyboardButton("📩 RECENSIONI", url="https://t.me/+mX8bV3BF-otlNDZk")],
            [InlineKeyboardButton("📝 CANALE PRINCIPALE", url="https://t.me/Regular_Dope")],
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

    async def _send_media_or_text(
        self,
        context,
        chat_id,
        caption,
        back_callback,
        video_file_id="",
        photo_file_ids=None,
    ):
        kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data=back_callback)]]
        markup = InlineKeyboardMarkup(kb)

        # Prefer video when available, otherwise try photos, then fall back to text.
        if video_file_id:
            try:
                sent = await context.bot.send_video(
                    chat_id=chat_id,
                    video=video_file_id,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                    supports_streaming=True,
                    reply_markup=markup,
                )
                return sent
            except BadRequest:
                pass

        photo_file_ids = list(photo_file_ids or [])
        if photo_file_ids:
            primary_photo_id, *extra_photo_ids = photo_file_ids
            try:
                sent = await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=primary_photo_id,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=markup,
                )
                for pid in extra_photo_ids:
                    try:
                        await context.bot.send_photo(chat_id=chat_id, photo=pid)
                    except BadRequest:
                        continue
                return sent
            except BadRequest:
                pass

        sent = await context.bot.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=markup,
        )
        return sent
        
    async def _send_product(self, context, cid, caption, photo_id=None, video_id=None, back_callback="shop"):
        """Unified product sender with photo/video fallback"""
        kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data=back_callback)]]
        markup = InlineKeyboardMarkup(kb)
        
        if photo_id:
            try:
                sent = await context.bot.send_photo(
                    chat_id=cid, photo=photo_id, caption=caption,
                    parse_mode=ParseMode.MARKDOWN, reply_markup=markup
                )
                context.user_data["last_menu_msg_id"] = sent.message_id
                return
            except BadRequest:
                pass
        
        if video_id:
            try:
                sent = await context.bot.send_video(
                    chat_id=cid, video=video_id, caption=caption,
                    parse_mode=ParseMode.MARKDOWN, supports_streaming=True, reply_markup=markup
                )
                context.user_data["last_menu_msg_id"] = sent.message_id
                return
            except BadRequest:
                pass
        
        # Fallback to text
        sent = await context.bot.send_message(
            chat_id=cid, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=markup
        )
        context.user_data["last_menu_msg_id"] = sent.message_id
        
    async def _check_membership(self, context, user_id, cid):
        """Check group membership and show join prompt if needed"""
        is_member = await self._is_member_of_required_group(context, user_id)
        if not is_member:
            sent = await self._ask_to_join_group(context, cid)
            context.user_data["last_menu_msg_id"] = sent.message_id
            return False
        return True

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        q = update.callback_query
        d = q.data
        cid = q.message.chat.id
        self.user_ids.add(update.effective_user.id)
        await q.answer()

        if update.effective_user.id != ADMIN_USER_ID:
            await self._relay_to_admin(context, update.effective_user, f"Pressed button: {d}")
        await self.delete_last_menu(context, cid)

        # Main navigation
        if d in ("back_to_main", "main"):
            await self.start(update, context)
            return

        if d == "shop":
            kb = [
                [
                    InlineKeyboardButton("HASH", callback_data="cat_hash"),
                    InlineKeyboardButton("ERBA", callback_data="cat_weed")
                ],
                [
                    InlineKeyboardButton("DABW0ODS", callback_data="prod_packwoods"),
                    InlineKeyboardButton("FUNGHETTI", callback_data="prod_funghetti")
                ],
                [
                    InlineKeyboardButton("SCIROPP0 THC", callback_data="prod_sciroppo"),
                    InlineKeyboardButton("SINTETICO", callback_data="cat_sintetico"),
                ],
                [
                    InlineKeyboardButton("TABACCHERIA", callback_data="cat_tabaccheria"),
                    InlineKeyboardButton("CARAMELLE", callback_data="prod_caramelle"),
                ],
                [
                    InlineKeyboardButton("HAI QUALCHE CONSIGLIO?", callback_data="suggest_product")
                ],
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
            kb = [
                [InlineKeyboardButton("Termini di Servizio", callback_data="tos_terms")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")],
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=TOS_TEXT,
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
            
        if d == "tos_terms":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="tos")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=TOS_TERMS_TEXT,
                reply_markup=InlineKeyboardMarkup(kb),
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
            
        if d == "suggest_product":
            text = (
                "Hai un'idea o un prodotto che vorresti vedere in vetrina?\n\n"
                "Scrivi qui sotto il tuo suggerimento in **un solo messaggio**.\n"
                "Il messaggio verrà inoltrato all'amministratore e salvato nella lista dei suggerimenti."
            )
            context.user_data["awaiting_suggestion"] = True
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "prod_packwoods":
            prod = self.products["packwoods"]
            caption = f"📦 *{prod['name']}*\n💵 Prezzo:\n{prod['price']}\n📝 Descrizione: {prod['description']}"
            await self._send_product(context, cid, caption, video_id=prod["video_file_id"])
            return

        if d == "prod_funghetti":
            prod = self.products["funghetti"]
            await self._send_product(context, cid, prod["caption"], video_id=prod["video_file_id"])
            return
            
        if d == "prod_sciroppo":
            prod = self.products["sciroppo"]
            caption = prod.get("caption", "")
            kb = [
                [InlineKeyboardButton("📘 Consigli D’Uso", callback_data="sciroppo_consigli")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="shop")],
            ]
            markup = InlineKeyboardMarkup(kb)

            if prod.get("video_file_id"):
                try:
                    sent = await context.bot.send_video(
                        chat_id=cid,
                        video=prod["video_file_id"],
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        supports_streaming=True,
                        reply_markup=markup,
                    )
                    context.user_data["last_menu_msg_id"] = sent.message_id
                except BadRequest:
                    sent = await context.bot.send_message(
                        chat_id=cid,
                        text=caption,
                        parse_mode=ParseMode.MARKDOWN,
                        reply_markup=markup,
                    )
                    context.user_data["last_menu_msg_id"] = sent.message_id
            else:
                sent = await context.bot.send_message(
                    chat_id=cid,
                    text=caption,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=markup,
                )
                context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "weed_caliusa_outdoor":
            if not await self._check_membership(context, update.effective_user.id, cid):
                return

            caption = (
                "Grape Haze Caliusa Outdoor\n"
                "In arrivo il 26 gennaio.\n"
                "Bud densi con sfumature violacee e cristalli brillanti, dal profilo terpenico fruttato con note di uva matura"
                "e leggero tocco speziato. Fumata morbida che sprigiona un’energia creativa e un effetto rilassante ed euforico.\n\n"
                "5g 50€\n"
                "10g 85€\n"
                "15g 120€\n"
                "20g 150€\n"
                "30g 210€\n"
                "50g 310€\n"
                "100g 560€"
            )
            await self._send_product(
                context,
                cid,
                caption,
                video_id="BAACAgQAAxkBAAECyYRpbi7Sda__oBWO-VXZKGQj48Pb7gAC9hkAApIBcFMCDtlzmOQB_TgE",
                back_callback="cat_weed",
            )
            return
            
        if d == "sciroppo_consigli":
            prod = self.products["sciroppo"]
            text = (
                "Da mescolare con qualsiasi tipo di bevanda! Consigliamo liquidi freddi e dolci per coprire il sapore.\n"
                "Scuotere la boccetta prima di ogni uso per distribuirlo bene.\n"
                "Dose leggera - 10ml\n"
                "Dose media - 20 ml\n"
                "Dose pesante - 30+ ml\n"
                "Per trovare la quantita' perfetta per te consigliamo di iniziare con una dose leggera, e raddoppiare la dose fino a raggiungere l'effetto desiderato."
            )
            sent = await self._send_media_or_text(
                context,
                cid,
                text,
                back_callback="prod_sciroppo",
                video_file_id=prod.get("video_file_id", ""),
                photo_file_ids=prod.get("photo_file_ids", []),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "cat_weed":
            if not await self._check_membership(context, update.effective_user.id, cid):
                return

            kb = [
                [InlineKeyboardButton("Calispain", callback_data="weed_calispain")],
                [InlineKeyboardButton("Caliusa Outdoor", callback_data="weed_caliusa_outdoor")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="shop")],
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="Scegli il tipo di weed:",
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
            
        if d == "weed_calispain":
            if not await self._check_membership(context, update.effective_user.id, cid):
                return

            sent = await self._send_media_or_text(
                context,
                cid,
                self.weed_overview,
                back_callback="cat_weed",
                video_file_id=self.weed_video_file_id,
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "cat_hash":
            if not await self._check_membership(context, update.effective_user.id, cid):
                return

            cat = "hash"
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
            
        if d == "cat_sintetico":
            if not await self._check_membership(context, update.effective_user.id, cid):
                return

            kb = [
                [InlineKeyboardButton("COC4", callback_data="prod_neve")],
                [InlineKeyboardButton("X4NAX", callback_data="prod_xanax")],
                [InlineKeyboardButton("0XY", callback_data="prod_oxy")],
                [InlineKeyboardButton("PARACOD1NA", callback_data="prod_paracodina")],
                [InlineKeyboardButton("LSD", callback_data="prod_lsd")],
                [InlineKeyboardButton("MD", callback_data="prod_md")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="shop")],
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="Scegli un prodotto sintetico:",
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
            
        if d == "cat_tabaccheria":
            text = (
                "Abbiamo allestito una sezione tabaccheria per la vostra comodita’. "
                "Al momento gli oggetti devono ancora arrivare. (BACKWOODS ARRIVATI - Il resto previsto per il 16-18 gennaio visto un leggero ritardo)."
            )
            kb = [
                [
                    InlineKeyboardButton("Backwoods", callback_data="tab_backwoods"),
                    InlineKeyboardButton("Cartine e Filtri", callback_data="tab_cartine_filtri"),
                ],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="shop")],
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=text,
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        
        if d == "tab_backwoods":
            await self._send_product(
                context, cid,
                "DISPONIBILI!!! Gli originali Backwoods.\nSigari americani iconici, apparsi in decine di videoclip. Tabacco e foglia aromatizzata alla vaniglia, con una botta di nicotina ben percepibile. Ideali da svuotare e riempire con il fiore di vostra scelta.\nOgni confezione contiene 5 sigari.\nx1 conf. 20€ \nx2 conf. 30€\nx3 conf. 40€\nx5 conf. 55€\nx8 conf. 80€",
                video_id="BAACAgQAAxkBAAEC0mdpbmGtQPJ_Gm7Y3_IieT2f9jQOMgACHBsAApIBeFOj0sWNQwteazgE",
                back_callback="cat_tabaccheria"
            )
            return
            
        if d == "tab_cartine_filtri":
            text = "Visualizza la nostra selezione di cartine e filtri"
            kb = [
                [
                    InlineKeyboardButton("RAW", callback_data="tab_raw"),
                    InlineKeyboardButton("Elements", callback_data="tab_elements"),
                ],
                [
                    InlineKeyboardButton("Blunt Wraps", callback_data="tab_bluntwraps"),
                    InlineKeyboardButton("Filtri ActiTube", callback_data="tab_actitube"),
                ],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="cat_tabaccheria")],
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=text,
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
            
        if d == "tab_raw":
            await self._send_product(
                context, cid,
                "Cartine RAW\n—\n1 pacchetto 1.20€\n5 pacchetti 5€\n10 pacchetti 8.50€\n25 pacchetti 20€\nPer veri appassionati, non sbiancate, combustione ultra lenta e totalmente insapori. Ogni cartina viene filigranata individualmente, cosi evita che un lato bruci piu' velocemente dell'altro.\n32 cartine per pacchetto.\n\nFiltri RAW \n—\n1 pacchetto 1€\n5 pacchetti 4€\n10 pacchetti 7€\n20 pacchetti 13€\nFiltri RAW facilmente modellabili, regolabili in grandezza, non sbiancati. Privi di additivi chimici o cloro.\n50 filtri per pacchetto.\n\nRAW Kit\n—\n1 kit 1.80€\n5 kit 8€\n10 kit 15€\n25 kit 33€\nOgni kit contiene un pacchetto di cartine e un pacchetto di filtri, gli stessi visibili precedentemente.",
                photo_id="AgACAgQAAxkBAAEBBRhpUOP8GifRxCRvc90TdB-MoTZvrQACeAtrG1JBiVI7j4Fw7QPmBwEAAwIAA3gAAzYE",
                back_callback="tab_cartine_filtri"
            )
            return
            
        if d == "tab_elements":
            await self._send_product(
                context, cid,
                "Cartine Elements\n—\nCartine per intenditori, combustione ultra lenta, sono fatte di pura carta di riso, bruciano senza creare cenere. Colla in gomma di zucchero.\n1 pacchetto 1.20€\n5 pacchetti 5€\n10 pacchetti 8.50€\n25 pacchetti 20€\n\nFiltri Elements\n—\n1 pacchetto 1€\n5 pacchetti 4€\n10 pacchetti 7€\n20 pacchetti 13€\nQuesti filtri Elements sono ecosostenibili e naturali, senza traccia di sostanze chimiche, ma sopratutto sono facili da usare.\n\nElements Kit\n—\n1 kit 1.80€\n5 kit 8€\n10 kit 15€\n25 kit 32€\nOgni kit contiene un pacchetto di cartine e un pacchetto di filtri, gli stessi visibili precedentemente.",
                photo_id="AgACAgQAAxkBAAEBBSVpUOiV7GwSb1NX0fJeTwaJPd9VqgACfQtrG1JBiVJzDmdQmw_p5AEAAwIAA3kAAzYE",
                back_callback="tab_cartine_filtri"
            )
            return
            
        if d == "tab_bluntwraps":
            await self._send_product(
                context, cid,
                "Juicy Jays Wraps Blue di canapa\n—\n1 pacchetto 2€\n2 pacchetti 3.80€\n5 pacchetti 8.50€\n10 pacchetti 14.50€\n20 pacchetti 20€\nFatti da foglia di canapa aromatizzata al mirtillo, brucia lentamente ed e' piu' facile da rollare rispetto alle foglie di tabacco, ed e' completamente priva di nicotina. Perfetto per blunt.",
                photo_id="AgACAgQAAxkBAAEBBRtpUORvVKgNiIyIt9L5NsVpWE_qrwACeQtrG1JBiVIa3xODPSP6MwEAAwIAA3gAAzYE",
                back_callback="tab_cartine_filtri"
            )
            return
            
        if d == "tab_actitube":
            await self._send_product(
                context, cid,
                "Filtri a carboni attivi Actitube 7mm\n—\n1 pacchetto 3€\n2 pacchetti 5€\n5 pacchetti 10€\n10 pacchetti 18€\nFiltri ai carboni attivi utili per ridurre l'assunzione di catrame. Dotati di cappuccio in ceramica su entrambe le estremita'.\nMigliorano il sapore delle boccate. Diametro di 7mm. Di origine vegetale e biodegradabili. Riutilizzabili.\nOgni pacchetto contiene 10 filtri.",
                photo_id="AgACAgQAAxkBAAEBBSNpUOS0Oh4YRmjxychZ30bAe1C4pQACegtrG1JBiVLziPgOsBazfQEAAwIAA3gAAzYE",
                back_callback="tab_cartine_filtri"
            )
            return

        if d == "prod_neve":
            prod = self.products["neve"]
            await self._send_product(context, cid, prod["caption"], video_id=prod["video_file_id"], back_callback="cat_sintetico")
            return
            
        if d == "prod_xanax":
            caption = (
                "Xanax 1mg\n"
                "Prezzo:\n"
                "5 pillole - 30€\n"
                "10 pillole - 40€\n\n"
                "Diretto da Estero 🇵🇱 (7-10 gg. lav.)\n"
                "5 blister (50 pillole) - 130€\n"
                "10 blister - 190€\n\n"
                "Benzo ad azione ultra-rapida che cancella ansia, stress e tensioni in pochi minuti, "
                "sostituendoli con un relax muscolare profondo e una calma mentale totale. "
                "Perfetto per un \"reset\" immediato o per accompagnare qualsiasi esperienza con un'onda di distacco tranquillo e piacevole. "
                "Blister diversi di provenienza farmaceutica.\n\n"
                "⚖️ Dose Consigliata:\n"
                "• Principianti: 2mg\n"
                "• Esperti: 4mg"
            )
            await self._send_product(
                context,
                cid,
                caption,
                video_id="BAACAgQAAxkBAAEB8pZpY4zIBl1rw-BgBTGfqDjDAAFPgpoAAscdAAIi5iFToJi2HP8P1oo4BA",
                back_callback="cat_sintetico",
            )
            return

        if d == "prod_caramelle":
            caption = (
                "Dank Gummies – caramelle al THC da 500 mg\n"
                "IN ARRIVO SETTIMANA PROSSIMA.\n"
                "Morbide, gustose e incredibilmente potenti. Basta mezza caramella per sentire un effetto intenso e prolungato che si fa sentire dopo più o meno un'ora. "
                "Perfette per chi vuole il massimo senza dare nell'occhio, "
                "o semplicemente per chi vuole provare qualcosa di diverso. Ogni pacchetto contiene 5 caramelle con 100 mg di THC.\n\n"
                "1 pacchetto - 30€\n"
                "2 pacchetti - 45€\n"
                "5 pacchetti - 95€\n"
                "10 pacchetti - 180€"
            )
            await self._send_product(
                context,
                cid,
                caption,
                video_id="BAACAgQAAxkBAAECn45pa9RavFAHDaX4fr42cBmZLDh-pAACeyMAAvFyYVOyKX3nBnOuBDgE",
                back_callback="shop",
            )
            return

        if d == "prod_oxy":
            caption = (
                "Oxypronal 40/20\n"
                "1 pillola 15€\n"
                "5 pillole 45€\n"
                "10 pillole 75€\n"
                "Conf. (28) 140€\n\n"
                "Analgesico a base di ossicodone. L'ossicodone offre un'onda calda di pura euforia, benessere totale e un relax corporeo profondo, "
                "con formulazione a durata prolungata. L'esperienza definitiva per il sollievo ricreativo. Provenienza farmaceutica. "
                "(Non rompere le pillole, ma si possono dividere in due.)\n\n"
                "⚖️ Dose Consigliata:\n"
                "• Principianti: 20mg\n"
                "• Esperti: 40mg"
            )
            await self._send_product(
                context,
                cid,
                caption,
                video_id="BAACAgQAAxkBAAEB8phpY4zPAb4f9uqzU8MzRg_zCqthkAACyB0AAiLmIVP3W179OOt9TzgE",
                back_callback="cat_sintetico",
            )
            return
            
        if d == "prod_paracodina":
            caption = (
                "Paracodina 10,25mg/ml Gocce\n"
                "Prezzo:\n"
                "1 flacone (14,63ml) - 70€\n"
                "2 flaconi (29,26ml) - 120€\n\n"
                "Sciroppo a base di diidrocodeina. Per un effetto sedativo e calmante, profondo e distensivo, che ti accompagna in uno stato di quiete e piacere duraturo. "
                "Meno potente dell’ossicodone. Provenienza farmaceutica.\n\n"
                "⚖️ Dose Consigliata:\n"
                "• Principianti: 60mg\n"
                "• Esperti: 150mg"
            )
            await self._send_product(
                context,
                cid,
                caption,
                video_id="BAACAgQAAxkBAAEB8hFpY4gSw_SVeHXMdeK8GJZyYluFMgACvB0AAiLmIVP61CA3WBz_XjgE",
                back_callback="cat_sintetico",
            )
            return
            
        if d == "prod_lsd":
            caption = (
                "LSD 250µg Blotter\n"
                "Prezzo:\n"
                "1 cartone - 15€\n"
                "2 cartoni - 25€\n"
                "5 cartoni - 50€\n"
                "10 cartoni - 75€\n"
                "20 cartoni - 125€\n"
                "30 cartoni - 165€\n"
                "Diretto da Estero 🇩🇪 (7-10 gg. lav.)\n"
                "50 cartoni - 200€\n"
                "100 cartoni - 330€\n\n"
                "Psichedelico classico su blotter tema Spongebob & Patrick. 250µg di pura esperienza visiva e mentale, per un viaggio intenso tra pattern geometrici, "
                "esplorazione introspettiva e percezione amplificata. Purezza certificata.\n\n"
                "⚖️ Dose Consigliata:\n"
                "• Principianti: 1 cartone.\n"
                "• Esperti: 1.5-2 cartoni."
            )
            await self._send_product(
                context,
                cid,
                caption,
                video_id="BAACAgQAAxkBAAEB8g9pY4gLdV6CDdzQLU_UFV6BHMjgAQACux0AAiLmIVPbx9TTHMVuGDgE",
                back_callback="cat_sintetico",
            )
            return
            
        if d == "prod_md":
            caption = (
                "MDMA 300mg Pills (Blue Punisher)\n\n"
                "IN ARRIVO TRA IL 20-21 GENNAIO\n"
                "1 pillola - 25€\n"
                "2 pillole - 35€\n"
                "5 pillole - 60€\n"
                "10 pillole - 90€\n"
                "20 pillole - 135€\n"
                "Diretto da Estero 🇩🇪 (7-10 gg. lav.)\n"
                "50 pillole - 210€\n"
                "100 pillole - 320€\n\n"
                "Pillola iconica da 300mg di MDMA puro. Per un'onda di euforia schiacciante, energia inesauribile e empatia totale. "
                "L'esperienza classica e potente per una serata di pura connessione e piacere sensoriale amplificato.\n\n"
                "⚖️ Dose Consigliata:\n"
                "• Principianti: ½ pillola.\n"
                "• Esperti: 1 pillola per il roll completo."
            )
            await self._send_product(
                context,
                cid,
                caption,
                photo_id="AgACAgQAAxkBAAEB8tppY46gsiseZfCkTiH7BDN0PnoDGAACLgxrG6lJEVPNKMTCFb62PwEAAwIAA3kAAzgE",
                back_callback="cat_sintetico",
            )
            return

        if d.startswith("prod_hash_") or d.startswith("prod_weed_"):
            cat = "hash" if d.startswith("prod_hash_") else "weed"
            idx = int(d.rsplit("_", 1)[1])
            prods = self.categories.get(cat, [])
            if 0 <= idx < len(prods):
                prod = prods[idx]
                caption = prod.get("caption", f"📦 *{prod.get('name', '')}*")
                sent = await self._send_media_or_text(
                    context,
                    cid,
                    caption,
                    back_callback=f"cat_{cat}",
                    video_file_id=prod.get("video_file_id", ""),
                    photo_file_ids=prod.get("photo_file_ids", []),
                )
                context.user_data["last_menu_msg_id"] = sent.message_id
            else:
                await q.answer("❌ Prodotto non trovato!")
            return

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        m = update.effective_message
        usr = update.effective_user
        self.user_ids.add(usr.id)
        self._save_users()

        # Handle product suggestion flow
        if usr and usr.id != ADMIN_USER_ID and context.user_data.get("awaiting_suggestion"):
            suggestion_text = (
                m.text or m.caption or
                (f"<{type(m.effective_attachment).__name__}>" if m.effective_attachment else "<no text>")
            )

            # Build suggestion entry
            entry = {
                "user_id": usr.id,
                "username": usr.username,
                "full_name": usr.full_name,
                "suggestion": suggestion_text,
            }
            self.suggestions.append(entry)
            self._save_suggestions()

            # Relay to admin
            await self._relay_to_admin(
                context,
                usr,
                f"[SUGGERIMENTO PRODOTTO]\n{suggestion_text}"
            )

            # Reset flag and confirm to user
            context.user_data["awaiting_suggestion"] = False
            await m.reply_text("Grazie per il suggerimento! È stato inoltrato all'amministratore.")
            return

        if usr and usr.id != ADMIN_USER_ID:
            txt = (
                m.text or m.caption or
                (f"<{type(m.effective_attachment).__name__}>" if m.effective_attachment else "<no text>")
            )
            await self._relay_to_admin(context, usr, txt)
            
        if usr and usr.id == ADMIN_USER_ID:
            if m.video:
                await m.reply_text(f"File ID del video:\n<code>{m.video.file_id}</code>", parse_mode=ParseMode.HTML)
                return
            if m.photo:
                await m.reply_text(f"File ID della foto:\n<code>{m.photo[-1].file_id}</code>", parse_mode=ParseMode.HTML)
                return
        t = m.text.lower() if m.text else ""
        if any(w in t for w in ("ciao", "salve")):
            await m.reply_text("Ciao! 👋 Usa /start per iniziare.")
        elif "aiuto" in t or "help" in t:
            await m.reply_text("Usa /start per vedere il menu principale.")
        else:
            await m.reply_text("Non ho capito. Usa /start per vedere le opzioni disponibili.")

# ───────────────────────── MAIN ───────────────────────── #
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
