import subprocess
import os
import json

def run_test():
    print("--- Testando Vision MCP ---")
    
    # Teste 1: Info da Tela
    print("Teste 1: Obtendo info da tela...")
    result = subprocess.run(["python", "vision_mcp.py", "info"], capture_output=True, text=True)
    try:
        info = json.loads(result.stdout)
        print(f"✓ Info obtida: {info['width']}x{info['height']}")
    except Exception as e:
        print(f"✗ Falha no Teste 1: {e}")
        return False

    # Teste 2: Captura de Tela
    print("Teste 2: Capturando tela...")
    if os.path.exists("vision_capture.png"):
        os.remove("vision_capture.png")
    
    result = subprocess.run(["python", "vision_mcp.py", "capture"], capture_output=True, text=True)
    if os.path.exists("vision_capture.png") and "SCREENSHOT_PATH" in result.stdout:
        print("✓ Captura realizada com sucesso.")
    else:
        print(f"✗ Falha no Teste 2: {result.stdout} {result.stderr}")
        return False

    print("--- Todos os testes de Visão passaram! ---")
    return True

if __name__ == "__main__":
    if run_test():
        exit(0)
    else:
        exit(1)
