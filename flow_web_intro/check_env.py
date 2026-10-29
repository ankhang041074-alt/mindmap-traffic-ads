import importlib.util
import shutil

mods = ["websockets", "websocket", "playwright", "PIL", "cv2", "aiohttp"]
print({m: bool(importlib.util.find_spec(m)) for m in mods})
print("ffmpeg:", shutil.which("ffmpeg"))
print("ffprobe:", shutil.which("ffprobe"))
