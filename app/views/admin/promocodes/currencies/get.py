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

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView


class PromocodeCurrencyView(AdminBaseView):
    route = '/admin/promocode/promocode_currency/get'
    promocode_currency = dict

    def __init__(self, currency):
        super().__init__()
        self.currency = currency

    async def build(self):
        self.controls = await self.get_controls(
            title=self.currency['currency'].upper(),
            main_section_controls=[
                Text(
                    value=f"{await self.client.session.gtv(key='amount')}: {self.currency['amount']}",
                    size=30,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='delete'),
                    ),
                    on_click=self.delete_promocode_currency,
                ),
            ],
         )

    async def delete_promocode_currency(self, _):
        await self.client.session.api.admin.promocodes.currencies.delete(
            id_=self.currency['id'],
        )
        await self.client.change_view(go_back=True, with_restart=True)
