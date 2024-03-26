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

from flet_core import colors

from app.controls.button import FilledButton
from app.controls.information import Text, Card
from app.controls.layout import AdminBaseView, Section
from app.utils import Fonts
from app.views.admin.promocodes.currencies import PromocodeCurrencyCreateView, PromocodeCurrencyView


class PromocodeView(AdminBaseView):
    route = '/admin/promocode/get'
    promocode = dict

    def __init__(self, promocode_id_str):
        super().__init__()
        self.promocode_id_str = promocode_id_str

    async def build(self):
        await self.set_type(loading=True)
        self.promocode = await self.client.session.api.client.promocodes.get(
            id_str=self.promocode_id_str,
        )
        await self.set_type(loading=False)

        self.controls = await self.get_controls(
            title=self.promocode['id_str'],
            main_section_controls=[
                Text(
                    value=f"{await self.client.session.gtv(key='usage_quantity')}: {self.promocode['usage_quantity']}\n"
                          f"{await self.client.session.gtv(key='remaining_quantity')}: "
                          f"{self.promocode['remaining_quantity']}\n"
                          f"{await self.client.session.gtv(key='date_from')}: {self.promocode['date_from']}\n"
                          f"{await self.client.session.gtv(key='date_to')}: {self.promocode['date_to']}\n"
                          f"{await self.client.session.gtv(key='type')}: "
                          f"{await self.client.session.gtv(key=self.promocode['type'])}",
                    size=25,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='delete'),
                    ),
                    on_click=self.delete_promocode,
                ),
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='currency'),
                    create_button=self.create_promocode_currency,
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value=currency['currency'].upper(),
                                    size=15,
                                    font_family=Fonts.REGULAR,
                                    color=colors.ON_PRIMARY,
                                ),
                            ],
                            on_click=partial(self.promocode_currency_view, currency),
                        )
                        for currency in self.promocode['currencies']
                    ],
                ),
            ],
        )

    async def delete_promocode(self, _):
        await self.client.session.api.admin.promocodes.delete(
            id_str=self.promocode_id_str,
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def create_promocode_currency(self, _):
        await self.client.change_view(view=PromocodeCurrencyCreateView(promocode_id_str=self.promocode_id_str))

    async def promocode_currency_view(self, currency, _):
        await self.client.change_view(PromocodeCurrencyView(currency=currency))
