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


from functools import partial

from flet_core import Column

from app.controls.button import ListItemButton
from app.controls.input import Dropdown
from app.controls.layout import AuthView
from app.utils import Icons
from app.views.auth.purchase.about.promotional_code import PromotionalCodeView


class PaymentMethodByCurrencyView(AuthView):
    payment_methods: list[dict]
    dd_currencies: Dropdown

    async def build(self):
        await self.set_type(loading=True)
        self.payment_methods = await self.client.session.api.client.payments.methods.get_list_by_currency(
            currency=self.client.session.payment.currency,
        )
        await self.set_type(loading=False)

        self.controls = await self.get_controls(
            controls=[
                Column(
                    controls=[
                        ListItemButton(
                            icon=Icons.CURRENCY,
                            name=method['name'],
                            on_click=partial(
                                self.change_view, method['id_str'],
                                method['payment_method_currency_id']
                            ),
                        ) for method in self.payment_methods
                    ],
                ),
            ],
        )

    async def change_view(self, payment_method, payment_method_currency_id, _):
        self.client.session.payment.payment_method = payment_method
        self.client.session.payment.payment_method_currency_id = payment_method_currency_id
        await self.client.change_view(view=PromotionalCodeView(), delete_current=True)
