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

from flet_core import Container, Row, alignment, Image, MainAxisAlignment, TextButton, Column, border_radius, margin

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts, Icons
from app.views.auth.purchase.about.erip import ERIPView
from app.views.main.tabs.account import Setting
from config import settings


class PaymentView(AuthView):
    payment_method = list[dict]
    advantages_container = Container()

    def __init__(self, currency):
        super().__init__()
        self.currency = currency

    async def build(self):
        await self.set_type(loading=True)
        self.payment_method = await self.client.session.api.client.currencies.get_list()
        await self.set_type(loading=False)

        payment = [
            Setting(name='erip', icon=Icons.ERIP, on_click=self.erip),
            Setting(name='card', icon=Icons.CARD, url=settings.url_payment_card)
        ] if self.currency == 'byn' else [
            Setting(name='card', icon=Icons.CARD, url=settings.url_payment_card)
        ]
        advantages = [
            Container(
                content=Row(
                    controls=[
                        Image(
                            src=setting.icon,
                            width=40,
                            height=40,
                        ),
                        Text(
                            value=await self.client.session.gtv(key=setting.name),
                            size=20,
                            font_family=Fonts.REGULAR,
                        ),
                    ]
                ),
                border_radius=border_radius.all(8),
                url=setting.url,
                on_click=setting.on_click,
                ink=True,
                margin=margin.symmetric(horizontal=20),
                padding=5,
            )
            for setting in payment
        ]
        self.advantages_container.content = Column(controls=advantages)
        await self.update_async()

        self.controls = await self.get_controls(
            with_expand=True,
            controls=[
                Row(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='payment'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='logout'),
                                size=16,
                            ),
                            on_click=self.logout
                        ),
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                ),
                self.advantages_container,
                Container(
                    content=FilledButton(
                        content=Text(
                            value=await self.client.session.gtv(key='paid'),
                            size=16,
                        ),
                        width=640,
                        on_click=self.change_view,
                    ),
                    expand=True,
                    alignment=alignment.bottom_center,
                ),
            ],
        )

    async def change_view(self, _):
        from app import InitView
        await self.client.change_view(view=InitView(), delete_current=True)

    async def erip(self, _):
        await self.client.change_view(view=ERIPView())

    async def logout(self, _):
        await self.client.session.set_cs(key='token', value=None)
        from app.views.auth.init import InitView
        await self.client.change_view(view=InitView(), delete_current=True)

