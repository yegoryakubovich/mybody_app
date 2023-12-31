#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from flet_core import ButtonStyle, ElevatedButton, MaterialState, RoundedRectangleBorder, Text, TextAlign, \
    TextThemeStyle

from app.utils import Fonts


class ProductChipButton(ElevatedButton):
    def __init__(self, text, on_click):
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
        self.on_click = on_click

