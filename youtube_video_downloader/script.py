import yt_dlp
from pprint import pprint

def get_video_details(video_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'writeinfojson': True,
        'no_check_formats': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)

        all_formats = info_dict["formats"]
        all_formats_reversed = all_formats.copy()
        all_formats_reversed.reverse()

        video_formats = find_video_formats(all_formats_reversed)
        audio_formats = find_audio_formats(all_formats_reversed)

        # thumbnail = info_dict["thumbnails"][-1]['url']
        return video_formats, audio_formats
    
def find_video_formats(formats):
    video_formats = {}
    for frmt in formats:
        vcodec = frmt.get('vcodec', 'none')
        acodec = frmt.get('acodec', 'none')
        protocol = frmt.get('protocol', 'none')
        if vcodec == 'none' or acodec != 'none' or protocol != 'https':
            continue

        # ext = frmt.get('ext')
        # if ext != 'mp4':
        #     continue

        height = frmt.get('height')
        fps = frmt.get('fps')
        format_key = f"{height}p . {fps}fps"

        video_formats_keys = video_formats.keys()
        if format_key not in video_formats_keys:
            video_formats[format_key] = frmt
        else:
            duplicate_format = video_formats[format_key]
            if duplicate_format['filesize'] < frmt['filesize']:
                video_formats[format_key] = frmt

    return video_formats

def find_audio_formats(formats):
    audio_formats = {}
    for frmt in formats:
        vcodec = frmt.get('vcodec', 'none')
        acodec = frmt.get('acodec', 'none')
        if vcodec != 'none' or acodec == 'none':
            continue

        format = frmt.get('format')
        if 'drc' in format:
            continue
        
        abr = frmt.get('abr')
        format_key = f"{abr}kbp"
        audio_formats[format_key] = frmt

    audio_formats_sorted = sort_audio_formats(audio_formats)
    audio_formats_clean = remove_close_audio_formats(audio_formats_sorted)

    return audio_formats_clean

def sort_audio_formats(audio_formats):
    audio_formats_sorted = {}
    audio_formats_keys = sorted([float(a.split('kbp')[0]) for a in audio_formats], reverse=True)
    for new_format in audio_formats_keys:
        key = f"{new_format}kbp"
        audio_formats_sorted[key] = audio_formats[key]

    return audio_formats_sorted

def remove_close_audio_formats(audio_formats: dict):
    format_keys = list(audio_formats.keys())
    last_key = format_keys[0]
    for key in format_keys[1:]:
        key_num = float(key.split('kbp')[0])
        last_key_num = float(last_key.split('kbp')[0])

        if abs(key_num - last_key_num) < 10:
            format_keys.remove(key)
        else:
            last_key = key

    audio_formats_clean = {}
    for key in format_keys:
        audio_formats_clean[key] = audio_formats[key]
    
    return audio_formats_clean

def show_formats(formats: dict, start_index: int = 0):
    formats_keys = list(formats.keys())
    for i in range(len(formats_keys)):
        frmt = formats[formats_keys[i]]
        filesize = readable_size(frmt['filesize'])
        ext = frmt['ext']
        print(f"[ {start_index + i} ] {formats_keys[i]} . {ext} - {filesize}")

def readable_size(size):
    KB = 1024
    MB = KB * KB
    GB = MB * KB

    if size < MB:
        return f"{size/KB:.2f} KB"
    elif size < GB:
        return f"{size/MB:.2f} MB"
    else:
        return f"{size/GB:.2f} GB"

def find_matching_audio(video_formats, audio_formats, selected_video_format):
    video_qualities = [int(v.split('p')[0]) for v in video_formats]
    audio_qualities = [float(a.split('kbp')[0]) for a in audio_formats]
    selected_video_quality = int(selected_video_format.split('p')[0])

    print()
    print(video_qualities)
    print(audio_qualities)
    print(selected_video_quality)
    print()

    if selected_video_quality == video_qualities[0]:
        return f"{audio_qualities[0]}kbp"
    if selected_video_quality == video_qualities[-1]:
        return f"{audio_qualities[-1]}kbp"

    highest_video_quality = max(video_qualities)
    if highest_video_quality >= 1080:
        matching_audio_qualtiy = match_1080p_or_higher(audio_qualities, selected_video_quality)
    elif highest_video_quality > 480:
        matching_audio_qualtiy = match_up_to_1080p(audio_qualities, selected_video_quality)
    else:
        matching_audio_qualtiy = match_up_to_720p(audio_qualities, selected_video_quality)

    return f"{matching_audio_qualtiy}kbp"
    
def match_1080p_or_higher(audio_qualities, selected_video_quality):
    if selected_video_quality >= 1080:
        return audio_qualities[0]
    if selected_video_quality > 480:
        if audio_qualities[1]:
            return audio_qualities[1]
        else: 
            return audio_qualities[0]
    if audio_qualities[-2]:
        return audio_qualities[-2]
    else:
        return audio_qualities[-1]

def match_up_to_1080p(audio_qualities, selected_video_quality):
    if selected_video_quality >= 480:
        if audio_qualities[1]:
            return audio_qualities[1]
        else:
            return audio_qualities[0]
    if audio_qualities[-2]:
        return audio_qualities[-2]
    else:
        return audio_qualities[-1]

def match_up_to_720p(audio_qualities, selected_video_quality):
    if audio_qualities[1]:
        return audio_qualities[1]
    else:
        return audio_qualities[0]

def download_video(url, video_format_id, audio_format_id):
    if audio_format_id:
        options = {
            'format': f'{video_format_id}+{audio_format_id}',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'merge_output_format': 'mp4',
        }
    else:
        options = {
            'format': video_format_id,
            'outtmpl': '%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=di-VTrW7Kr0'
    # input("Enter the video URL: ")

    video_formats, audio_formats = get_video_details(video_url)

    print()
    show_formats(video_formats)
    video_formats_keys = list(video_formats.keys())

    print()
    show_formats(audio_formats, len(video_formats_keys))
    audio_formats_keys = list(audio_formats.keys())

    matching_audio_format = find_matching_audio(video_formats_keys, audio_formats_keys, video_formats_keys[0])
    # download_video(video_url, video_format_id, audio_format_id)