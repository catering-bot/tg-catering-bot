import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

MENU = {
    "эконом": {
        "канапе": [
            ("Митбол из говядины с паназиатским соусом", 163.8),
            ("Митбол из индейки с томатной сальсой", 151.2),
            ("Сырные шарики", 151.2),
            ("Фалафель с хумусом из фасоли", 144.9),
            ("Томаты черри с моцареллой и соусом песто", 214.2),
        ],
        "брускетта": [
            ("С моцареллой, черри и зелёным базиликом", 264.6),
            ("С жареными грибами и творожным муссом", 239.4),
            ("С баклажаном, брынзой и гранатом", 283.5),
        ],
        "салаты": [
            ("Салат Цезарь с птицей и перепелиным яйцом", 793.8),
            ("Салат Греческий с пряными травами", 793.8),
            ("Салатный микс с печёной свёклой и брынзой", 617.4),
        ],
        "горячее": [
            ("Цыплёнок барбекю маринованный в травах", 1233.3),
            ("Овощи гриль со сливочным соусом", 466.7),
            ("Паста Болоньезе", 880.0),
        ],
        "десерты": [
            ("Медовик", 166.7),
            ("Красный бархат", 220.0),
            ("Фрукты на шпажке", 413.3),
        ],
        "напитки": [
            ("Морс ягодный (1 литр)", 855.6),
            ("Артезианская вода 500мл", 133.3),
            ("Чай в ассортименте", 127.8),
        ],
    },
    "стандарт": {
        "канапе": [
            ("Тартар из лосося на крутоне", 214.2),
            ("Слабосолёная сёмга с мини спаржей и крем-чизом", 252.0),
            ("Рулетик из ростбифа с артишоками", 390.6),
            ("Сыр Бри с вяленной клюквой и фисташкой", 283.5),
            ("Угорь на рисовом спонже с унаги соусом", 283.5),
        ],
        "тарталетки": [
            ("Фило с тартаром из лосося", 214.2),
            ("Фило с креветками и гуакамоле", 302.4),
            ("Вонтон с тартаром из говядины и каперсами", 245.7),
        ],
        "брускетта": [
            ("С подкопчённым лососем и артишоками", 277.2),
            ("С ростбифом, спаржей и рукколой", 434.7),
            ("С пармской ветчиной и грушей на гриле", 441.0),
        ],
        "салаты": [
            ("С лососем, брюссельской капустой и апельсиновым дрессингом", 806.4),
            ("Салат с креветками, авокадо и рукколой", 875.7),
            ("Утиная грудка с нектарином гриль и кешью", 837.9),
        ],
        "горячее": [
            ("Филе из сёмги в апельсиновом маринаде с ризотто", 1140.0),
            ("Ягнёнок на косточке с перечным соусом", 1173.3),
            ("Паэлья с морепродуктами", 1586.7),
        ],
        "десерты": [
            ("Панакота маракуйя", 335.6),
            ("Тирамису", 246.7),
            ("Фрукты и ягоды в конверте", 486.7),
        ],
        "напитки": [
            ("Лимонад домашний (1 литр)", 855.6),
            ("Морс ягодный (1 литр)", 855.6),
            ("Свежевыжатый сок апельсин", 555.6),
        ],
    },
    "премиум": {
        "канапе": [
            ("Рисовый спонж с икрой летучей рыбы и крем-чиз из копченого угря", 201.6),
            ("Гребешки с манго и соусом из лобстеров", 522.9),
            ("Мини блинчики с икрой", 315.0),
            ("Рулетик из пармской ветчины с яблоком и сыром дорблю", 441.0),
            ("Тунец с чукой", 252.0),
        ],
        "тарталетки": [
            ("Фило с тартаром из лосося в апельсиновом соусе", 214.2),
            ("Вонтон с тартаром из тунца с вялеными черри и киноа", 315.0),
            ("Фило с креветками и гуакамоле", 302.4),
        ],
        "брускетта": [
            ("С мясом краба, гуакамоле и чёрными креветками", 441.0),
            ("С ростбифом, спаржей и рукколой", 434.7),
            ("С пармской ветчиной и грушей на гриле", 441.0),
        ],
        "салаты": [
            ("Салат с креветками, авокадо и рукколой", 875.7),
            ("Утиная грудка с нектарином гриль и кешью", 837.9),
            ("Микс с артишоками, авокадо и лимонным песто", 819.0),
        ],
        "горячее": [
            ("Чилийский сибас на гриле с картофельным пюре", 1800.0),
            ("Ростбиф с брусничным соусом и беби картофелем", 1513.3),
            ("Филе миньон с мятным кускусом и вишнёвым соусом", 1260.0),
        ],
        "десерты": [
            ("Ягодная тарелка", 2520.0),
            ("Панакота маракуйя", 335.6),
            ("Тирамису", 246.7),
        ],
        "напитки": [
            ("Лимонад домашний (1 литр)", 855.6),
            ("Свежевыжатый сок апельсин", 555.6),
            ("Свежевыжатый сок ананас", 750.0),
        ],
    },
}

