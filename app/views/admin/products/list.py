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


import functools

from flet_core import Container, Row, Card, Text, Column, ScrollMode

from app.controls.button import FilledButton
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.products.create import CreateProductView
from app.views.admin.products.get import ProductView


class ProductListView(View):
    route = '/admin'
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
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='products'),
                            on_create_click=self.create_product,
                        ),
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='fats'),
                                    ),
                                    on_click=self.fats,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='proteins'),
                                    ),
                                    on_click=self.proteins,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='carbohydrates'),
                                    ),
                                    on_click=self.carbohydrates,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='all_type'),
                                    ),
                                    on_click=self.all_type,
                                ),
                            ]
                        )
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=await self.client.session.gtv(key=product['name_text']),
                                            size=18,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.product_view, product['id']),
                            ),
                            margin=0,
                        )
                        for product in self.products
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_product(self, _):
        await self.client.change_view(view=CreateProductView())

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
