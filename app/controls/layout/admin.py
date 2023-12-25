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


from flet_core import Image, Container, padding, alignment, MainAxisAlignment, Row, Column
from flet_manager.utils import get_svg

from app.controls.information import Text
from app.controls.layout.view import View
from app.utils import Fonts


class AdminView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 0
        self.spacing = 0

    async def get_title(self, title: str, on_create_click=None, create_button=True):

        async def go_back(_):
            await self.client.change_view(go_back=True)

        left_controls = [
            Container(
                content=Image(
                    src=get_svg(path='assets/icons/arrow_back.svg'),
                    height=20,
                    color='#000000',
                ),
                ink=True,
                on_click=go_back,
            ),
            Text(
                value=title,
                size=36,
                font_family=Fonts.SEMIBOLD,
            ),
        ]

        right_controls = []

        if create_button:
            right_controls.append(
                Container(
                    content=Row(
                        controls=[
                            Container(
                                content=Image(
                                    src=get_svg(path='assets/icons/addition.svg'),
                                    height=13,
                                    color='#FFFFFF',
                                ),
                                ink=True,
                                on_click=self.client.change_view(go_back=True),
                            ),
                            Text(
                                value='Create',
                                size=13,
                                font_family=Fonts.SEMIBOLD,
                                color='#FFFFFF',
                            ),
                        ],
                    ),
                    padding=5,
                    border_radius=24,
                    bgcolor='#008F12',
                    on_click=on_create_click,
                )
            )

        return Row(
            controls=[
                Container(
                    content=Row(controls=left_controls),
                ),
                Container(
                    content=Row(controls=right_controls),
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

    async def get_controls(
            self,
            controls: dict = None,
            title: str = None,
            on_create_click=None,
            create_button=True
    ) -> list:

        title_controls = await self.get_title(title, on_create_click, create_button)

        body_controls = []

        if controls is not None:
            if 'textfields' in controls:
                for textfield in controls['textfields']:
                    body_controls.append(textfield)

            if 'dropdowns' in controls:
                for dropdown in controls['dropdowns']:
                    body_controls.append(dropdown)

            if 'buttons' in controls:
                body_controls.append(Row(controls=controls['buttons']))

            if 'cards' in controls:
                for card in controls['cards']:
                    body_controls.append(card)

        controls = [
            Container(
                content=Column(
                    controls=[
                                 # Header
                                 Container(
                                     content=Image(
                                         src=get_svg(
                                             path='assets/icons/logos/logo_2_full.svg',
                                         ),
                                         height=56,
                                     ),
                                     alignment=alignment.center,
                                     padding=padding.symmetric(vertical=32, horizontal=96),
                                 ),
                                 # Body
                                 title_controls,
                             ] + body_controls,
                    width=640,
                ),
                expand=True,
                alignment=alignment.center,
            ),
        ]
        return controls
