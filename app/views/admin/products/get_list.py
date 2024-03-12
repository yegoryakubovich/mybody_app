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


from functools import partial

from flet_core import Row, ScrollMode, colors

from app.controls.button import ProductChipButton
from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.information.search_bar import SearchBar
from app.controls.layout import AdminBaseView
from app.controls.navigation.pagination import PaginationWidget
from app.utils import Fonts
from app.utils.pagination import paginate_items, total_page
from app.views.admin.products.create import ProductCreateView
from app.views.admin.products.get import ProductView


class ProductListView(AdminBaseView):
    route = '/admin/product/list/get'
    products: list[dict]
    nutrient_type = None
    anchor: SearchBar
    text: Text
    page_product: int = 1
    total_pages: int

    async def build(self):
        await self.set_type(loading=True)
        self.products = await self.client.session.api.client.products.get_list(
            type_=self.nutrient_type,
        )
        await self.set_type(loading=False)

        self.total_pages = total_page(self.products)
        self.products = paginate_items(self.products, self.page_product)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_product_get_list_view_title'),
            create_button=self.create_product,
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
                    wrap=True,
                ),
            ] + [
                Card(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key=product['name_text']),
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                            color=colors.ON_PRIMARY,
                        ),
                    ],
                    on_click=partial(self.product_view, product['id']),
                )
                for product in self.products
            ] + [
                PaginationWidget(
                    current_page=self.page_product,
                    total_pages=self.total_pages,
                    on_back=self.previous_page,
                    on_next=self.next_page,
                    text_back=await self.client.session.gtv(key='back'),
                    text_next=await self.client.session.gtv(key='next'),
                ),
            ]
        )

    def handle_product_click(self, event):
        self.text = event.control.data

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

    async def next_page(self, _):
        if self.page_product < self.total_pages:
            self.page_product += 1
            await self.restart()

    async def previous_page(self, _):
        if self.page_product > 1:
            self.page_product -= 1
            await self.restart()
