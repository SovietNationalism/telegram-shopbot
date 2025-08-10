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
                    "TEMPORANEAMENTE SOLD OUT NUOVA RICETTA MIGLIORATA CON BOCCETTE MIGLIORI "
                    "E SENZA SEDIMENTO IN ARRIVO\n\n"
                    "Gusti: Lampone, Fragola, Menta, Limone\n\n"
                    "Formula a base di estratto di hashish in sciroppo dolce: massima stabilità "
                    "e biodisponibilità.\n\n"
                    "💧 Mischialo alle bevande fredde e dolci.\n"
                    "Ogni bottiglia: 300 mg THC in 150 ml.\n"
                    "Dosaggi consigliati (2 mg/ml):\n"
                    "🟢 10–15 mg • 🟡 25–35 mg • 🔴 50 mg+"
                ),
                "video_file_id": "BAACAgQAAxkBAAIBCmhsFSRwLTrFoTt3ZbImNDzA8cKtAALKHQACU4xhU_j8jDMDFSiJNgQ",
            },
            "4": {
                "name": "THC Vapes Packwoods™ 💨",
                "price": "1 - 45\n2 - 80\n3 - 110\n4 - 135\n5 - 160\n10 - 300",
                "description": "1,000 mg Delta-9 distillato: bastano pochi tiri per una fattanza potente.",
                "special_note": "DISPONIBILI",
                "video_file_id": "BAACAgQAAxkBAAIBhGhsLZ3WwkXvnqI-G74L_hsWrg6YAAI8GQACw-ZgU0zEehfiSYpmNgQ",
            },
            "5": {
                "name": "THC Brownies 🍰",
                "caption": (
                    "SOLD OUT\n\n"
                    "📦 *THC Brownies*\n"
                    "💵 Prezzo:\n1pz 10€\n2pz 15€\n5pz 35€\n10pz 65€\n20pz 120€\n50pz 280€\n\n"
                    "⚠️ 50 mg THC per pezzo. Scaldalo 10–20 s in microonde per un gusto top!"
                ),
                "video_file_id": "BAACAgQAAxkBAAICzmhucsfJasY9h-D9-mTSUhFTYGisAAIcGgACeZJxUyMtK0Venf2aNgQ",
            },
            "8": {
                "name": "Citronella Kush 🍋",
                "caption": (
                    "📦 *Citronella Kush* – SOLD OUT\n"
                    "Agrumi freschi, fiori resinosi e potenti.\n"
                    "Prezzi (g): 1.5 25€ • 2 24€ • 4 35€ • 5 45€ • 8 70€ • 10 80€\n"
                    "…fino a 100 g 525€"
                ),
                "video_file_id": "BAACAgQAAxkBAAJTAAFokbjhN3ZdheSLMYqGzi9Nb335JAACOR0AAjvEiFCAvNsOwcysSTYE",
            },
        }

        # ------------------  ALTRO (ex-Servizi) ------------------ #
        self.services = {
            "1": {
                "name": "Creazione Bot Telegram",
                "price": "€35/m",
                "description": "Hai bisogno di un bot simile? Posso crearlo per te.",
                "photo_file_id": "AgACAgQAAxkBAAIBVmY0n9f5v1cAAQ1nUuH4QnX8h3QjAAJ8tzEbJ2FTkJ7yK5y1vN2BAAMCAANzAAMvBA",
            },
            "2": {
                "name": "Tabaccheria",
                "price": (
                    "Juicy Jay’s Hemp Wraps – Red Alert\n"
                    "1 pz 2€ | 5 pz 8.50€ | 10 pz 14.50€ | 20 pz 22€\n\n"
                    "⸻\n\n"
                    "RAW Cartine King Size Slim\n"
                    "1 pz 1.20€ | 5 pz 5€ | 10 pz 8.50€ | 25 pz 20€\n\n"
                    "⸻\n\n"
                    "RAW Filtri Perforated Wide\n"
                    "1 pz 1€ | 5 pz 4€ | 10 pz 7€ | 25 pz 15€\n\n"
                    "⸻\n\n"
                    "Kit RAW (cartine + filtri)\n"
                    "1 kit 1.80€ | 5 kit 8€ | 10 kit 15€ | 25 kit 33.50€"
                ),
                "description": "Cartine, filtri e wraps premium per rollate perfette.",
                "video_file_id": "BAACAgQAAxkBAAJIpmiN5A3zxkV7mpOA_22S3Tg5KDYPAAIZIgACE_pxUIDKk2M2sBaQNgQ",
            }
        }

        # ------------------  REGOLAMENTO  ------------------ #
        self.rules_text = (
            "📦 Spedizioni in tutta Italia\n"
            "1. Scrivici i prodotti e il metodo di pagamento.\n"
            "2. Confermiamo prezzo.\n"
            "3. Spedizione rapida e gratuita salvo eccezioni.\n\n"
            "🤝 Meet-up a Mantova: verifica foto documento + contanti.\n"
            "🚗 Delivery città limitrofe (mín 50€): Mantova 10–15€, Verona 20€, Brescia/Modena 25€…"
        )

    # ────────────────  HELPER: relay  ──────────────── #
    async def _relay_to_admin(self, context: ContextTypes.DEFAULT_TYPE, who, what: str):
        message = f"👤 {who.full_name} ({who.id})\n💬 {what}"
        try:
            await context.bot.send_message(ADMIN_USER_ID, message)
        except Exception as e:
            logger.warning(f"Relay failed: {e}")

    # ─────────────────  COMMANDS  ───────────────── #
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.delete_last_menu(context, update.effective_chat.id)
        kb = [
            [InlineKeyboardButton("🛍️ Shop", callback_data="shop")],
            [InlineKeyboardButton("💰 Pagamenti", callback_data="payments")],
            [InlineKeyboardButton("📋 Regolamento", callback_data="rules")],
            [InlineKeyboardButton("📢 Canale", url="https://t.me/+A3JnK9ALAmtiMjBk")],
            [InlineKeyboardButton("👥 Contattami", callback_data="contact")],
            [InlineKeyboardButton("👨‍💻 Developer", callback_data="developer")],
        ]
        msg = (
            "🎉 Benvenuto su *Vetrina ItalianEdibles* 🇮🇹\n"
            "Esplora i prodotti e contattaci in pochi clic!"
        )
        m = update.effective_message
        try:
            sent = await m.reply_photo(WELCOME_IMAGE_URL, caption=msg,
                                       parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb))
        except BadRequest:
            sent = await m.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb))
        context.user_data["last_menu_msg_id"] = sent.message_id

    async def delete_last_menu(self, context, chat_id):
        mid = context.user_data.get("last_menu_msg_id")
        if mid:
            try:
                await context.bot.delete_message(chat_id, mid)
            except:
                pass
            context.user_data["last_menu_msg_id"] = None

    # ─────────────────  CALLBACKS  ───────────────── #
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        q, d, cid = update.callback_query, update.callback_query.data, update.callback_query.message.chat.id
        await q.answer()
        if update.effective_user.id != ADMIN_USER_ID:
            await self._relay_to_admin(context, update.effective_user, f"Pressed {d}")
        await self.delete_last_menu(context, cid)

        # ---- rules ----
        if d == "rules":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            sent = await context.bot.send_message(cid, self.rules_text, reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---- back_to_main ----
        if d == "back_to_main":
            await self.start(update, context); return

        # ---- shop ----
        if d == "shop":
            kb = [
                [InlineKeyboardButton("📱 Prodotti", callback_data="products")],
                [InlineKeyboardButton("🔧 Altro", callback_data="services")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")],
            ]
            sent = await context.bot.send_message(
                cid, "🛍️ *SHOP*\nScegli una categoria:",
                parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(kb)
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---- payments ----
        if d == "payments":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            txt = (
                "💰 *METODI DI PAGAMENTO*\n\n"
                "🏦 Bonifico • 📲 Hype/Revolut/Satispay • 💸 Crypto LTC/BTC • 💵 Contanti\n"
                "PayPal o carte prepagate +10%."
            )
            sent = await context.bot.send_message(cid, txt, parse_mode=ParseMode.MARKDOWN,
                                                  reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---- contact / developer ----
        if d in ("contact", "developer"):
            txt = ("👥 *CONTATTAMI*: clicca per scrivermi direttamente."
                   if d == "contact"
                   else "👨‍💻 *DEVELOPER*: bot creato da @ItalianEdibles.")
            kb = [
                [InlineKeyboardButton("✉️ Scrivimi", url="https://t.me/ItalianEdibles")],
                [InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]
            ]
            sent = await context.bot.send_message(cid, txt, parse_mode=ParseMode.MARKDOWN,
                                                  reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---- products list ----
        if d in ("products", "back_to_products"):
            kb = [
                [InlineKeyboardButton(self.products[k]["name"], callback_data=f"product_{k}")]
                for k in ("2", "4", "5", "8")
            ] + [[InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]]
            sent = await context.bot.send_message(cid, "📱 *PRODOTTI*: scegli:",
                                                  parse_mode=ParseMode.MARKDOWN,
                                                  reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---- services list ----
        if d in ("services", "back_to_services"):
            kb = [
                [InlineKeyboardButton(s["name"], callback_data=f"service_{sid}")]
                for sid, s in self.services.items()
            ] + [[InlineKeyboardButton("⬅️ Indietro", callback_data="shop")]]
            sent = await context.bot.send_message(cid, "🔧 *ALTRO*: scegli:",
                                                  parse_mode=ParseMode.MARKDOWN,
                                                  reply_markup=InlineKeyboardMarkup(kb))
            context.user_data["last_menu_msg_id"] = sent.message_id
            return

        # ---- single product ----
        if d.startswith("product_"):
            key, prod = d.split("_")[1], self.products.get(d.split("_")[1])
            if not prod:
                await q.answer("❌ Prodotto non trovato!"); return
            caption = prod.get("caption") or (
                f"📦 *{prod['name']}*\n💵 Prezzi:\n{prod['price']}\n"
                f"📝 {prod.get('description','')}" + (f"\n\n*{prod.get('special_note')}*" if prod.get("special_note") else "")
            )
            kb_back = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Prodotti", callback_data="back_to_products")]])
            await self._send_media(context, cid, prod, caption, kb_back); return

        # ---- single service ----
        if d.startswith("service_"):
            sid, serv = d.split("_")[1], self.services.get(d.split("_")[1])
            if not serv:
                await q.answer("❌ Elemento non trovato!"); return
            caption = f"🛠️ *{serv['name']}*\n💵 Prezzo: {serv['price']}\n📝 {serv['description']}"
            kb_back = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Altro", callback_data="back_to_services")]])
            await self._send_media(context, cid, serv, caption, kb_back); return

    # helper to send video→photo→text
    async def _send_media(self, context, cid, item, caption, kb_back):
        try:
            if item.get("video_file_id"):
                sent = await context.bot.send_video(cid, item["video_file_id"], caption=caption,
                                                    parse_mode=ParseMode.MARKDOWN, supports_streaming=True,
                                                    reply_markup=kb_back)
            elif item.get("photo_file_id"):
                sent = await context.bot.send_photo(cid, item["photo_file_id"], caption=caption,
                                                    parse_mode=ParseMode.MARKDOWN, reply_markup=kb_back)
            else:
                raise BadRequest("no media")
        except BadRequest:
            sent = await context.bot.send_message(cid, caption, parse_mode=ParseMode.MARKDOWN, reply_markup=kb_back)
        context.user_data["last_menu_msg_id"] = sent.message_id

    # ────────────────  MESSAGES  ──────────────── #
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        m, usr = update.effective_message, update.effective_user
        if usr and usr.id != ADMIN_USER_ID:
            txt = m.text or m.caption or "<no text>"
            await self._relay_to_admin(context, usr, txt)
        if usr and usr.id == ADMIN_USER_ID:
            if m.video:
                await m.reply_text(f"Video ID:\n<code>{m.video.file_id}</code>", parse_mode=ParseMode.HTML); return
            if m.photo:
                await m.reply_text(f"Photo ID:\n<code>{m.photo[-1].file_id}</code>", parse_mode=ParseMode.HTML); return
        t = (m.text or "").lower()
        if any(w in t for w in ("ciao", "salve")):
            await m.reply_text("Ciao! Usa /start per cominciare.")
        elif "aiuto" in t or "help" in t:
            await m.reply_text("Usa /start per il menu principale.")
        else:
            await m.reply_text("Non capisco; prova /start.")

# ─────────────────────  MAIN  ───────────────────── #
def main():
    logger.info("Bot in avvio…")
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        bot = ShopBot()
        app.add_handler(CommandHandler("start", bot.start))
        app.add_handler(CallbackQueryHandler(bot.button_handler))
        app.add_handler(MessageHandler(filters.ALL, bot.handle_message))
        app.run_polling()
    except Exception as e:
        logger.exception(f"❌ Errore critico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
