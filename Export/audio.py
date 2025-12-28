import subprocess
import sys

def ffmpeg_exists() :
    try :
        subprocess.run(["ffmpeg","-version"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
        return True
    except Exception as e:
        print("Erreur : " + str(e), file=sys.stderr, flush=True)
        return False

def merge_audio_lrc(audio_path, lrc_path, output_path) :
    try :
        lyrics = open(lrc_path, 'r', encoding='utf-8').read()
        cmd = [
            "ffmpeg",
            "-y",
            "-i", audio_path,
            "-metadata", f"lyrics={lyrics}",
            "-c:a", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e :
        print("Erreur ffmpeg : "+str(e), file=sys.stderr, flush=True)
        return False

def audio_to_lyrics_video(audio, srt, bg, output) :
    try :
        cmd = [
            "ffmpeg", "-y",
	    "-xerror",
            "-loop", "1",
            "-i", str(bg),
            "-i", str(audio),
            "-vf", f"subtitles={srt}",
            "-c:a","copy",
            "-shortest",
            output
        ]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e :
        print("Erreur : "+str(e), file=sys.stderr, flush=True)
        return False



if __name__ == '__main__' :
    print(ffmpeg_exists())
