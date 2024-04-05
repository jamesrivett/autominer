import keyboard as kb
import mouse
import time, threading

minerState = False
hitterState = False
lastEnable = 0
debounce = .5


def enableMiner():
    global minerState
    global lastEnable

    assert(not minerState)
    minerState = True
    print("MINER ON")
    mouse.press(button='left')
    kb.press('w')
    lastEnable = time.time()

def disableMiner():
    global minerState
    mouse.release(button='left')
    kb.release('w')
    minerState = False
    print("MINER OFF")

def enableHitter():
    global hitterState
    global lastEnable

    assert(not hitterState)
    hitterState = True
    print("HITTER ON")
    lastEnable = time.time()

def disableHitter():
    global hitterState 
    hitterState = False
    print("HITTER OFF")

def hitLoop():
    global hitterState
    if hitterState:
        mouse.click()
    threading.Timer(1, hitLoop).start()
        


def deadman(event):
    global minerState
    global hitterState
    global lastEnable

    if (minerState or hitterState) and (time.time() - lastEnable) > debounce:
        disableHitter()
        disableMiner()

def deadmanMouse():
    global minerState
    global hitterState
    global lastEnable

    if minerState and (time.time() - lastEnable) > debounce:
        disableHitter()
        disableMiner()

def main():
    hitLoop()
    kb.add_hotkey('ctrl+shift+M', lambda: enableMiner())
    kb.add_hotkey('ctrl+shift+H', lambda: enableHitter())
    kb.on_press(deadman)
    mouse.on_click(deadmanMouse)
    kb.wait()


if __name__ == "__main__":
    main()