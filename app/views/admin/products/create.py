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


from flet_core import Container, Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import View


class CreateProductView(View):
    route = '/admin'
    tf_name: TextField
    dd_nutrient_type = Dropdown

    async def build(self):
        nutrients_type = ['proteins', 'fats', 'carbohydrates']
        nutrient_type_options = [
            Option(
                text=nutrient_type,
            ) for nutrient_type in nutrients_type
        ]

        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name_product'),
        )
        self.dd_nutrient_type = Dropdown(
            label=await self.client.session.gtv(key='nutrients_type'),
            value=nutrients_type[0],
            options=nutrient_type_options,
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='create_product'),
                            create_button=False,
                        ),
                        self.tf_name,
                        self.dd_nutrient_type,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='create'),
                                size=16,
                            ),
                            on_click=self.create_product,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_product(self, _):
        from app.views.admin.products.get import ProductView
        if len(self.tf_name.value) < 2 or len(self.tf_name.value) > 1024:
            self.tf_name.error_text = await self.client.session.gtv(key='name_min_max_letter')
        else:
            response = await self.client.session.api.product.create(
                name=self.tf_name.value,
                type_=self.dd_nutrient_type.value,
            )
            print(response)
            product_id = response.product_id
            await self.client.change_view(view=ProductView(product_id=product_id))
