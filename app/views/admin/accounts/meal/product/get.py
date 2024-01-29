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
from flet_core.dropdown import Option
from mybody_api_client.utils.base_section import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.information.snackbar import SnackBar
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error


class AccountMealProductView(AdminBaseView):
    route = '/admin/account/meal/product/get'
    tf_quantity: TextField
    dd_product: Dropdown
    products: list[dict]
    snack_bar: SnackBar

    def __init__(self, product, meal_id):
        super().__init__()
        self.product = product
        self.meal_id = meal_id

    async def build(self):
        await self.set_type(loading=True)
        self.products = await self.client.session.api.client.product.get_list()
        await self.set_type(loading=False)

        product_options = [
            Option(
                text=await self.client.session.gtv(key=product['name_text']),
                key=product['id']
            ) for product in self.products
        ]
        self.dd_product = Dropdown(
            label=await self.client.session.gtv(key='name'),
            value=self.product['id'],
            options=product_options,
        )
        self.snack_bar = SnackBar(
            content=Text(
                value=await self.client.session.gtv(key='successful'),
            ),
        )
        self.tf_quantity = TextField(
            label=await self.client.session.gtv(key='quantity'),
            value=self.product['meal_product']['value'],
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.product['name_text']),
            main_section_controls=[
                self.dd_product,
                self.tf_quantity,
                self.snack_bar,
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
            id_=self.product['meal_product']['id'],
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def update_meal_product(self, _):
        fields = [(self.tf_quantity, 1, 5, True)]
        for field, min_len, max_len, check_int in fields:
            if not await Error.check_field(self, field, min_len, max_len, check_int):
                return
        try:
            await self.client.session.api.admin.meal.update_product(
                id_=self.product['meal_product']['id'],
                product_id=self.dd_product.value,
                value=self.tf_quantity.value,
            )
            self.snack_bar.open = True
            await self.update_async()
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
