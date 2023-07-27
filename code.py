print("Starting")

import board
import digitalio
import ulab.numpy as np
import usb_hid

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.modules.encoder import EncoderHandler
from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.modules.layers import Layers
from kmk.modules.potentiometer import PotentiometerHandler
from kmk.modules.midi import MidiKeys


encoder_handler = EncoderHandler()

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys(),)
keyboard.modules = [encoder_handler,]
keyboard.modules.append(Layers())
keyboard.modules.append(MidiKeys())

keyboard.SCL=board.GP3
keyboard.SDA=board.GP2

keyboard.col_pins = (board.GP1, board.GP5, board.GP8, board.GP10, board.GP21,)
keyboard.row_pins = (board.GP6, board.GP15, board.GP16, board.GP17, board.GP18,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.debug_enabled = True

keyboard.last_level = -1

# Windows 10
level_steps = 50
level_inc_step = 2

level_lut = [int(x) for x in np.linspace(0, level_steps, 52).tolist()]

VOL_UP = simple_key_sequence(
    (
        KC.VOLU, 
        KC.MACRO_SLEEP_MS(1),
        KC.VOLU,
    )
)

VOL_DOWN = simple_key_sequence(
    (
        KC.VOLD, 
        KC.MACRO_SLEEP_MS(1),
        KC.VOLD,
    )
)

def set_sys_vol(state):
    # convert to 0-100
    new_pos = int((state.position/127)*40)
    level = level_lut[new_pos]
    print(f"new vol level: {level}")
    # print(f"last: {keyboard.last_level}")

    # check if uninitialized
    if keyboard.last_level == -1:
        keyboard.last_level = level
        return

    level_diff = abs(keyboard.last_level - level)
    cmd = None
    if level_diff > 0:
        # set volume to new level
        vol_direction = "unknown"
        if level > keyboard.last_level:
            vol_direction = "down"
            cmd = KC.VOLU
        else:
            vol_direction = "up"
            cmd = KC.VOLD
        
        print(f"Setting system volume {vol_direction} by {level_diff} to reach {level}")
        if vol_direction == "up":
            keyboard.tap_key(VOL_UP)
        elif vol_direction == "down":
            keyboard.tap_key(VOL_DOWN)
            
            

        keyboard.last_level = level
    return

def potentiometer_1_handler(state):
    val = 127 - state.position
    if state.position >= 125:
        val = 0
    elif state.position <= 2:
        val = 127
    keyboard.tap_key(KC.MIDI_CC(1, val))
    #set_sys_vol(state)
    
def potentiometer_2_handler(state):
    val = 127 - state.position
    if state.position >= 125:
        val = 0
    elif state.position <= 2:
        val = 127
    keyboard.tap_key(KC.MIDI_CC(2, val))
    
faders = PotentiometerHandler()
faders.pins = (
    (board.A0, potentiometer_1_handler, False),
    (board.A1, potentiometer_2_handler, False),
)
keyboard.modules.append(faders)
    

mute_mic = KC.LWIN(KC.LALT(KC.K))
email = send_string("martijn12358@gmail.com")
switch_window = KC.LALT(KC.TAB)

encoder_handler.pins = ((board.GP14, board.GP0, None,),
                        (board.GP11, board.GP9, None,),
                        (board.GP20, board.GP19, None,),)

keyboard.keymap = [
    [KC.F14, KC.A,KC.A,KC.M, KC.AUDIO_MUTE,
     KC.MEDIA_PREV_TRACK, KC.MEDIA_NEXT_TRACK, KC.MEDIA_PLAY_PAUSE,KC.A, mute_mic,
     email, KC.A,KC.A,KC.A,KC.A,
     KC.F13, KC.A,KC.A,KC.A,KC.A,
     switch_window, KC.F16,KC.A,KC.A,KC.A,]
]

encoder_handler.map = [ ((KC.UP, KC.DOWN,),(KC.LEFT, KC.RIGHT,),(KC.UP, KC.DOWN,),),
                     ]

oled_ext = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC,1:["layer"]},
        corner_two={0:OledReactionType.LAYER,1:["1","2","3","4"]},
        corner_three={0:OledReactionType.LAYER,1:["base","raise","lower","adjust"]},
        corner_four={0:OledReactionType.LAYER,1:["qwerty","nums","shifted","leds"]}
        ),
        toDisplay=OledDisplayMode.TXT,flip=False)
keyboard.extensions.append(oled_ext)

if __name__ == '__main__':
    keyboard.go()
          