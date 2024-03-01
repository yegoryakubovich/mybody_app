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

from flet_core import Container, Column, alignment, Row, Image, ProgressRing, MainAxisAlignment

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts, Icons
from app.views.auth.purchase.about.payment import PaymentView


class PurchaseFirstView(AuthView):
    ICONS = [Icons.ADMIN_PRODUCTS, Icons.ABOUT, Icons.ADMIN_EXERCISES, Icons.PRIVACY_POLICY, Icons.SUPPORT]

    async def build(self):
        advantages = [
            Row(
                controls=[
                    Image(
                        src=self.ICONS[i],
                        width=25,
                        height=25,
                    ),
                    Container(
                        content=Text(
                            value=await self.client.session.gtv(key=f"you_get_{i + 1}"),
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    )
                ]
            )
            for i in range(5)
        ]
        self.controls = await self.get_controls(
            with_expand=True,
            controls=[
                Container(
                    content=Column(
                        controls=advantages,
                    ),
                ),
                Container(
                    content=FilledButton(
                        content=Text(
                            value=await self.client.session.gtv(key='buy'),
                            size=16,
                        ),
                        width=640,
                        on_click=self.change_view,
                    ),
                    expand=True,
                    alignment=alignment.bottom_center,
                ),
            ]
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
        await self.client.change_view(view=PaymentView(), delete_current=True)
