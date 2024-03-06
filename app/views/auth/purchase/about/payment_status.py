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


class PaymentStatusView(AuthView):

    async def build(self):
        from app import InitView
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
                            Container(
                                Text(
                                    value=await self.client.session.gtv(key='checking_status_payment'),
                                    size=20,
                                    font_family=Fonts.REGULAR,
                                ),
                                alignment=alignment.center
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    padding=50
                ),
            ],
        )
        await self.update_async()

        counter = 0
        while counter < 12:
            payment = await self.client.session.api.client.payments.get(
                id_=self.client.session.payment.payment_id
            )
            if payment and payment.state == 'paid':
                break
            await asyncio.sleep(5)
            counter += 1

        await self.client.change_view(view=InitView())
