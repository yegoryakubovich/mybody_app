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


from flet_core import Container, Column, alignment, Row, Image

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts, Icons
from app.utils.payment import Payment
from app.views.auth.purchase.about.payment import PaymentView
from app.views.auth.purchase.about.payment_method import PaymentMethodView


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
                    ),
                ],
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
            ],
        )

    async def change_view(self, _):
        self.client.session.payment = Payment()
        await self.client.change_view(view=PaymentMethodView(), delete_current=True)
