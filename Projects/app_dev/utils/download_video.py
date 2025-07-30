from yt_dlp import YoutubeDL
import os
#from .upload_file import upload_file
#from .get_file_link import get_file_link

dir='/home/andrew/video_downloader/temp_files/'

async def download_video(
    url: str,
    height: int
):
    os.makedirs(dir, exist_ok=True)

    ydl_opts = {
        'format': f'bestvideo[height<={height}]+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(dir, '%(title)s.%(ext)s'),
        'quiet': True
    }

    final_file = None

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # Получаем путь до итогового файла
        if 'requested_downloads' in info and info['requested_downloads']:
            final_file = info['requested_downloads'][0].get('_filename')
        else:
            # fallback
            final_file = ydl.prepare_filename(info)

    try:
        filename_only = os.path.basename(final_file)
        print(f"\nПуть до итогового файла: {final_file}")
        print(f"Название итогового файла: {filename_only}")
        return final_file
    except Exception as e:
        print(f"Ошибка {e}")