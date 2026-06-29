import logging
import psycopg2
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import config


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать данные", callback_data='show_data')],
        [InlineKeyboardButton("Показать логи репликации", callback_data='show_logs')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'show_data':
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = cur.fetchall()

            if tables:
                result = "Список таблиц в БД:\n"
                for table in tables:
                    result += f"• {table[0]}\n"
            else:
                result = "В базе данных нет таблиц."

            cur.close()
            conn.close()
            await query.edit_message_text(result)

        except Exception as e:
            await query.edit_message_text(f"Ошибка при получении данных: {str(e)}")

    elif query.data == 'show_logs':
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_name = 'replication_logs'
                );
            """)
            has_logs_table = cur.fetchone()[0]

            if has_logs_table:
                cur.execute("""
                    SELECT timestamp, action, details
                    FROM replication_logs
                    ORDER BY timestamp DESC
                    LIMIT 10;
                """)
                logs = cur.fetchall()

                if logs:
                    result = "Последние логи репликации:\n\n"
                    for log in logs:
                        result += f"{log[0]}\n"
                        result += f"{log[1]}\n"
                        result += f"{log[2]}\n"
                        result += "─" * 30 + "\n"
                else:
                    result = "Логи репликации отсутствуют."
            else:
                result = "Таблица для логов репликации не найдена."

            cur.close()
            conn.close()
            await query.edit_message_text(result)

        except Exception as e:
            await query.edit_message_text(f"Ошибка при получении логов: {str(e)}")


def main():
    application = Application.builder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

    
if __name__ == '__main__':
    main()
