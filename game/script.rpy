#Initialize Speech-Blip

init python:
    def speech_blip(event, **kwargs):
        if event == "show":
            # Loops sound
            renpy.sound.play("blip.wav", channel="sound", loop=True)
        elif event == "slow_done" or event == "end":
            # END sound/line finished
            renpy.sound.stop(channel="sound")

 

define arthur = Character("Arthur Slivaro",callback=speech_blip)
define lain = Character("Lain Sterling",callback=speech_blip)

transform flip_right:
    xzoom -1.0 
    xalign 1.0 
    yalign 1.0
 

# Start game.

label start:

    play music theme_b

    show lain_neutral at center

    # dialouge.
    lain "..."
    lain "...."
    lain "Where....Am I?"
    show lain_neutral at left with moveinleft
    show arthur_smirk at flip_right with dissolve
    arthur "Hmm..."
    arthur "Maybe our lord and saviour Emma has not programmed a proper place for us to be yet"
    lain "AHHH!!!"
    arthur "What--? Whats wrong Lain?"
    lain "WHAT HAPPENED TO YOU WHY ARE YOU SO LOW QUALITY?"
    arthur "I had the same question about you... You don't look as handsome as I remember.."
    lain "...Well, maybe Emma hasnt made us proper sprites either..."
    arthur"Never mind that, Your right. lets give her time and we will look beautiful!!11!"

    # end the game or something idk

    return
