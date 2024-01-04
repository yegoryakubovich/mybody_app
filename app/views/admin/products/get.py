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

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown
from app.controls.layout import AdminBaseView


class ProductView(AdminBaseView):
    route = '/admin/product/get'
    product = dict
    articles = list[dict]
    dd_nutrient_type = Dropdown
    dd_articles = Dropdown
    dd_units = Dropdown

    def __init__(self, product_id):
        super().__init__()
        self.product_id = product_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.product.get(
            id_=self.product_id
        )
        self.product = response.product
        response = await self.client.session.api.article.get_list(
        )
        self.articles = response.articles
        await self.set_type(loading=False)

        nutrients_unit = [
            await self.client.session.gtv(key='gr'),
            await self.client.session.gtv(key='ml'),
        ]
        nutrients_type = [
            await self.client.session.gtv(key='proteins'),
            await self.client.session.gtv(key='fats'),
            await self.client.session.gtv(key='carbohydrates'),
        ]
        nutrient_type_options = [
            Option(
                text=nutrient_type,
            ) for nutrient_type in nutrients_type
        ]
        article_options = [
            Option(
                text=article['name_text'],
                key=article['id']
            ) for article in self.articles
        ]
        nutrients_unit = [
            Option(
                text=nutrient_unit,
            ) for nutrient_unit in nutrients_unit
        ]
        self.dd_nutrient_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=self.product['type'],
            options=nutrient_type_options,
        )
        self.dd_units = Dropdown(
            label=await self.client.session.gtv(key='unit'),
            value=self.product['unit'],
            options=nutrients_unit,
        )
        self.dd_articles = Dropdown(
            label=await self.client.session.gtv(key='article'),
            value=self.product['article'],
            options=article_options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.product['name_text']),
            main_section_controls=[
                self.dd_nutrient_type,
                self.dd_articles,
                self.dd_units,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_product,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_product,
                        ),
                    ],
                ),
            ]
        ),

    async def delete_product(self, _):
        await self.client.session.api.product.delete(
            id_=self.product_id
        )
        await self.client.change_view(go_back=True)

    async def update_product(self, _):
        response = await self.client.session.api.product.update(
            id_=self.product_id,
            type_=self.dd_nutrient_type.value,
            unit=self.dd_units.value,
            article_id=self.dd_articles.value,
        )
        print(response)
        await self.update_async()
