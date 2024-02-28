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


from flet_core import Container, Column, Row, alignment, Image, MainAxisAlignment, TextButton

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts, Icons
from app.views.auth.purchase.about.erip import ERIPView
from app.views.main.tabs.account import Setting
from config import settings


class PaymentView(AuthView):
    async def build(self):
        payment = [
            Setting(name='erip', icon=Icons.PRIVACY_POLICY, on_click=self.erip),
            Setting(name='card', icon=Icons.SUPPORT, url=settings.url_payment_card)
        ]
        advantages = [
            Row(
                controls=[
                    Container(
                        content=Image(
                            src=setting.icon,
                            width=40,
                            height=40,
                        ),
                        url=setting.url,
                        on_click=setting.on_click,
                    ),
                    Text(
                        value=await self.client.session.gtv(key=setting.name),
                        size=20,
                        font_family=Fonts.REGULAR,
                    ),
                ]
            )
            for setting in payment
        ]

        self.controls = await self.get_controls(
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
                    margin=20,
                ),
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
        await self.client.change_view(view=InitView())

    async def erip(self, _):
        await self.client.change_view(view=ERIPView())

    async def logout(self, _):
        await self.client.session.set_cs(key='token', value=None)
        from app.views.auth.init import InitView
        await self.client.change_view(view=InitView(), delete_current=True)

