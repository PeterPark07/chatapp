from youtubesearchpython import VideosSearch
import yt_dlp
import os
import shutil

def search_youtube(query, max_results=1):
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result()
    video_urls = [result['link'] for result in results['result']]
    return video_urls

def download_music(query, download_dir):
    # Ensure the music directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    try:
    
        url = search_youtube(query, max_results=1)[0]
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
    
        return filename

    except Exception as e:
        print(f"Error downloading music: {e}")
        return None


# Delete the folder and its contents
def delete_music_folder(MUSIC_DIR):
    if os.path.exists(MUSIC_DIR):
        shutil.rmtree(MUSIC_DIR)
