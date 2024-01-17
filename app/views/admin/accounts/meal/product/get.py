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
from app.controls.input import TextField
from app.controls.layout import AdminBaseView


class AccountMealProductView(AdminBaseView):
    route = '/admin/account/meal/product/get'
    tf_quantity: TextField

    def __init__(self, product, meal_id):
        super().__init__()
        self.product = product
        self.meal_id = meal_id

    async def build(self):
        print(self.product)
        self.tf_quantity = TextField(
            label=await self.client.session.gtv(key='quantity'),
            value=self.product['meal_product']['value'],
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.product['name_text']),
            main_section_controls=[
                self.tf_quantity,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_meal_product,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_meal_product,
                        ),
                    ],
                ),
            ],
        )

    async def delete_meal_product(self, _):
        await self.client.session.api.admin.meal.delete_product(
            id_=self.product['id'],
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def update_meal_product(self, _):
        await self.client.session.api.admin.meal.update_product(
            id_=self.product['meal_product']['id'],
            product_id=self.product['meal_product']['id'],
            value=self.tf_quantity.value,
        )
        await self.client.change_view(go_back=True, with_restart=True)
