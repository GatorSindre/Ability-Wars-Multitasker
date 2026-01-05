import socket
import time
import pyautogui
import keyboard
import sys

canceled = False

PORT = 5005
HostCredentials = ('192.168.50.101', 55592)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print(f"Listening on {PORT}")

def EmulatorWrite(text):
    print(f"Writing '{text}")
    for char in text:
        pyautogui.press(char)
        time.sleep(0.01)

focusCoords = ((558, 154), (0, 0))
def Focus(window):
    coords = focusCoords[window]
    pyautogui.click(coords[0], coords[1])
    print(f"Focus {window}")

yieldCoords = ((483, 124), (0, 0))
def Yield(window):
    coords = yieldCoords[window]
    pyautogui.click(coords[0], coords[1])
    print(f"Yield {window}")

def e_press(window):
    Focus(window)
    keyboard.press("e")
    time.sleep(0.1)
    keyboard.release("e")

def q_press(window):
    Focus(window)
    keyboard.press("q")
    time.sleep(0.05)
    keyboard.release("q")


e_ability_coords = ((787, 176), (0, 0))
def e_ability(window):
    coords = e_ability_coords[window]
    pyautogui.click(coords[0], coords[1])
    print(f"Ability {window}")

def E_Portal(player):
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"grounddeep {player}")
    keyboard.press_and_release("enter")
    time.sleep(0.1)
    e_press(0)
    time.sleep(0.05)
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"wp home")
    time.sleep(0.5)
    keyboard.press_and_release("enter")
    time.sleep(0.05)

def E_Portal_Closest():
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"groundclosest")
    keyboard.press_and_release("enter")
    time.sleep(0.1)
    e_press(0)
    time.sleep(0.05)
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"wp home")
    keyboard.press_and_release("enter")
    time.sleep(0.05)

def Farm(player):
    global canceled
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"loopgoto {player}")
    keyboard.press_and_release("enter")
    time.sleep(0.1)
    while not canceled:
        data, addr = sock.recvfrom(1024)
        message = data.decode().strip()

        if message == "cancel":
            canceled = True
    canceled = False
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"unloopgoto")
    keyboard.press_and_release("enter")
    time.sleep(1)
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"wp home")
    keyboard.press_and_release("enter")
    time.sleep(0.1)

def Heal():
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"wp heal")
    keyboard.press_and_release("enter")
    time.sleep(0.1)

def Home():
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"wp home")
    keyboard.press_and_release("enter")
    time.sleep(0.1)

def Kidnap(player):
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"kidnap {player}")
    keyboard.press_and_release("enter")
    time.sleep(4)
    e_ability(0)

def EnableHacks():
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"float")
    keyboard.press_and_release("enter")

    time.sleep(0.2)

    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"noclip")
    keyboard.press_and_release("enter")

def DisableHacks():
    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"unfloat")
    keyboard.press_and_release("enter")

    time.sleep(0.2)

    Yield(0)
    time.sleep(0.2)
    EmulatorWrite(f"clip")
    keyboard.press_and_release("enter")


def handle_key(key_event):
    if key_event.event_type == 'down' and key_event.name == "å":
        Kidnap("steve")
keyboard.hook(handle_key)

def decypher_message(parts):
    if parts[0] == "kidnap":
        Kidnap(message_parts[1])   
    elif parts[0] == "e-portal":
        E_Portal(parts[1])
    elif parts[0] == "portal-closest":
        E_Portal_Closest()
    elif parts[0] == "e-press":
        e_press(0)
    elif parts[0] == "q-press":
        q_press(0)
    elif parts[0] == "enablehacks":
        EnableHacks()
    elif parts[0] == "disablehacks":
        DisableHacks()
    elif parts[0] == "farm":
        Farm(parts[1])
    elif parts[0] == "home":
        Home()
    elif parts[0] == "heal":
        Heal()


while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode().strip()
    
    print(f"Received '{message}' from {addr}")

    if addr[0] == HostCredentials[0]:
        message_parts = message.split(" ")
        decypher_message(message_parts)
    else:
        print("UNAUTHORIZED SIGNAL DETECTED --- EXITING PROGRAM...")
        sys.exit(0)
