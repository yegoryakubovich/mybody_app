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

from flet_core import Row, Container, MainAxisAlignment, Column, margin

from app.controls.information import Text
from app.controls.layout.view import View
from app.utils import Fonts


class ClientSection:
    title: str
    controls: list
    create_button: Any = None

    def __init__(self, title: str, controls: list):
        self.title = title
        self.controls = controls

    @staticmethod
    async def get_title(title: str):
        controls = [
            Text(
                value=title,
                size=36,
                font_family=Fonts.SEMIBOLD,
            ),
        ]

        return Row(
            controls=controls,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

    async def get_controls(self) -> list:
        title_control = await self.get_title(title=self.title)

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


class ClientBaseView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 0
        self.spacing = 0

    async def get_controls(
            self,
            title: str,
            main_section_controls: list,
            sections: list[ClientSection] = None,
    ) -> list:

        title_control = await self.get_title(
            title=title,
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
                padding=10,
                margin=margin.only(bottom=15),
            ),
        ]

        controls = [
            await self.get_header(),
            *main_content,
        ]
        if sections is not None:
            for section in sections:
                controls += await section.get_controls()

        return controls
