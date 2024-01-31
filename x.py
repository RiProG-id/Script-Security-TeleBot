import os
import zipfile
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

TOKEN = 'YOUR_BOT_TOKEN'

def create_temp_folder():
    if not os.path.exists('temp_folder'):
        os.makedirs('temp_folder')

def delete_temp_files():
    for file_name in os.listdir('temp_folder'):
        file_path = os.path.join('temp_folder', file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f'Error while deleting temp files: {e}')

def scan_zip(file_path):
    detected_codes = []
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            file_content = zip_ref.read(file_info.filename)
            detected_code = detect_dangerous_code(file_content)
            if detected_code:
                detected_codes.append(f'⚠️ File {file_info.filename} dalam ZIP mengandung kode berbahaya: {detected_code}')
    return detected_codes

def scan_sh(sh_content):
    detected_code = detect_dangerous_code(sh_content)
    if detected_code:
        return f'⚠️ File skrip berbahaya mengandung kode: {detected_code}'
    return None

def detect_dangerous_code(content):
    match = re.search(rb'\b(rm -rf|if=/dev/)\b', content)
    return match.group().decode('utf-8') if match else None

def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    file_id = document.file_id
    file = context.bot.get_file(file_id)

    create_temp_folder()

    if document.file_size > 5 * 1024 * 1024:
        return

    try:
        file_path = file.download()
    except FileNotFoundError:
        update.message.reply_text('❌ File not found. Please try again.')
        return

    if file_path.endswith('.zip'):
        results = scan_zip(file_path)
        if results:
            for result in results:
                update.message.reply_text(result)
        else:
            update.message.reply_text('✅ Pemindaian ZIP telah selesai.')
    elif file_path.endswith('.sh'):
        with open(file_path, 'rb') as sh_file:
            sh_content = sh_file.read()
            result = scan_sh(sh_content)
            if result:
                update.message.reply_text(result)
            else:
                update.message.reply_text('✅ File skrip aman.')
    else:
        pass

    delete_temp_files()

def start_scan(update: Update, context: CallbackContext) -> None:
    pass

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.document, handle_document))
    dp.add_handler(CommandHandler("start_scan", start_scan))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()