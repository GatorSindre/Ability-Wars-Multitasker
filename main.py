import socket
import keyboard

TARGET_IP = "192.168.50.103"
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def SendSignal(message):
    sock.sendto(message.encode("utf-8"), (TARGET_IP, PORT))
    print(f"Sent {message} to {TARGET_IP}")

name = ""

def player_target(message):
    global name
    name = ""
    def handle_key(key_event):
        global name
        if key_event.name == "enter":
            SendSignal(f"{message}{name[1:]}")
            name = ""
            keyboard.unhook(hook)
        elif key_event.name in ("skift", "ctrl", "alt"):
            return
        elif (key_event.event_type == "down"):
            name += key_event.name
            print(f"{name}")
    hook = keyboard.hook(handle_key)

keyboard.add_hotkey('ctrl+t', lambda: SendSignal("e-portal steve"))
keyboard.add_hotkey('ctrl+v', lambda: player_target("e-portal "))

keyboard.add_hotkey('ctrl+f', lambda: SendSignal("e-press"))
keyboard.add_hotkey('ctrl+b', lambda: SendSignal("q-press"))

keyboard.add_hotkey('ctrl+l', lambda: SendSignal("farm steve"))
keyboard.add_hotkey('ctrl+k', lambda: player_target("farm "))

keyboard.add_hotkey('ctrl+y', lambda: SendSignal("heal"))
keyboard.add_hotkey('ctrl+u', lambda: SendSignal("home"))

keyboard.add_hotkey('ctrl+m', lambda: SendSignal("cancel"))
keyboard.add_hotkey('ctrl+n', lambda: SendSignal("enablehacks"))
keyboard.add_hotkey('ctrl+h', lambda: SendSignal("disablehacks"))

keyboard.wait()