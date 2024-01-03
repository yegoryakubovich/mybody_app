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


from flet_core import Container, Column

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView


class CurrencyView(AdminBaseView):
    route = '/admin'
    currency = dict

    def __init__(self, currency_id_str):
        super().__init__()
        self.currency_id_str = currency_id_str

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.currency.get(
            id_str=self.currency_id_str,
        )
        self.currency = response.currency
        print( self.currency)
        await self.set_type(loading=False)

        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key=self.currency['id_str']),
                        main_section_controls=[
                            FilledButton(
                                content=Text(
                                    value=await self.client.session.gtv(key='delete'),
                                ),
                                on_click=self.delete_currency,
                            ),
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def delete_currency(self, _):
        await self.client.session.api.currency.delete(
            id_str=self.currency_id_str,
        )
        await self.client.change_view(go_back=True)
