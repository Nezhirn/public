from yt_dlp import YoutubeDL

async def list_unique_resolutions(url):
    with YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        resolutions = {}
        for fmt in formats:
            if fmt.get('vcodec') != 'none' and fmt.get('height'):
                height = fmt['height']
                if height not in resolutions or fmt.get('tbr', 0) > resolutions[height].get('tbr', 0):
                    resolutions[height] = fmt
        list_resolutions = []
        for height in sorted(resolutions):
            #fmt = resolutions[height]
            list_resolutions.append(int(height))
        return list_resolutions
