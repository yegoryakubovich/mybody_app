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


from flet_core import Row

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown
from app.controls.layout import AuthView
from app.utils import Fonts
from app.views.auth.purchase.about.payment_method_by_currency import PaymentMethodByCurrencyView
from app.views.auth.purchase.about.payment_method_select_currency import PymentMethodSelectCurrencyView


class PaymentMethodView(AuthView):
    currencies: list
    currency: str
    dd_currencies: Dropdown

    async def build(self):
        await self.set_type(loading=True)
        self.currencies = await self.client.session.api.client.payments.methods.currencies.get_list()
        await self.set_type(loading=False)

        if self.client.session.account.currency in self.currencies:
            self.currency = self.client.session.account.currency
        else:
            self.currency = 'byn'

        self.controls = await self.get_controls(
            controls=[
                Text(
                    value=await self.client.session.gtv(
                        key='convenient_pay') + ' ' + self.currency.upper() + '?',
                    size=30,
                    font_family=Fonts.SEMIBOLD
                ),
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='yes'),
                                size=16,
                            ),
                            horizontal_padding=54,
                            on_click=self.change_view,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='no'),
                                size=16,
                            ),
                            horizontal_padding=54,
                            on_click=self.select_currency,
                        ),
                    ],
                ),
            ],
        )

    async def change_view(self, _):
        self.client.session.payment.currency = self.currency
        await self.client.change_view(view=PaymentMethodByCurrencyView(), delete_current=True,)

    async def select_currency(self, _):
        await self.client.change_view(view=PymentMethodSelectCurrencyView(), delete_current=True)
