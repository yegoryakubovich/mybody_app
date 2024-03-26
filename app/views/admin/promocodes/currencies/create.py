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
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error


class PromocodeCurrencyCreateView(AdminBaseView):
    route = '/admin/promocode/currency/create'
    tf_amount: TextField
    dd_currency: Dropdown
    currencies: list[dict]

    def __init__(self, promocode_id_str):
        super().__init__()
        self.promocode_id_str = promocode_id_str

    async def build(self):
        self.currencies = await self.client.session.api.client.currencies.get_list()
        currency_options = [
            Option(
                text=currency.get('name_text'),
                key=currency.get('id_str'),
            ) for currency in self.currencies
        ]
        self.dd_currency = Dropdown(
            label=await self.client.session.gtv(key='currency'),
            value=self.currencies[0]['id_str'],
            options=currency_options,
        )
        self.tf_amount = TextField(
            label=await self.client.session.gtv(key='amount'),
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_promocode_create_view_title'),
            main_section_controls=[
                self.dd_currency,
                self.tf_amount,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_promocode_currency,
                ),
            ],
         )

    async def create_promocode_currency(self, _):
        fields = [(self.tf_amount, True)]
        for field, check_int in fields:
            if not await Error.check_field(self, field, check_int):
                return
        try:
            await self.set_type(loading=True)
            await self.client.session.api.admin.promocodes.currencies.create(
                promocode=self.promocode_id_str,
                currency=self.dd_currency.value,
                amount=self.tf_amount.value,
            )
            await self.set_type(loading=False)
            await self.client.change_view(go_back=True, with_restart=True, delete_current=True)
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
