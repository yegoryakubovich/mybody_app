#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
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


from flet_core import Container, Row, Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown
from app.controls.layout import View


class ProductView(View):
    route = '/admin'
    product = dict
    dd_nutrient_type = Dropdown

    def __init__(self, product_id):
        super().__init__()
        self.product_id = product_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.product.get(
            id_=self.product_id
        )
        self.product = response.product
        await self.set_type(loading=False)

        nutrients_type = ['proteins', 'fats', 'carbohydrates']
        nutrient_type_options = [
            Option(
                text=nutrient_type,
            ) for nutrient_type in nutrients_type
        ]

        self.dd_nutrient_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=self.product['type'],
            options=nutrient_type_options,
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                         title=await self.client.session.gtv(key=self.product['name_text']),
                         create_button=False,
                        ),
                        self.dd_nutrient_type,
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='update_product'),
                                    ),
                                    on_click=self.update_product,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='delete_product'),
                                    ),
                                    on_click=self.delete_product,
                                ),
                            ]
                        )
                    ],
                ),
                padding=10
            ),
        ]

    async def delete_product(self, _):
        await self.client.session.api.product.delete(
            id_=self.product_id
        )
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()

    async def update_product(self, _):
        await self.client.session.api.product.update(
            id_=self.product_id,
            type_=self.dd_nutrient_type.value,

        ),
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()
