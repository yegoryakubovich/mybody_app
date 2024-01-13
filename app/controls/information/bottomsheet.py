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


from flet_core import BottomSheet as BottomSheetFlet, Container, Stack, Column, Image, margin, Text, TextAlign, Row, \
    MainAxisAlignment, CrossAxisAlignment, padding, IconButton, icons

from app.controls.button import FilledButton
from app.utils import Fonts


class BottomSheet(BottomSheetFlet):
    def __init__(self, icon: str, title: str, description: str, button_title=None, button_on_click=None):
        super().__init__(
            content=Container(
                Stack(
                    controls=[
                        Container(
                            content=Column(
                                controls=[
                                    Container(
                                        content=Image(
                                            src=icon,
                                            color='#1d1d1d',  # FIXME
                                        ),
                                        margin=margin.only(bottom=16),
                                    ),
                                    Text(
                                        value=title,
                                        font_family=Fonts.SEMIBOLD,
                                        size=28,
                                    ),
                                    Text(
                                        value=description,
                                        font_family=Fonts.REGULAR,
                                        size=16,
                                        text_align=TextAlign.CENTER,
                                    ),
                                ] + ([
                                    Row(
                                        controls=[
                                            FilledButton(
                                                content=Text(
                                                    value=button_title,
                                                    color='#000000',  # FIXME
                                                ),
                                                width=256,
                                                on_click=button_on_click,
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.CENTER
                                    ),
                                ] if button_title and button_on_click else []),
                                spacing=10,
                                tight=True,
                                width=384,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                            ),
                            padding=padding.symmetric(vertical=24, horizontal=32),
                        ),
                        IconButton(
                            icon=icons.CLOSE,
                            on_click=self.close,
                            top=1,
                            right=0,
                        ),
                    ],
                ),
                padding=10,
            ),
            open=False,
        )

    async def close(self, _):
        self.open = False
        await self.update_async()

    async def open_(self, _):
        self.open = True
        await self.update_async()
