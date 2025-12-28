import subprocess
import sys

def merge_video_srt(video_path, srt_path, output_path) :
    try :
        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"subtitles={srt_path}",
            "-c:a", "copy",
            output_path
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception as e :
        print("Erreur lors de la merge video+srt : "+str(e), file=sys.stderr, flush=True)
        return False
