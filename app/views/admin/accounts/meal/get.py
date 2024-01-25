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

from flet_core import Row, ScrollMode
from flet_core.dropdown import Option, Dropdown
from mybody_api_client.utils.base_section import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text, Card
from app.controls.information.snackbar import SnackBar
from app.controls.input import TextField
from app.controls.layout import AdminBaseView, Section
from app.utils import Fonts, Error
from app.views.admin.accounts.meal.product import AccountMealProductCreateView, AccountMealProductView


class AccountMealView(AdminBaseView):
    route = '/admin/account/meal/get'
    meal: dict
    products: list
    snack_bar: SnackBar
    dd_type: Dropdown
    tf_date: TextField
    tf_fats = TextField
    tf_proteins = TextField
    tf_carbohydrates = TextField

    def __init__(self, meal_id):
        super().__init__()
        self.meal_id = meal_id

    async def build(self):
        await self.set_type(loading=True)
        self.meal = await self.client.session.api.client.meal.get(
            id_=self.meal_id,
        )
        self.products = []
        for i, product in enumerate(self.meal['products']):
            product_info = await self.client.session.api.client.product.get(id_=product['product'])
            # Находим соответствующий продукт в self.meal['products']
            meal_product = self.meal['products'][i]
            if meal_product is not None:
                product_info['meal_product'] = meal_product
            self.products.append(product_info)
        await self.set_type(loading=False)

        meal_type_dict = {
            'meal_1': await self.client.session.gtv(key='meal_1'),
            'meal_2': await self.client.session.gtv(key='meal_2'),
            'meal_3': await self.client.session.gtv(key='meal_3'),
            'meal_4': await self.client.session.gtv(key='meal_4'),
            'meal_5': await self.client.session.gtv(key='meal_5'),
        }
        meal_type_options = [
            Option(
                text=meal_type_dict[meal_type],
                key=meal_type,
            ) for meal_type in meal_type_dict
        ]
        self.dd_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=self.meal['type'],
            options=meal_type_options,
        )

        self.tf_date = TextField(
            label=await self.client.session.gtv(key='date'),
            value=self.meal['date'],
        )
        self.snack_bar = SnackBar(
            content=Text(
                value=await self.client.session.gtv(key='successful'),
            ),
        )
        self.tf_fats = TextField(
            label=await self.client.session.gtv(key='fats'),
            value=self.meal['fats']
        )
        self.tf_proteins = TextField(
            label=await self.client.session.gtv(key='proteins'),
            value=self.meal['proteins']
        )
        self.tf_carbohydrates = TextField(
            label=await self.client.session.gtv(key='carbohydrates'),
            value=self.meal['carbohydrates']
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.meal['type']),
            main_section_controls=[
                self.dd_type,
                self.tf_date,
                self.tf_fats,
                self.tf_proteins,
                self.tf_carbohydrates,
                self.snack_bar,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_meal,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_meal,
                        ),
                    ]
                )
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='meals'),
                    on_create_click=self.create_meal_product,
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value=await self.client.session.gtv(key=product['name_text']),
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
        await self.client.change_view(
            AccountMealProductView(
                product=product,
                meal_id=self.meal_id,
            ),
        )

    async def delete_meal(self, _):
        await self.client.session.api.admin.meal.delete(
            id_=self.meal_id,
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def create_meal_product(self, _):
        await self.client.change_view(
            AccountMealProductCreateView(
                meal_id=self.meal_id,
            ),
        )

    async def update_meal(self, _):
        fields = [self.tf_date]
        for field in fields:
            if not await Error.check_date_format(self, field):
                return
        try:
            await self.client.session.api.admin.meal.update(
                id_=self.meal_id,
                date=self.tf_date.value,
                type_=self.dd_type.value,
                fats=self.tf_fats.value,
                proteins=self.tf_proteins.value,
                carbohydrates=self.tf_carbohydrates.value,
            )
            self.snack_bar.open = True
            await self.update_async()
        except ApiException:
            await self.set_type(loading=False)
            return await self.client.session.error(code=0)
