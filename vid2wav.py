import subprocess

##
## Extracts audio from video and splits into 60 second wav audio files.
##

def vid2wav(file,output="wav"):
    audio_name = file.split("/")[-1].split(".")[:-1][0]
    subprocess.run([f"ffmpeg -y -i '{file}' -acodec pcm_s16le -ac 2 '{audio_name}.{output}'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', f"{audio_name}.{output}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        t = int(-(-float(result.stdout.strip())/60 // 1))
        for i in range(t):
            ti = str(datetime.timedelta(minutes=i))
            tf = str(datetime.timedelta(minutes=i,seconds=59))
            command = f"ffmpeg -y -hide_banner -loglevel error -y -ss {ti} -to {tf} -i '{audio_name}.{output}' -ab 160k -ac 2 -ar 44100 -vn 'audio/{audio_name}-{str(i).zfill(len(str(t)))}.{output}'"
            subprocess.call(command, shell=True) 
        try:
            subprocess.call(f"rm '{audio_name}.{output}'", shell=True)
        except:
            pass
    except: 
        print("Incorrect file path or format.")










