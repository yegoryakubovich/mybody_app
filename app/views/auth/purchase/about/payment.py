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


from flet_core import Container, Column, Row, MainAxisAlignment

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts
from app.views.auth.purchase.about.erip import ERIPView
from config import settings


class PaymentView(AuthView):
    async def build(self):
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='payment'),
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Text(
                                value=await self.client.session.gtv(key='payment_text_one'),
                                size=20,
                                font_family=Fonts.REGULAR,
                            ),
                            Row(
                                controls=[
                                    FilledButton(
                                        content=Text(
                                            value='ЕРИП',
                                            size=16,
                                        ),
                                        width=150,
                                        on_click=self.erip,
                                    ),
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='card'),
                                            size=16,
                                        ),
                                        width=150,
                                        url=settings.url_payment_card,
                                    ),
                                ],
                            ),
                            Text(
                                value=await self.client.session.gtv(key='payment_text_two'),
                                size=20,
                                font_family=Fonts.REGULAR,
                            ),
                            Row(
                                controls=[
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='paid'),
                                            size=16,
                                        ),
                                        horizontal_padding=54,
                                        on_click=self.change_view,
                                    ),
                                    FilledButton(
                                        content=Text(
                                            value=await self.client.session.gtv(key='logout'),
                                        ),
                                        on_click=self.logout
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                            )
                        ],
                        spacing=10
                    ),
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
