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


from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown
from app.controls.layout import AuthView
from app.views.auth.purchase.about.payment_method_by_currency import PaymentMethodByCurrencyView


class PymentMethodSelectCurrencyView(AuthView):
    currencies = list
    dd_currencies: Dropdown

    async def build(self):
        await self.set_type(loading=True)
        self.currencies = await self.client.session.api.client.payments.methods.currencies.get_list()
        await self.set_type(loading=False)

        currencies_options = [
            Option(
                text=currency.upper(),
                key=currency,
            ) for currency in self.currencies
        ]

        self.dd_currencies = Dropdown(
            label=await self.client.session.gtv(key='currency'),
            value=currencies_options,
            options=currencies_options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='select_currency'),
            controls=[
                self.dd_currencies,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='next'),
                        size=16,
                    ),
                    horizontal_padding=54,
                    on_click=self.change_view,
                ),
            ],
        )

    async def change_view(self, _):
        self.client.session.payment.currency = self.dd_currencies.value
        await self.client.change_view(view=PaymentMethodByCurrencyView(), delete_current=True)
