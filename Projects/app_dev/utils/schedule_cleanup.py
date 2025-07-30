
import asyncio, os

async def schedule_cleanup(final_file):
            await asyncio.sleep(60 * 15)
            try:
                if os.path.exists(final_file):
                    os.remove(final_file)
                    print(f"Удалён локальный файл: {final_file}")
            except Exception as e:
                print(f"Ошибка удаления файла: {e}")

#from .clean_all import clean_all
#async def schedule_cleanup(file_path):
#    await asyncio.sleep(120)  # ждать 1 минуту
#    print("\n⏳ Удаляем файл с Google Диска и локально...")
#    try:
#        await clean_all()  # удаление с Google Диска
#        if os.path.exists(file_path):
#            os.remove(file_path)
#            print(f"🗑️ Удалён локальный файл: {file_path}")
#        else:
#            print("⚠️ Локальный файл уже удалён.")
#    except Exception as e:
#        print(f"❌ Ошибка при удалении: {e}")

