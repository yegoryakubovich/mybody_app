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


import json

from flet_core import Container, Row, alignment, MainAxisAlignment, TextButton, Column, margin, colors

from app.controls.button import FilledButton, ListItemButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts, Icons
from app.views.auth.purchase.about.erip import ERIPView
from app.views.auth.purchase.about.payment_status import PaymentStatusView
from app.views.main.tabs.account import Setting


class PaymentView(AuthView):
    payment_method = list[dict]
    advantages_container = Container()

    async def build(self):
        data = json.loads(self.client.session.payment.data)
        payment = [
            Setting(name='erip', icon=Icons.ERIP, on_click=self.erip),
            Setting(name='card', icon=Icons.CARD, url=data['payment_link'])
        ] if self.client.session.payment.currency == 'byn' else [
            Setting(name='card', icon=Icons.CARD, url=data['payment_link'])
        ]
        advantages = [
            ListItemButton(
                icon=setting.icon,
                name=await self.client.session.gtv(key=setting.name),
                on_click=setting.on_click,
                url=setting.url,
            )
            for setting in payment
        ]

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
                Container(
                    content=Column(
                        controls=advantages,
                    ),
                    margin=margin.symmetric(horizontal=20),
                ),
                Container(
                    content=FilledButton(
                        content=Text(
                            value=await self.client.session.gtv(key='paid'),
                            size=16,
                        ),
                        width=640,
                        on_click=self.payment,
                    ),
                    expand=True,
                    alignment=alignment.bottom_center,
                ),
                Container(
                    content=FilledButton(
                        content=Text(
                            value=await self.client.session.gtv(key='cancel_payment'),
                            size=16,
                            color=colors.ON_BACKGROUND
                        ),
                        width=640,
                        bgcolor=colors.SURFACE,
                        on_click=self.payment,
                    ),
                    alignment=alignment.bottom_center,
                ),
            ],
        )

    async def payment(self, _):
        await self.client.change_view(view=PaymentStatusView(), delete_current=True)

    async def erip(self, _):
        await self.client.change_view(view=ERIPView())

    async def logout(self, _):
        await self.client.session.set_cs(key='token', value=None)
        from app.views.auth.init import InitView
        await self.client.change_view(view=InitView())
