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


from flet_core import Container, Column, alignment, border, margin, Row, Image

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts, Icons


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
    async def build(self):
        icon = [Icons.ADMIN_SERVICES, Icons.SECURITY, Icons.ADMIN_EXERCISES, Icons.ADMIN_PRODUCTS, Icons.SUPPORT]
        advantages = [
            Advantage(icon[i], await self.client.session.gtv(key=f"you_get_{i+1}"))
            for i in range(5)
        ]
        self.controls = await self.get_controls(
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Container(
                                content=Text(
                                    value=await self.client.session.gtv(key='НАЗВАНИЕ ПРОДУКТА'),
                                    size=20,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                                alignment=alignment.top_center
                            ),
                            Container(
                                content=Column(
                                    controls=[advantage.to_control() for advantage in advantages],
                                ),
                            ),
                            Container(
                                content=Text(
                                    value=f'{1000000} {self.client.session.account.currency}'.upper(),
                                    size=20,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                                alignment=alignment.top_center
                            ),
                            Container(
                                content=FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='next'),
                                        size=16,
                                    ),
                                    on_click=self.change_view,
                                ),
                                alignment=alignment.top_center,
                            ),
                        ]
                    ),
                    alignment=alignment.top_center,
                    border=border.all(5, '#008F12'),
                    border_radius=6,
                    padding=20,
                    margin=margin.symmetric(horizontal=20)
                ),
            ],
        )

    async def change_view(self, _):
        from app import InitView
        await self.client.change_view(view=InitView())
