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
ADMIN_USER_ID     = 8219761049
ADMIN_CONTACT     = "https://t.me/RegularDope"
REQUIRED_GROUP_ID = -1003514626970  # put the actual group ID here
REQUIRED_GROUP_LINK = "https://t.me/+xwCcckoNERw2MWU0"

WELCOME_IMAGE_URL = "https://i.postimg.cc/5yBdW1BK/IMG-0466.jpg"
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
    "• Carta di credito/debito (10% commissione)\n"
    "• Contanti spediti (+5 €)\n"
    "• PayPal (10% commissione)\n"
    "• Bonifico dal tabacchino (0% commissione)\n"
    "• Gift card crypto (Bitnovo, ecc.) (+10% commissione)\n"
    "• Buoni regalo (Amazon, ecc.) (+50% commissione)\n\n"
    "COSTO SPEDIZIONE:\n"
    "• Inpost GRATUITA\n"
    "• Altri corrieri 10€"
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
                "name": "THC Vapes Packwoods™ x Runtz",
                "price": (
                    "1 - 45€\n"
                    "2 - 80€\n"
                    "3 - 115€\n"
                    "4 - 145€\n"
                    "5 - 165€\n"
                    "10 - 300€\n"
                ),
                "description": "Disponibile in due strain\nBlue Dream\nSkywalker Og\nCon 1000 mg di distillato Delta-9 THC in ogni pennetta, basta una dozzina di tiri per sentire un effetto potente e duraturo.",
                "video_file_id": "BAACAgQAAxkBAAK8e2lMUoehoRdmRCvBGfZPztZEp2qfAAIoHQACnZJgUilpkLWW64h4NgQ",
                "photo_file_ids": [],
            },
            "funghetti": {
                "caption": (
                    "📦 *Funghi Psylocibe Cubensis*\n"
                    "Disponibili.\n\n"
                    "3.5g 45€\n"
                    "5g 65€\n"
                    "10g 105€\n"
                    "15g 125€\n20g 160€\n\n"
                    "Una miscela di varietà classiche e potenti, McKennai, Golden Teacher, e Jedi Mind Fuck.\n"
                    "Effetto profondo e duraturo, ideale per esplorare nuove dimensioni. Disponibili subito per chi cerca un'esperienza "
                    "autentica e coinvolgente."
                ),
                "video_file_id": "BAACAgQAAxkBAAI9gmk_9B6WfvUiC8Q6FWDumJqt_cZQAALaGgAC3ykBUjFj1UkcKnyCNgQ",  # Fill as needed
                "photo_file_ids": [],
            },
            "sciroppo": {
                "name": "Sciroppo al THC",
                "caption": (
                    "📦 *Sciroppo al THC* (formato 100 ml, 200 mg)\n"
                    "💵 Prezzo:\n"
                    "x 1 30€\n"
                    "x 2 45€\n"
                    "x 4 70€\n"
                    "x 5 80€\n"
                    "x 10 145€\n"
                    "x 20 265€\n\n"
                    "📝 Descrizione:\n"
                    "Composta da estratto di hashish a base di etanolo, emulsionato in uno sciroppo al lampone (o ciliega a scelta) per una stabilità e biodisponibilità superiore.\n"
                ),
                "video_file_id": "BAACAgQAAxkBAALA8WlM8ils5hJW6qELQ3rDIHhXlJFOAAKpGgACScdoUvDEPR-NjqSKNgQ",  # metti qui il file_id del video se ce l'hai, altrimenti lascia vuoto
                "photo_file_ids": [],
            },
            "neve": {
                "name": "Neve",
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
                        "DISPONIBILE:\n"
                        "5g 45€\n"
                        "10g 75€\n"
                        "15g 110€\n"
                        "20g 135€\n"
                        "30g 175€\n"
                        "40g 210€\n"
                        "50g 240€\n"
                        "100g 430€\n"
                        "200g 850€\n"
                        "Card bufalo plein. Meglio dei soliti dry sift commerciali a un prezzo imbattibile.\n"
                        "Effetto intenso e prolungato, ottimo odore e sapore, Già curato, si sbriciola con facilità ed è un piacere da fumare in tutti i modi."
                    ),
                    "video_file_id": "BAACAgQAAxkBAAIpLGk1eriw6PhQgnRcYqO9Eii-5OpvAAJsHgAC9lypUYj4r8UZBRQLNgQ",
                    "photo_file_ids": [],
                },
                {
                    "name": "Frozen 180/90",
                    "caption": (
                        "📦 *Frozen Sift 180/90* – Tropicana Cookies\n\n"
                        "Qualità premium, molto superiore a qualsiasi dry o filtrato, con un rapporto qualità/prezzo davvero competitivo.\n"
                        "Effetto deciso e duraturo, profilo aromatico intenso e gusto pulito.\n"
                        "Il materiale è ancora nel processo di cura e nel video si mostra vetrato.\n\n"
                        "💵 Prezzi:\n"
                        "3g 40€\n"
                        "5g 60€\n"
                        "10g 115€\n"
                        "15g 165€\n"
                        "20g 210€\n"
                        "25g 270€\n"
                        "35g 340€\n"
                        "50g 450€\n"
                        "100g 850€"
                    ),
                    "video_file_id": "BAACAgQAAxkBAAJvNmlGsy_TAQ2z9PKMchUAAU2owFL_KwACph4AAtE3OFICcX6H57AUyDYE",
                    "photo_file_ids": [],
                },
            ],
            "weed": [
                # Add WEED category products here later the same way
            ]
        }
        self.weed_video_file_id = "BAACAgQAAxkBAAIfGGksX9SvE4VCDU76INV67CCyjBRfAAJCGQACfFpgUb9qGHvsCn-ENgQ"
        self.weed_overview = (
            "🌿 *Weed*\n"
            "Una Calispain dalla genetica agrumata, dal profilo aromatico fresco e deciso. Fiori compatti e resinosi, estremamente "
            "appiccicosi al tatto. L’effetto è forte, persistente e si fa notare subito per purezza e carattere. Disponibile!\n\n"
            "Citronella Kush\n"
            "5g 40\n"
            "10g 75\n"
            "15g 110\n"
            "20g 135\n"
            "30g 175\n"
            "40g 200\n"
            "50g 220\n"
            "100g 420\n"
            "200g 780"
        )
        self.user_ids = set()

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
        await self.delete_last_menu(context, update.effective_chat.id)
        kb = [
            [InlineKeyboardButton("🛍️ SHOP", callback_data="shop")],
            [InlineKeyboardButton("💳 PAGAMENTI", callback_data="pagamenti")],
            [InlineKeyboardButton("📜 COME ORDINARE", callback_data="tos")],
            [InlineKeyboardButton("📦 ORDINA QUI", url=ADMIN_CONTACT)],
            [InlineKeyboardButton("💬 CHAT CLIENTI", url="https://t.me/+xwCcckoNERw2MWU0")],
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
                    InlineKeyboardButton("PACKW0ODS X RUNTZ", callback_data="prod_packwoods"),
                    InlineKeyboardButton("FUNGHETTI", callback_data="prod_funghetti")
                ],
                [
                    InlineKeyboardButton("SCIROPP0 THC", callback_data="prod_sciroppo"),
                    InlineKeyboardButton("SINTETICO", callback_data="cat_sintetico"),
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

        if d == "prod_packwoods":
            prod = self.products["packwoods"]
            caption = (
                f"📦 *{prod['name']}*\n"
                f"💵 Prezzo:\n{prod['price']}\n"
                f"📝 Descrizione: {prod['description']}"
            )
            sent = await self._send_media_or_text(
                context,
                cid,
                caption,
                back_callback="shop",
                video_file_id=prod.get("video_file_id", ""),
                photo_file_ids=prod.get("photo_file_ids", []),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "prod_funghetti":
            prod = self.products["funghetti"]
            sent = await self._send_media_or_text(
                context,
                cid,
                prod.get("caption", ""),
                back_callback="shop",
                video_file_id=prod.get("video_file_id", ""),
                photo_file_ids=prod.get("photo_file_ids", []),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
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
            is_member = await self._is_member_of_required_group(context, update.effective_user.id)
            if not is_member:
                sent = await self._ask_to_join_group(context, cid)
                context.user_data["last_menu_msg_id"] = sent.message_id
                return

            kb = [
                [InlineKeyboardButton("Calispain", callback_data="weed_calispain")],
                [InlineKeyboardButton("Cali Usa", callback_data="weed_cali_usa")],
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
            is_member = await self._is_member_of_required_group(context, update.effective_user.id)
            if not is_member:
                sent = await self._ask_to_join_group(context, cid)
                context.user_data["last_menu_msg_id"] = sent.message_id
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

        if d == "weed_cali_usa":
            is_member = await self._is_member_of_required_group(context, update.effective_user.id)
            if not is_member:
                sent = await self._ask_to_join_group(context, cid)
                context.user_data["last_menu_msg_id"] = sent.message_id
                return

            text = "Arriva verso fine gennaio!"
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="cat_weed")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=text,
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        if d == "cat_hash":
            is_member = await self._is_member_of_required_group(context, update.effective_user.id)
            if not is_member:
                sent = await self._ask_to_join_group(context, cid)
                context.user_data["last_menu_msg_id"] = sent.message_id
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
            is_member = await self._is_member_of_required_group(context, update.effective_user.id)
            if not is_member:
                sent = await self._ask_to_join_group(context, cid)
                context.user_data["last_menu_msg_id"] = sent.message_id
                return

            kb = [
                [InlineKeyboardButton("Neve", callback_data="prod_neve")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="shop")],
            ]
            sent = await context.bot.send_message(
                chat_id=cid,
                text="Scegli un prodotto sintetico:",
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
            
        if d == "prod_neve":
            prod = self.products["neve"]
            sent = await self._send_media_or_text(
                context,
                cid,
                prod.get("caption", ""),
                back_callback="cat_sintetico",
                video_file_id=prod.get("video_file_id", ""),
                photo_file_ids=prod.get("photo_file_ids", []),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
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
