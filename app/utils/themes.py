#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
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


from flet_core import ColorScheme, ScrollbarTheme, TextStyle, TextTheme, Theme, colors


BASE_TEXT_STYLE = TextStyle(
    font_family='Regular',
    color='black',
)
PRIMARY_COLOR_LIGHT = 'BLACK'
PRIMARY_COLOR_DARK = 'WHITE'
BG_COLOR_LIGHT = 'WHITE'
BG_COLOR_DARK = 'BLACK'
SECONDARY_COLOR_LIGHT = colors.GREY_700
SECONDARY_COLOR_DARK = colors.GREY_300


class Themes:
    LIGHT = Theme(
        color_scheme=ColorScheme(
            surface=BG_COLOR_LIGHT,
            surface_tint=BG_COLOR_LIGHT,
            primary=SECONDARY_COLOR_LIGHT,
            on_surface=PRIMARY_COLOR_LIGHT,
            on_primary=PRIMARY_COLOR_LIGHT,
            secondary_container=BG_COLOR_LIGHT,
            on_secondary_container=PRIMARY_COLOR_LIGHT,
            on_secondary=BG_COLOR_LIGHT,
            outline=PRIMARY_COLOR_LIGHT,
        ),
        text_theme=TextTheme(
            label_medium=BASE_TEXT_STYLE,
            label_large=BASE_TEXT_STYLE,
            label_small=BASE_TEXT_STYLE,
            body_small=BASE_TEXT_STYLE,
            body_medium=BASE_TEXT_STYLE,
            body_large=BASE_TEXT_STYLE,
        ),
        scrollbar_theme=ScrollbarTheme(
            track_color=PRIMARY_COLOR_LIGHT,
            track_border_color=PRIMARY_COLOR_LIGHT,
            thickness=0
        )
    )
    DARK = Theme(
        color_scheme=ColorScheme(
            surface=BG_COLOR_DARK,
            surface_tint=BG_COLOR_DARK,
            primary=SECONDARY_COLOR_DARK,
            on_surface=PRIMARY_COLOR_DARK,
            on_primary=PRIMARY_COLOR_DARK,
            secondary_container=BG_COLOR_DARK,
            on_secondary_container=PRIMARY_COLOR_DARK,
            on_secondary=BG_COLOR_DARK,
            outline=PRIMARY_COLOR_DARK,
        ),
        text_theme=TextTheme(
            label_medium=BASE_TEXT_STYLE,
            label_large=BASE_TEXT_STYLE,
            label_small=BASE_TEXT_STYLE,
            body_small=BASE_TEXT_STYLE,
            body_medium=BASE_TEXT_STYLE,
            body_large=BASE_TEXT_STYLE,
        ),
        scrollbar_theme=ScrollbarTheme(
            track_color=PRIMARY_COLOR_DARK,
            track_border_color=PRIMARY_COLOR_DARK,
            thickness=0
        )
    )



