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
import functools

from app.controls.button import FilledButton
from app.controls.information import Text, Card
from app.controls.layout import AdminBaseView, Section
from app.utils import Fonts
from app.views.admin.accounts.meal.product import AccountMealProductCreateView, AccountMealProductView


class AccountMealView(AdminBaseView):
    route = '/admin/account/meal/get'
    meal = dict
    products = list

    def __init__(self, meal_id):
        super().__init__()
        self.meal_id = meal_id

    async def build(self):
        await self.set_type(loading=True)
        self.meal = await self.client.session.api.client.meal.get(
            id_=self.meal_id,
        )
        self.products = []
        for product in self.meal['products']:
            product_info = await self.client.session.api.client.product.get(id_=product['product'])
            # Находим соответствующий продукт в self.meal['products']
            meal_product = next((p for p in self.meal['products'] if p['product'] == product_info['id']), None)
            if meal_product is not None:
                product_info['meal_product'] = meal_product
            self.products.append(product_info)

        await self.set_type(loading=False)
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.meal['type']),
            on_create_click=self.create_meal_product,
            main_section_controls=[
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='delete'),
                    ),
                    on_click=self.delete_meal,
                ),
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='meals'),
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value=product['name_text'],
                                    size=18,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                            ],
                            on_click=functools.partial(
                                self.product_view, product
                            ),
                        )
                        for product in self.products
                    ],
                ),
            ],
        )

    async def product_view(self, product, _):
        await self.client.change_view(AccountMealProductView(
            product=product,
            meal_id=self.meal_id,
        ),
    )

    async def delete_meal(self, _):
        pass

    async def create_meal_product(self, _):
        await self.client.change_view(
            AccountMealProductCreateView(
                meal_id=self.meal_id,
            ),
        )
        await self.client.change_view(go_back=True, with_restart=True)
