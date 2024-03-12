import subprocess
import json
import os

##
## Extracts audio from video and splits into 60 second wav audio files.
##

def vid2wav(file,output="wav",save_dict=True):
    """
    Extracts audio from video files and saves it in chunks of 60 seconds, as required in the transcription API.
    """
    vidText = dict()
    audio_name = file.split("/")[-1].split(".")[:-1][0]
    subprocess.run([f"ffmpeg -y -i '{file}' -acodec pcm_s16le -ac 2 '{audio_name}.{output}'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', f"{audio_name}.{output}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        t = int(-(-float(result.stdout.strip())/60 // 1))
        for i in range(t):
            ti = str(datetime.timedelta(minutes=i))
            tf = str(datetime.timedelta(minutes=i,seconds=59))
            min0=str(i).zfill(max(2,len(str(t))))
            command = f"ffmpeg -y -hide_banner -loglevel error -y -ss {ti} -to {tf} -i '{audio_name}.{output}' -ab 160k -ac 2 -ar 44100 -vn 'audio/{audio_name}-{min0}.{output}'"
            subprocess.call(command, shell=True) 
            vidText[f"{min0}:00"] = f"audio/{audio_name}-{min0}.{output}"
        if save_dict:
            with open(f'audio/{audio_name}_split_dict.json', 'w') as file:
                file.write(json.dumps(vidText))
        try:
            subprocess.call(f"rm '{audio_name}.{output}'", shell=True)
        except:
            pass
    except: 
        print("Incorrect file path or format.")









