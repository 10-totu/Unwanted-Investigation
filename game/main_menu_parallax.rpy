## -- Store mouse position -- 
default persistent.mx = 0.5
default persistent.my = 0.5

## -- PYTHON: Read<Mouse_position>-- 
init python:
    import pygame

    class ParallaxLayer(renpy.Displayable):
        """
        Wraps a child displayable and offsets it based on the
        current mouse position.

        mx_factor / my_factor control how many pixels the layer
        shifts when the cursor moves from centre to edge.
        Positive values move in the direction of the cursor;
        negative values move opposite (classic parallax feel).
        """
        def __init__(self, child, mx_factor=20, my_factor=12, **kwargs):
            super(ParallaxLayer, self).__init__(**kwargs)
            self.child   = renpy.displayable(child)
            self.mx_factor = mx_factor
            self.my_factor = my_factor

        def render(self, width, height, st, at):
            # Normalise mouse to -1 … +1 (centre = 0)
            mx, my = renpy.get_mouse_pos()
            nx = (mx / float(config.screen_width))  * 2 - 1
            ny = (my / float(config.screen_height)) * 2 - 1

            ox = int(nx * self.mx_factor)
            oy = int(ny * self.my_factor)

            # Render child slightly larger so edges never show
            pad = max(abs(self.mx_factor), abs(self.my_factor)) + 4
            child_render = renpy.render(
                self.child,
                width  + pad * 2,
                height + pad * 2,
                st, at
            )

            rv = renpy.Render(width, height)
            rv.blit(child_render, (-pad + ox, -pad + oy))

            # Keep redrawing so motion stays responsive
            renpy.redraw(self, 0)
            return rv

        def event(self, ev, x, y, st):
            return self.child.event(ev, x, y, st)

        def visit(self):
            return [self.child]


## ── Convenience functions ────────────────────────────────────
init python:
    def parallax(child, mx=20, my=12):
        """Return a ParallaxLayer displayable."""
        return ParallaxLayer(child, mx_factor=mx, my_factor=my)


## ── Colours & style ──────────────────────────────────────────
init python:
    # Colour palette
    C_TITLE   = "#ffffff"   
    C_ACCENT  = "#e03f3f"   
    C_TEXT    = "#fffefc"  
    C_BTN_BG  = "#000000cc" 
    C_BTN_HVR = "#22222222" 
    C_BTN_TXT = "#ffffff"
    C_BTN_LIN = "#ff0000"

## ── Button style ─────────────────────────────────────────────
style main_menu_button:
    background      Frame(Solid(C_BTN_BG), 0, 0)
    hover_background Frame(Solid(C_BTN_HVR), 0, 0)
    xpadding 40
    ypadding 14
    xminimum 220

style main_menu_button_text:
    font         "gui/font/Oxford.ttf"  #FONT
    size         26
    color        C_BTN_TXT
    hover_color  C_ACCENT
    selected_color C_ACCENT
    outlines     [(1, "#00000088", 1, 1)]
    kerning      3.0

## ── Main menu screen ─────────────────────────────────────────
screen main_menu():
    tag menu

    # ── Layer 0 – deepest background (moves least) ──────────
    add parallax(
        "images/menu_bg/menu_bg_far.png",   # far background
        mx=8, my=5
    ) xpos 0 ypos 0

    # ── Layer 1 – midground ─────────────────────────────────
    add parallax(
        "images/menu_bg/menu_bg_mid.png",   # midground element
        mx=22, my=16
    ) xpos 0 ypos 0

    # ── Layer 2 – foreground details (moves most) ───────────
    add parallax(
        "images/menu_bg/menu_bg_fore.png",  # foreground element
        mx=35, my=22
    ) xpos 0 ypos 0

    # ── Vignette overlay ────────────────────────────────────
    add Solid("#00000055") xpos 0 ypos 0

    ## ── UI content ─────────────────────────────────────────
    vbox:
        xalign 0.15
        yalign 0.50
        spacing 6

        # Game title
        text "Unwanted Investigation--VERSION 0.001":
            style "main_menu_button_text"
            size 72
            color C_TITLE
            outlines [(2, "#00000099", 2, 2)]
            yoffset -10


        null height 40

        # Menu buttons
        textbutton "New Game":
            hover_sound "audio/hover_b.mp3"
            style "main_menu_button"
            action [Play("sound", "hover_a.mp3"), Start()] 

        null height 4

        textbutton "Load Game":
            hover_sound "audio/hover_b.mp3"
            style "main_menu_button"
            action ShowMenu("load")

        null height 4

        textbutton "Preferences":
            hover_sound "audio/hover_b.mp3"
            style "main_menu_button"
            action ShowMenu("preferences")

        null height 4

        textbutton "About":
            hover_sound "audio/hover_b.mp3"
            style "main_menu_button"
            action ShowMenu("about")

        null height 4

        textbutton "Quit":
            hover_sound "audio/hover_b.mp3"
            style "main_menu_button"
            action Quit(confirm=True)

    # ── Corner version label ─────────────────────────────────
    text "v1.0":
        xalign 0.99
        yalign 0.99
        style "main_menu_button_text"
        size 14
        color C_TEXT


## ── Override default main_menu ───────────────────────────────
## This tells Ren'Py to use our screen instead of the default one.
define config.main_menu_music = "audio/menu_theme.ogg"  # optional


