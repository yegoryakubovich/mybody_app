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
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView



class AccountMealProductCreateView(AdminBaseView):
    route = '/admin/account/meal/product/create'
    products: list[dict]
    tf_quantity: TextField
    dd_product: Dropdown

    def __init__(self, meal_id):
        super().__init__()
        self.meal_id = meal_id

    async def build(self):
        await self.set_type(loading=True)
        self.products = await self.client.session.api.client.product.get_list()
        await self.set_type(loading=False)

        product_options = [
            Option(
                text=product['name_text'],
                key=product['id']
            ) for product in self.products
        ]
        self.tf_quantity = TextField(
            label=await self.client.session.gtv(key='quantity'),
        )
        self.dd_product = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=product_options[0].key,
            options=product_options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_role_create_view_title'),
            main_section_controls=[
                self.dd_product,
                self.tf_quantity,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_meal_product,
                ),
            ]
        )

    async def create_meal_product(self, _):
        from app.views.admin.accounts.meal.product import AccountMealProductView
        await self.client.session.api.admin.meal.create(
            meal_id=self.meal_id,
            product_id=self.dd_product,
            value=self.tf_quantity.value,
        )
        await self.client.change_view(AccountMealProductView(meal_id=self.meal_id), delete_current=True)
