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


import asyncio

from flet_core import Container, Column, alignment, border, margin, Row, Image, ProgressRing, MainAxisAlignment

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts, Icons
from app.views.auth.purchase.about.payment import PaymentView


class Advantage:
    def __init__(self, icon_path, text):
        self.icon_path = icon_path
        self.text = text

    def to_control(self):
        return Row(
            controls=[
                Image(
                    src=self.icon_path,
                    width=15,
                    height=15,
                ),
                Text(
                    value=self.text,
                    size=15,
                    font_family=Fonts.MEDIUM,
                ),
            ]
        )


class PurchaseFirstView(AuthView):
    ICONS = [Icons.ADMIN_PRODUCTS, Icons.ABOUT, Icons.ADMIN_EXERCISES, Icons.PRIVACY_POLICY, Icons.SUPPORT]

    async def build(self):
        advantages = [
            Row(
                controls=[
                    Image(
                        src=self.ICONS[i],
                        width=15,
                        height=15,
                    ),
                    Text(
                        value=await self.client.session.gtv(key=f"you_get_{i + 1}"),
                        size=15,
                        font_family=Fonts.MEDIUM,
                    ),
                ]
            )
            for i in range(5)
        ]
        self.controls = await self.get_controls(
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Container(
                                content=Text(
                                    value=f'{await self.client.session.gtv(key="course")}' + ' ' + 'My Body',
                                    size=20,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                                alignment=alignment.top_center
                            ),
                            Container(
                                content=Column(
                                    controls=advantages,
                                ),
                            ),
                            Container(
                                content=Text(
                                    value='109 BYN',
                                    size=20,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                                alignment=alignment.top_center
                            ),
                            Container(
                                content=FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='buy'),
                                        size=16,
                                    ),
                                    on_click=self.change_view,
                                ),
                                alignment=alignment.top_center,
                            ),
                        ]
                    ),
                    alignment=alignment.top_center,
                    border=border.all(2, '#008F12'),
                    border_radius=6,
                    padding=20,
                    margin=margin.symmetric(horizontal=20)
                ),
            ],
        )

    async def change_view(self, _):
        progress_ring = ProgressRing(
            height=20,
            width=20,
        )
        self.controls.clear()
        self.controls = await self.get_controls(
            controls=[
                Container(
                    content=Row(
                        controls=[
                            progress_ring,
                            Text(
                                value=await self.client.session.gtv(key='expose_check'),
                                size=20,
                                font_family=Fonts.REGULAR,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    padding=50
                ),
            ],
        )
        await self.update_async()
        await asyncio.sleep(1)
        await self.client.change_view(view=PaymentView())
