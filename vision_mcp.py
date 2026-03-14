import mss
import pyautogui
import os
import json
import sys
from datetime import datetime

# Configurações de Segurança: PyAutoGUI fail-safe (mova o mouse para um canto da tela para parar)
pyautogui.FAILSAFE = True

def capture_screen(filename="screenshot.png"):
    """Captura a tela inteira e salva no disco."""
    with mss.mss() as sct:
        # Pega o monitor principal
        monitor = sct.monitors[1]
        sct_img = sct.shot(output=filename)
        return os.path.abspath(filename)

def mouse_click(x, y, relative=False):
    """Clica em uma posição X, Y (absoluta ou relativa 0-100%)."""
    if relative:
        w, h = pyautogui.size()
        x = int((x / 100) * w)
        y = int((y / 100) * h)
    
    pyautogui.click(x, y)
    return f"Clicou em {x}, {y}"

def keyboard_type(text):
    """Digita texto no teclado."""
    pyautogui.write(text, interval=0.1)
    return f"Digitou: {text}"

def get_screen_info():
    """Retorna informações da tela."""
    w, h = pyautogui.size()
    return {"width": w, "height": h}

# Loop de escuta MCP simples (Simulação de MCP para este ambiente CLI)
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "capture":
            path = capture_screen("vision_capture.png")
            print(f"SCREENSHOT_PATH:{path}")
        elif cmd == "click" and len(sys.argv) == 4:
            res = mouse_click(int(sys.argv[2]), int(sys.argv[3]), relative=True)
            print(res)
        elif cmd == "type" and len(sys.argv) == 3:
            res = keyboard_type(sys.argv[2])
            print(res)
        elif cmd == "info":
            print(json.dumps(get_screen_info()))
    else:
        print("Uso: vision_mcp.py [capture | click X Y | type TEXT | info]")
