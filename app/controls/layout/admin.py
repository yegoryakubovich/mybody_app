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


from typing import Any

from flet_core import Row, Container, Image, MainAxisAlignment, Column, margin, colors

from app.controls.information import Text
from app.controls.layout.view import View
from app.utils import Fonts, Icons


class Section:
    title: str
    controls: list
    create_button: Any = None

    def __init__(self, title: str, controls: list, create_button: Any = None, ):
        self.title = title
        self.controls = controls
        self.create_button = create_button

    @staticmethod
    async def get_title(title: str, create_button: Any = None):
        controls = [
            Text(
                value=title,
                size=36,
                font_family=Fonts.SEMIBOLD,
                color=colors.ON_BACKGROUND,
            ),
        ]

        if create_button:
            controls.append(
                Container(
                    content=Row(
                        controls=[
                            Image(
                                src=Icons.CREATE,
                                height=10,
                                color='#FFFFFF',
                            ),
                            Text(
                                value='Create',
                                size=13,
                                font_family=Fonts.SEMIBOLD,
                                color='#FFFFFF',
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=7,
                    border_radius=24,
                    bgcolor='#008F12',
                    on_click=create_button,
                ),
            )

        return Row(
            controls=controls,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

    async def get_controls(self) -> list:
        title_control = await self.get_title(title=self.title, create_button=self.create_button)

        controls = [
            Container(
                content=Column(
                    controls=[
                        title_control,
                        *self.controls,
                    ],
                    spacing=8,
                ),
                padding=10,
            ),
        ]
        return controls


class AdminBaseView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 0
        self.spacing = 0

    async def get_controls(
            self,
            title: str,
            main_section_controls: list,
            sections: list[Section] = None,
            text_key: str = None,
            create_button: Any = None,
    ) -> list:

        title_control = await self.get_title(
            title=title,
            text_key=text_key,
            create_button=create_button,
        )

        main_content = [
            Container(
                content=Column(
                    controls=[
                        title_control,
                        *main_section_controls,
                    ],
                    spacing=8,
                ),
                padding=16,
                margin=margin.only(bottom=15),
            ),
        ]

        controls = [
            await self.get_header(),
            *main_content,
        ]
        if sections:
            for section in sections:
                controls += await section.get_controls()

        return controls
