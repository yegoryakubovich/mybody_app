from flet_core import ButtonStyle, ElevatedButton, MaterialState, RoundedRectangleBorder, Text, TextAlign, \
    TextThemeStyle

from app.utils import Fonts


class ProductChipButton(ElevatedButton):
    def __init__(self, text):
        super().__init__()
        self.content = Text(
            value=text,
            style=TextThemeStyle.BODY_MEDIUM,
            font_family=Fonts.MEDIUM,
            text_align=TextAlign.CENTER,
            color='#000000',  # FIXME
        )
        self.style = ButtonStyle(
            shape={MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
            overlay_color={
                MaterialState.DEFAULT: '#51B62E',
                MaterialState.HOVERED: '#B3DDB8',  # FIXME
            },
        )
        self.bgcolor = '#B3DDB8'
        self.elevation = 0
        self.height = 25

