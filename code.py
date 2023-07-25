print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.peg_oled_Display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.modules.encoder import EncoderHandler
encoder_handler = EncoderHandler()

keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys(),) 
keyboard.modules = [encoder_handler]

keyboard.SCL=board.GP3
keyboard.SDA=board.GP2

keyboard.col_pins = (board.GP1, board.GP5, board.GP8, board.GP10, board.GP21,)
keyboard.row_pins = (board.GP6, board.GP15, board.GP16, board.GP17, board.GP18,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.debug_enabled = True

mute_mic = KC.LWIN(KC.LALT(KC.K))

encoder_handler.pins = ((board.GP14, board.GP0, None,),
                        (board.GP11, board.GP9, None,),
                        (board.GP20, board.GP19, None,),)

keyboard.keymap = [
    [KC.A, KC.A,KC.A,KC.A, mute_mic,
     KC.MEDIA_PREV_TRACK, KC.MEDIA_NEXT_TRACK, KC.MEDIA_PLAY_PAUSE,KC.A,KC.AUDIO_MUTE,
     KC.A, KC.A,KC.A,KC.A,KC.A,
     KC.A, KC.A,KC.A,KC.A,KC.A,
     KC.A, KC.A,KC.A,KC.A,KC.A,]
]

encoder_handler.map = [ ((KC.UP, KC.DOWN,),(KC.UP, KC.DOWN,),(KC.UP, KC.DOWN,),),
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
    
    