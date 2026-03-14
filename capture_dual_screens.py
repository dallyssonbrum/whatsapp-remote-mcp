import mss
import os

def capture_all_screens():
    with mss.mss() as sct:
        # Pega a lista de monitores (o monitor [0] eh o conjunto de todos)
        # sct.monitors[1:] sao as telas individuais
        monitor_list = sct.monitors[1:]
        print(f"DEBUG_INFO: Encontrados {len(monitor_list)} monitores.")
        
        paths = []
        for i, monitor in enumerate(monitor_list):
            filename = f"vision_monitor_{i+1}.png"
            sct.shot(mon=i+1, output=filename)
            paths.append(os.path.abspath(filename))
            print(f"SCREENSHOT_MONITOR_{i+1}:{filename}")
        return paths

if __name__ == "__main__":
    capture_all_screens()
