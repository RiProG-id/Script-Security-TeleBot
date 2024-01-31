import os
import zipfile
import re
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

TOKEN = 'YOUR_BOT_TOKEN'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Halo! Terima kasih sudah memulai bot ini. Source Code: [GitHub](https://github.com/RiProG-id/Script-Security-TeleBot)', disable_web_page_preview=True)

def welcome(update: Update, context: CallbackContext) -> None:
    if update.message.new_chat_members:
        for _ in update.message.new_chat_members:
            update.message.reply_text('Halo! Terima kasih telah menambahkan saya ke grup. Source Code: [GitHub](https://github.com/RiProG-id/Script-Security-TeleBot)', disable_web_page_preview=True)

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
    dangerous_patterns = [
        r'\b(rm\s*-rf|if=/dev/null|cmd\s+erase|apparmor|setenforce|shred\s*-f|ufw\s+disable|iptables\s+-F|setfacl|:(){ :|:& };:)\b',
    ]

    for pattern in dangerous_patterns:
        match = re.search(pattern, content.decode('utf-8'))
        if match:
            return match.group()

    return None
    
def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    file_id = document.file_id
    file = context.bot.get_file(file_id)

    if document.file_size > 5 * 1024 * 1024:
        update.message.reply_text('❌ File size exceeds the limit (5MB). Please try again with a smaller file.')
        return

    try:
        file_path = os.path.join('temp_folder', document.file_name)
        file.download(file_path)
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

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.command, welcome))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, start))
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
