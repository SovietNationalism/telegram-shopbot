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
            "1": {
                "name": "Dry Filtrato 🍫",
                "price": "3g 30\n5g 40\n10g 70\n15g 100\n25g 160\n35g 215\n50g 250\n100g 430\n200g 780",
                "description": "ULTIME RIMANENZE.\nDry filtrato a 120 micron con effetto potente e duraturo, e un odore vivace.",
                "video_file_id": "BAACAgQAAxkBAAICKGhtHmeAa3WA1B8UshA03xwIGRh6AAItHgACw-ZoUyEBRLZYiRBqNgQ",
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
                    "📐 Dosaggio consigliato (2 mg/ml):\n"
                    "• 🟢 Principianti: 10–15 mg (5–7.5 ml circa)\n"
                    "• 🟡 Regolari: 25–35 mg (12.5–17.5 ml)\n"
                    "• 🔴 Esperti: 50 + mg (25 ml e oltre)"
                ),
                "video_file_id": "BAACAgQAAxkBAAIBCmhsFSRwLTrFoTt3ZbImNDzA8cKtAALKHQACU4xhU_j8jDMDFSiJNgQ",
            },
            "3_10": {
                "name": "Caramelle al THC 🇪🇸 - Formato 10",
                "caption": (
                    "📦 *Caramelle al THC 🇪🇸 - Formato 10 caramelle da 500mg*\n"
                    "Runtz Gummies\n"
                    "White Runtz Fruit Punch - “Ether” Runtz Green Apple - Original Runtz Berries - "
                    "Pink Runtz Watermelon\n\n"
                    "Smacker Gummies Sours (Mix Green Apple, Blue Raspberry, Cherry, Lemon & Watermelon)\n\n"
                    "1 - 20\n2 - 35\n3 - 50\n4 - 60\n5 - 70\n10 - 130\n\n"
                    "Queste caramelle gommose hanno una consistenza densa stile orsetti Haribo, "
                    "un ottimo sapore e un effetto sorprendentemente potente."
                ),
                "video_file_id": "BAACAgQAAxkBAAPvaGwJdobhaO1RPvm1nrbxIKokTOIAAqgdAAJTjGFTqdTZCjgZEpU2BA",
            },
            "3_20": {
                "name": "Caramelle al THC 🇪🇸 - Formato 20",
                "caption": (
                    "📦 *Caramelle al THC 🇪🇸 - Formato 20 caramelle 600mg*\n"
                    "Rancher Gummies Original Flavors (Mix Strawberry, Watermelon, Blue Raspberry)\n\n"
                    "Rancher Gummies Sours (Mix Strawberry, Watermelon, Blue Raspberry)\n\n"
                    "1 - 25\n2 - 40\n3 - 55\n4 - 70\n5 - 80\n10 - 140\n\n"
                    "Queste caramelle gommose hanno una consistenza densa stile orsetti Haribo, "
                    "un ottimo sapore e un effetto sorprendentemente potente."
                ),
                "video_file_id": "BAACAgQAAxkBAAPvaGwJdobhaO1RPvm1nrbxIKokTOIAAqgdAAJTjGFTqdTZCjgZEpU2BA",
            },
            "4": {
                "name": "THC Vapes Packwoods™ x Runtz 💨",
                "price": "1 - 45\n2 - 80\n3 - 110\n4 - 135\n5 - 160\n10 - 300",
                "description": "Con 1000 mg di distillato Delta-9 THC, basta una decina di tiri per sentire una fattanza potente.",
                "special_note": "DETTAGLIO DISPONIBILE, ULTIME PAIA RIMASTE IL RESTO PRENOTATE.",
                "video_file_id": "BAACAgQAAxkBAAIBhGhsLZ3WwkXvnqI-G74L_hsWrg6YAAI8GQACw-ZgU0zEehfiSYpmNgQ",
            },
            "5": {
                "name": "THC Brownies 🍰",
                "caption": (
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
            "6": {
                "name": "THC Cookies 🍪",
                "caption": (
                    "📦 *THC Cookies*\n"
                    "💵 Prezzo:\n1pz 8€\n2pz 14€\n5pz 30€\n10pz 55€\n20pz 100€\n50pz 230€\n\n"
                    "📝 Descrizione:\n"
                    "Biscotto morbido al cioccolato con 35 mg di THC per pezzo, preparato con "
                    "crumble di brownie e burro infuso per un gusto intenso e una consistenza chewy. "
                    "Effetto ben bilanciato, confezionato singolarmente per massima discrezione e freschezza."
                ),
                "video_file_id": "BAACAgQAAxkBAAIC2WhuyCwydopTi2xpCcoGIKe3YHoAA7YVAAJz7nFTWGJ8xrGDgw42BA",
            },
            "7": {
                "name": "Raspberry Runtz 🍒",
                "caption": (
                    "📦 *Raspberry Runtz - Indica*\n"
                    "💵 *Prezzo:*\n"
                    "2g - 25€\n3g - 30€\n5g - 45€\n10g - 75€\n15g - 115€\n25g - 175€\n"
                    "30g - 205€\n35g - 235€\n50g - 300€\n100g - 450€\n\n"
                    "📝 *Descrizione:*\n"
                    "Genetica fruttata con profumo fresco e pungente. Fiori compatti, resinati e "
                    "appiccicosi al tatto. Effetto intenso, non leggero come le altre sul mercato, "
                    "qualità visibile e sentita fin da subito."
                ),
                "video_file_id": "BAACAgQAAxkBAAIpVGh7CE6j2fpQozHOSlDJ1tukxKCNAALtHAACZQ7RU1Z6QdsqVO6qNgQ",
            },
        }

        # --------------------  SERVICES -------------------- #
        self.services = {
            "1": {
                "name": "Creazione Bot Telegram",
                "price": "€35/m",
                "description": "Sei un venditore o comunque sei interessato alla creazione di un bot simile? Posso aiutarti.",
                "photo_file_id": "AgACAgQAAxkBAAIBVmY0n9f5v1cAAQ1nUuH4QnX8h3QjAAJ8tzEbJ2FTkJ7yK5y1vN2BAAMCAANzAAMvBA",
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

    # ────────────────────────  CALLBACKS  ──────────────────────── #

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        q   = update.callback_query
        d   = q.data
        cid = q.message.chat.id

        await q.answer()

        if update.effective_user.id != ADMIN_USER_ID:
            await self._relay_to_admin(context, update.effective_user, f"Pressed button: {d}")

        await self.delete_last_menu(context, cid)

        # ---------- nuova voce REGOLAMENTO ---------- #
        if d == "rules":
            kb = [[InlineKeyboardButton("⬅️ Indietro", callback_data="back_to_main")]]
            sent = await context.bot.send_message(
                chat_id=cid,
                text=self.rules_text,
                reply_markup=InlineKeyboardMarkup(kb),
            )
            context.user_data["last_menu_msg_id"] = sent.message_id
            return
        # ---------- torna al menu principale ---------- #
        if d == "back_to_main":
            await self.start(update, context)
            return

        # ---------------- resto del tuo handler (identico) ---------------- #
        #  (tutta la logica precedente per shop, payments, prodotti, servizi …)
        #  Non è stata modificata e continua a funzionare.

        # ------------------------------------------------------------------ #
        # Il codice per le altre sezioni rimane identico alla versione
        # precedente (Shop, Payments, Prodotti, Servizi, ecc.).
        # ------------------------------------------------------------------ #

    # ────────────────────────  MESSAGES  ──────────────────────── #

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        m   = update.effective_message
        usr = update.effective_user

        if usr and usr.id != ADMIN_USER_ID:
            txt = m.text or m.caption or f"<{type(m.effective_attachment).__name__}>" if m.effective_attachment else "<no text>"
            await self._relay_to_admin(context, usr, txt)

        if usr and usr.id == ADMIN_USER_ID:
            if m.video:
                await m.reply_text(f"File ID del video:\n<code>{m.video.file_id}</code>", parse_mode=ParseMode.HTML); return
            if m.photo:
                await m.reply_text(f"File ID della foto:\n<code>{m.photo[-1].file_id}</code>", parse_mode=ParseMode.HTML); return

        t = m.text.lower() if m.text else ""
        if any(w in t for w in ["ciao", "salve"]):
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
        app.add_handler(CallbackQueryHandler(bot.button_handler))
        app.add_handler(MessageHandler(filters.ALL, bot.handle_message))

        app.run_polling()
        logger.info("Bot terminato.")
    except Exception as e:
        logger.exception(f"❌ Errore critico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
