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


from pyperclip import copy

from flet_core import Container, Column, Row, MainAxisAlignment, colors, Image, margin

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AuthView
from app.utils import Fonts, Icons


class ERIPView(AuthView):
    tf_clipboard: TextField

    async def build(self):
        self.tf_clipboard = TextField(
            label=await self.client.session.gtv(key='check_number'),
            value='a',
            height=50,
            color=colors.ON_BACKGROUND,
        )
        clipboard = Container(
            Row(
                controls=[
                    self.tf_clipboard,
                    Container(
                        content=Image(
                            src=Icons.COPY,
                            height=40,
                            color=colors.ON_BACKGROUND,
                        ),
                        ink=True,
                        on_click=self.copy_check,
                        bgcolor=colors.TRANSPARENT,
                        border_radius=15,
                    )
                ],
            ),
            margin=margin.only(top=15, bottom=15),
        )

        self.controls = await self.get_controls(
            title='ЕРИП',
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Text(
                                value=await self.client.session.gtv(key='erip_payment'),
                                size=20,
                                font_family=Fonts.REGULAR,
                            ),
                            clipboard,
                            Row(
                                controls=[
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='paid'),
                                            size=16,
                                        ),
                                        horizontal_padding=54,
                                        on_click=self.payment,
                                    ),
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='back'),
                                        ),
                                        on_click=self.go_back,
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                    ),
                ),
            ],
        )

    async def payment(self, _):
        from app import InitView
        await self.client.change_view(view=InitView())

    async def copy_check(self, _):
        copy(self.tf_clipboard.value)
