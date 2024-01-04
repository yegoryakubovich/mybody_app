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

from app.controls.button import ProductChipButton
from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.products.create import ProductCreateView
from app.views.admin.products.get import ProductView


class ProductListView(AdminBaseView):
    route = '/admin/product/list/get'
    products: list[dict]
    nutrient_type = None

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.product.get_list(
            type_=self.nutrient_type or None,
        )
        self.products = response.products
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_product_get_list_view_title'),
            on_create_click=self.create_product,
            main_section_controls=[
                Row(
                    controls=[
                        ProductChipButton(
                            Text(
                                value=await self.client.session.gtv(key='fats'),
                            ).value,
                            on_click=self.fats
                        ),
                        ProductChipButton(
                            Text(
                                value=await self.client.session.gtv(key='proteins'),
                            ).value,
                            on_click=self.proteins
                        ),
                        ProductChipButton(
                            Text(
                                value=await self.client.session.gtv(key='carbohydrates'),
                            ).value,
                            on_click=self.carbohydrates,
                        ),
                        ProductChipButton(
                            Text(
                                value=await self.client.session.gtv(key='all_products'),
                            ).value,
                            on_click=self.all_type,
                        ),
                    ],
                ),
            ] + [
                Card(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key=product['name_text']),
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=functools.partial(self.product_view, product['id']),
                )
                for product in self.products
            ],
         )

    async def create_product(self, _):
        await self.client.change_view(view=ProductCreateView())

    async def product_view(self, product_id, _):
        await self.client.change_view(view=ProductView(product_id=product_id))

    async def fats(self, _):
        self.nutrient_type = 'fats'
        await self.build()
        await self.update_async()

    async def proteins(self, _):
        self.nutrient_type = 'proteins'
        await self.build()
        await self.update_async()

    async def carbohydrates(self, _):
        self.nutrient_type = 'carbohydrates'
        await self.build()
        await self.update_async()

    async def all_type(self, _):
        self.nutrient_type = None
        await self.build()
        await self.update_async()
