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

from flet_core import MainAxisAlignment, Container, ProgressRing, Column, alignment

from app.controls.information import Text
from app.controls.layout import AuthView
from app.utils import Fonts
from app.views.auth.purchase.about import PaymentView


class FormationCheckView(AuthView):

    async def build(self):
        self.controls = await self.get_controls(
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Container(
                                content=ProgressRing(
                                    height=20,
                                    width=20,
                                ),
                                alignment=alignment.center
                            ),
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

        while True:
            payment = await self.client.session.api.client.payments.get(
                id_=self.client.session.payment.payment_id
            )
            if payment and payment.state == 'waiting':
                break
            await asyncio.sleep(5)

        self.client.session.payment.data = payment.data
        await self.client.change_view(view=PaymentView(), delete_current=True),

