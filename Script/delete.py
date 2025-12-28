import threading, time, os

def delete_later(path, delay=300) :
    print(f"Deleting {path}")
    def _() :
        time.sleep(delay)
        if os.path.exists(path) :
            os.remove(path)
            print(f"{path} deleted successfully")
    threading.Thread(target=_).start()