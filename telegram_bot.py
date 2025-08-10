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
                    "Una formula composta con estratto di hashish a base di etanolo di alta "
                    "qualità, emulsionato in uno sciroppo dolce per una stabilità e "
                    "biodisponibilità superiore.\n\n"
                    "💧 Da mescolare con qualsiasi tipo di bevanda! Consigliamo liquidi freddi "
                    "e dolci per mascherare il sapore.\n"
                    "Ogni bottiglia contiene 300 mg di THC attivo in 150 ml di sciroppo. "
                    "Scuotere la boccetta prima di ogni uso per distribuirlo bene.\n\n"
                    "Dosaggio consigliato (2 mg/ml):\n"
                    "🟢 Principianti: 10–15 mg (5–7.5 ml circa)\n"
                    "🟡 Regolari: 25–35 mg (12.5–17.5 ml)\n"
                    "🔴 Esperti: 50 + mg (25 ml e oltre)\n"
                    "Ricordarsi che gli ml non equivalgono ai grammi."
                ),
                "video_file_id": "BAACAgQAAxkBAAIBCmhsFSRwLTrFoTt3ZbImNDzA8cKtAALKHQACU4xhU_j8jDMDFSiJNgQ",
            },
            "4": {
                "name": "THC Vapes Packwoods™ 💨",
                "price": "1 - 45\n2 - 80\n3 - 110\n4 - 135\n5 - 160\n10 - 300",
                "description": "Con 1000 mg di distillato Delta-9 THC, basta una decina di tiri per sentire una fattanza potente.",
                "special_note": "DISPONIBILI",
                "video_file_id": "BAACAgQAAxkBAAIBhGhsLZ3WwkXvnqI-G74L_hsWrg6YAAI8GQACw-ZgU0zEehfiSYpmNgQ",
            },
            "5": {
                "name": "THC Brownies 🍰",
                "caption": (
                    "SOLD OUT\n\n"
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
            "8": {
                "name": "Citronella Kush 🍋",
                "caption": (
                    "📦 *Citronella Kush*\n"
                    "💵 Prezzo:\n"
                    "1.5g 25€\n2g 24€\n4g 35€\n5g 45€\n8g 70€\n10g 80€\n"
                    "15g 115€\n25g 185€\n30g 220€\n40g 255€\n50g 310€\n100g 525€\n\n"
                    "📝 Descrizione: SOLD OUT. Una Calispain con genetica agrumata con note fresche e potenti. Fiori densi, "
                    "ricchi di resina e molto appiccicosi. Effetto potente e duraturo, "
                    "si distingue subito per qualità e intensità."
                ),
                "video_file_id": "BAACAgQAAxkBAAJTAAFokbjhN3ZdheSLMYqGzi9Nb335JAACOR0AAjvEiFCAvNsOwcysSTYE",
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
                "description": "Cartine, filtri e wraps premium selezionati per rollare blunt perfetti.",
                "video_file_id": "BAACAgQAAxkBAAJIpmiN5A3zxkV7mpOA_22S3Tg5KDYPAAIZIgACE_pxUIDKk2M2sBaQNgQ",
            }
        }

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
            "Zone vicine a Mantova (entro 15 km) – 10/15€\n"
            "Verona – 20€\n"
            "Brescia – 25€\n"
            "Modena – 25€\n"
            "Cremona – 25€\n"
            "Reggio Emilia – 25€\n"
            "Carpi – 25€\n"
            "Parma – 25€"
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
        await self.delete_last_menu(context, update.effective_chat.id)

        kb = [
            [InlineKeyboardButton("🛍️ Shop 🛍️", callback_data="shop")],
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

    async def delete_last_menu(self, context, chat_id):
        msg_id = context.user_data.get("last_menu_msg_id")
        if msg_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
            context.user_data["last_menu_msg_id"] = None

    # Remaining handlers and logic are **unchanged** ...

# ──────────────────────────  MAIN  ────────────────────────── #
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
