import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

MENU = {
    "канапе": [
        ("Рисовый спонж с икрой летучей рыбы и крем-чиз из копченого угря", 201.6),
        ("Угорь на рисовом спонже с унаги соусом", 283.5),
        ("Тартар из лосося на крутоне", 214.2),
        ("Слабосолёная сёмга с мини спаржей и крем-чизом", 252.0),
        ("Гребешки с манго и соусом из лобстеров", 522.9),
        ("Мини блинчики с икрой", 315.0),
        ("Рулетик из ростбифа с артишоками и вялеными томатами", 390.6),
        ("Митбол из говядины с паназиатским соусом", 163.8),
        ("Сыр Бри с вяленной клюквой и фисташкой", 283.5),
        ("Сырные шарики", 151.2),
    ],
    "тарталетки": [
        ("Фило с тартаром из лосося в апельсиновом соусе", 214.2),
        ("Фило с креветками и гуакамоле", 302.4),
        ("Вонтон с тартаром из тунца с вялеными черри и киноа", 315.0),
        ("Вонтон с тартаром из говядины и каперсами", 245.7),
    ],
    "брускетта": [
        ("С подкопчённым лососем и артишоками", 277.2),
        ("С мясом краба, гуакамоле и чёрными креветками", 441.0),
        ("С ростбифом, спаржей и рукколой", 434.7),
        ("С моцареллой, черри и зелёным базиликом", 264.6),
        ("С жареными грибами и творожным муссом", 239.4),
    ],
    "салаты": [
        ("Салат Цезарь с птицей и перепелиным яйцом", 793.8),
        ("Салат Греческий с пряными травами", 793.8),
        ("С лососем, брюссельской капустой и апельсиновым дрессингом", 806.4),
        ("Салат с креветками, авокадо, рукколой и лимонной заправкой", 875.7),
        ("Микс салата с томатами черри, рукколой, моцареллой", 724.5),
    ],
    "горячее_банкет": [
        ("Чилийский сибас на гриле с картофельным пюре", 1800.0),
        ("Филе из сёмги в апельсиновом маринаде с ризотто", 1140.0),
        ("Ягнёнок на косточке с перечным соусом и беби картофелем", 1173.3),
        ("Ростбиф с брусничным соусом и печёным беби картофелем", 1513.3),
        ("Цыплёнок барбекю маринованный в травах и цедре апельсина", 1233.3),
        ("Паэлья с морепродуктами", 1586.7),
    ],
    "bbq": [
        ("Палтус на гриле", 973.3),
        ("Шашлык из свинины", 280.0),
        ("Баранина туша", 1086.7),
        ("Вырезка говяжья", 713.3),
        ("Цыплята в соусе тандури", 373.3),
        ("Колбаски ассорти", 653.3),
        ("Печёные овощи (картофель, свёкла, тыква, грибы)", 853.3),
    ],
    "десерты": [
        ("Медовик", 166.7),
        ("Панакота маракуйя", 335.6),
        ("Красный бархат", 220.0),
        ("Тирамису", 246.7),
        ("Фрукты и ягоды в конверте", 486.7),
    ],
    "напитки": [
        ("Лимонад домашний (1 литр)", 855.6),
        ("Морс ягодный (1 литр)", 855.6),
        ("Свежевыжатый сок апельсин", 555.6),
        ("Чай в ассортименте", 127.8),
        ("Артезианская вода 500мл", 133.3),
    ],
}

FURSHET_SET = {
    "канапе": 5,
    "тарталетки": 2,
    "брускетта": 2,
    "салаты": 1,
    "горячее_банкет": 1,
    "десерты": 2,
    "напитки": 3,
}

BANKET_SET = {
    "салаты": 1,
    "горячее_банкет": 1,
    "десерты": 2,
    "напитки": 3,
}

BBQ_SET = {
    "bbq": 3,
    "салаты": 1,
    "десерты": 1,
    "напитки": 3,
}

TYPE, GUESTS, CONFIRM = range(3)


def generate_menu(event_type: str, guests: int) -> str:
    if event_type == "фуршет":
        preset = FURSHET_SET
        title = "🍽️ ФУРШЕТ"
    elif event_type == "банкет":
        preset = BANKET_SET
        title = "🥂 БАНКЕТ"
    else:
        preset = BBQ_SET
        title = "🔥 BBQ"

    lines = [f"{title} на {guests} человек\n{'='*35}"]
    total = 0

    cat_names = {
        "канапе": "🫙 КАНАПЕ",
        "тарталетки": "🥟 ТАРТАЛЕТКИ",
        "брускетта": "🥖 БРУСКЕТТА",
        "салаты": "🥗 САЛАТЫ",
        "горячее_банкет": "🍖 ГОРЯЧЕЕ",
        "bbq": "🔥 BBQ",
        "десерты": "🍰 ДЕСЕРТЫ",
        "напитки": "🥤 НАПИТКИ",
    }

    for category, portions_per_person in preset.items():
        if category not in MENU:
            continue
        lines.append(f"\n{cat_names.get(category, category.upper())}:")
        items = MENU[category][:3]
        for name, price_per_portion in items:
            total_portions = portions_per_person * guests
            cost = price_per_portion * total_portions
            total += cost
            lines.append(f"  • {name[:45]}")
            lines.append(f"    {total_portions} порц. × {price_per_portion:.0f}₽ = {cost:,.0f}₽")

    lines.append(f"\n{'='*35}")
    lines.append(f"💰 ИТОГО: {total:,.0f} ₽")
    lines.append(f"👤 На 1 человека: {total/guests:,.0f} ₽")
    lines.append(f"\n📞 Для заказа: info@slcatering.ru")
    lines.append(f"☎️ +7 (926) 141-25-18")
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🍽️ Фуршет", "🥂 Банкет", "🔥 BBQ"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Добро пожаловать в SmiLe Event & Catering!\n\n"
        "Я помогу рассчитать меню и стоимость.\n\n"
        "Выберите тип мероприятия:",
        reply_markup=reply_markup,
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
        f"Отлично! Тип: {context.user_data['type'].upper()}\n\n"
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
    menu_text = generate_menu(context.user_data["type"], guests)
    keyboard = [["✅ Отправить заявку", "🔄 Начать заново"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(menu_text, reply_markup=reply_markup)
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
    await update.message.reply_text("До свидания! Напишите /start чтобы начать заново.",
                                     reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start),
                      MessageHandler(filters.TEXT & ~filters.COMMAND, start)],
        states={
            TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_type)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_guests)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    print("🤖 Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
