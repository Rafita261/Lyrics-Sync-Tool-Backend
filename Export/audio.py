import subprocess

def ffmpeg_exists() :
    try :
        subprocess.run(["ffmpeg","h"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(str(e))
        return False