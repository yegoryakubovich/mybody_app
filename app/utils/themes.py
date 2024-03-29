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


from flet_core import Theme, ColorScheme, PageTransitionsTheme, PageTransitionTheme, TextTheme

from flet_manager.utils import Themes


page_transitions = PageTransitionsTheme(
    android=PageTransitionTheme.CUPERTINO,
    ios=PageTransitionTheme.CUPERTINO,
    linux=PageTransitionTheme.CUPERTINO,
    macos=PageTransitionTheme.CUPERTINO,
    windows=PageTransitionTheme.CUPERTINO,
)


themes = Themes(
    light=Theme(
        color_scheme=ColorScheme(
            background='#FFFFFF',
            on_background='#000000',
            primary='#008F12',
            on_primary='#FFFFFF',
            primary_container='#B3E5B9',
            on_primary_container='#005B0C',
            secondary='#008F12',
            secondary_container='#008F12',
            shadow='#DDDDDD',
            surface='#CDEBD1',
            on_surface='#000000',

        ),
        text_theme=TextTheme(),
        page_transitions=page_transitions,
    ),
    dark=Theme(
        color_scheme=ColorScheme(
            background='#383838',
            on_background='#FFFFFF',
            primary='#008F12',
            on_primary='#FFFFFF',
            primary_container='#B3E5B9',
            on_primary_container='#005B0C',
            secondary='#008F12',
            secondary_container='#008F12',
            shadow='#292929',
            surface='#CDEBD1',
            on_surface='#000000',
        ),
        page_transitions=page_transitions,
    ),
)
