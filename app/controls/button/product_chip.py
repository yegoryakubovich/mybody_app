from flet_core import ButtonStyle, ElevatedButton, FontWeight, MaterialState, RoundedRectangleBorder, Text, TextAlign, \
    TextThemeStyle


class ProductChipButton(ElevatedButton):
    def __init__(self, text):
        super().__init__()
        self.content = Text(
            value=text,
            style=TextThemeStyle.BODY_MEDIUM,
            weight=FontWeight.BOLD,
            text_align=TextAlign.CENTER,
            color='#000000',  # FIXME
        )
        self.style = ButtonStyle(
            shape={MaterialState.DEFAULT: RoundedRectangleBorder(radius=10)},
            padding={},
            overlay_color={
                MaterialState.DEFAULT: '#51B62E',
                MaterialState.HOVERED: '#B3DDB8',  # FIXME
            },
        )
        self.bgcolor = '#B3DDB8'
        self.elevation = 0
        self.height = 25