PORTIONS = {
    "фуршет": {"канапе": 5, "тарталетки": 2, "брускетта": 2, "салаты": 1, "горячее": 1, "десерты": 2, "напитки": 3},
    "банкет": {"салаты": 1, "горячее": 1, "десерты": 2, "напитки": 3},
    "bbq":    {"горячее": 3, "салаты": 1, "десерты": 1, "напитки": 3},
}

CAT_NAMES = {
    "канапе": "🫙 КАНАПЕ",
    "тарталетки": "🥟 ТАРТАЛЕТКИ",
    "брускетта": "🥖 БРУСКЕТТА",
    "салаты": "🥗 САЛАТЫ",
    "горячее": "🍖 ГОРЯЧЕЕ",
    "десерты": "🍰 ДЕСЕРТЫ",
    "напитки": "🥤 НАПИТКИ",
}

BUDGET_LABELS = {
    "эконом": "💚 Эконом (до 3,000 ₽/чел)",
    "стандарт": "💛 Стандарт (3,000–6,000 ₽/чел)",
    "премиум": "💎 Премиум (от 6,000 ₽/чел)",
}

TYPE, GUESTS, BUDGET, CONFIRM = range(4)


def generate_menu(event_type: str, guests: int, budget: str) -> str:
    portions = PORTIONS.get(event_type, PORTIONS["фуршет"])
    menu_items = MENU.get(budget, MENU["стандарт"])
    type_labels = {"фуршет": "🍽️ ФУРШЕТ", "банкет": "🥂 БАНКЕТ", "bbq": "🔥 BBQ"}
    title = type_labels.get(event_type, "🍽️ ФУРШЕТ")
    lines = [f"{title} на {guests} человек", f"{BUDGET_LABELS[budget]}", "=" * 35]
    total = 0
    for category, portions_per_person in portions.items():
        if category not in menu_items:
            continue
        lines.append(f"\n{CAT_NAMES.get(category, category.upper())}:")
        for name, price in menu_items[category][:3]:
            total_portions = portions_per_person * guests
            cost = price * total_portions
            total += cost
            lines.append(f"  • {name[:45]}")
            lines.append(f"    {total_portions} порц. × {price:.0f}₽ = {cost:,.0f}₽")
    lines.append(f"\n{'='*35}")
    lines.append(f"💰 ИТОГО: {total:,.0f} ₽")
    lines.append(f"👤 На 1 человека: {total/guests:,.0f} ₽")
    lines.append(f"\n📞 Для заказа:")
    lines.append(f"📧 info@slcatering.ru")
    lines.append(f"☎️ +7 (926) 141-25-18")
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🍽️ Фуршет", "🥂 Банкет", "🔥 BBQ"]]
    await update.message.reply_text(
        "👋 Добро пожаловать в SmiLe Event & Catering!\n\n"
        "Я помогу рассчитать меню и стоимость.\n\n"
        "Выберите тип мероприятия:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return TYPE


async def get_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "фуршет" in text:
        context.user_data["type"] = "фуршет"
    elif "банкет" in text:
        context.user_data["type"] = "банкет"
    elif "bbq" in text:
        context.user_data["type"] = "bbq"
    else:
        await update.message.reply_text("Пожалуйста выберите из предложенных вариантов.")
        return TYPE
    await update.message.reply_text(
        f"Тип: {context.user_data['type'].upper()}\n\n"
        "👥 Сколько гостей ожидается?\n(введите число, например: 50)",
        reply_markup=ReplyKeyboardRemove(),
    )
    return GUESTS


async def get_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        guests = int(update.message.text.strip())
        if guests < 1 or guests > 10000:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Пожалуйста введите число гостей (например: 50)")
        return GUESTS
    context.user_data["guests"] = guests
    keyboard = [["💚 Эконом"], ["💛 Стандарт"], ["💎 Премиум"]]
    await update.message.reply_text(
        f"Гостей: {guests}\n\n💰 Выберите бюджет на человека:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return BUDGET


async def get_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "эконом" in text:
        context.user_data["budget"] = "эконом"
    elif "стандарт" in text:
        context.user_data["budget"] = "стандарт"
    elif "премиум" in text:
        context.user_data["budget"] = "премиум"
    else:
        await update.message.reply_text("Пожалуйста выберите бюджет из предложенных вариантов.")
        return BUDGET
    menu_text = generate_menu(context.user_data["type"], context.user_data["guests"], context.user_data["budget"])
    keyboard = [["✅ Отправить заявку", "🔄 Начать заново"]]
    await update.message.reply_text(
        menu_text,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return CONFIRM


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "заявку" in update.message.text:
        await update.message.reply_text(
            "✅ Ваша заявка отправлена!\n\n"
            "Наш менеджер свяжется с вами в ближайшее время.\n\n"
            "📞 Лена Смирнова: +7 (926) 141-25-18\n"
            "📧 info@slcatering.ru\n\n"
            "Спасибо за обращение в SmiLe Event & Catering! 🎉",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END
    else:
        return await start(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("До свидания! Напишите /start чтобы начать заново.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), MessageHandler(filters.TEXT & ~filters.COMMAND, start)],
        states={
            TYPE:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type)],
            GUESTS:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_guests)],
            BUDGET:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_budget)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    print("🤖 Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
