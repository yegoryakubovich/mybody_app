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


from flet_core import Container, Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error


class CreateProductView(AdminBaseView):
    route = '/admin'
    tf_name: TextField
    dd_nutrients_type = Dropdown
    dd_articles = Dropdown
    dd_units = Dropdown

    async def build(self):

        await self.set_type(loading=True)
        response = await self.client.session.api.article.get_list(
        )
        articles = response.articles
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
        article_options = [
            Option(
                text=article['name_text'],
                key=article['id']
            ) for article in articles
        ]
        nutrients_type_options = [
            Option(
                text=nutrient_type,
            ) for nutrient_type in nutrients_type
        ]
        nutrients_unit = [
            Option(
                text=nutrient_unit,
            ) for nutrient_unit in nutrients_unit
        ]
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.dd_nutrients_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=nutrients_type[0],
            options=nutrients_type_options,
        )
        self.dd_articles = Dropdown(
            label=await self.client.session.gtv(key='article'),
            value=await self.client.session.gtv(key=articles[0]['name_text']),
            options=article_options,
        )
        self.dd_units = Dropdown(
            label=await self.client.session.gtv(key='units'),
            value=nutrients_unit[0],
            options=nutrients_unit,
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_product_create_view_title'),
                        main_section_controls=[
                            self.tf_name,
                            self.dd_nutrients_type,
                            self.dd_articles,
                            self.dd_units,
                            FilledButton(
                                content=Text(
                                    value=await self.client.session.gtv(key='create'),
                                    size=16,
                                ),
                                on_click=self.create_product,
                            ),
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def create_product(self, _):
        from app.views.admin.products.get import ProductView
        fields = [(self.tf_name, 1, 32)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len, max_len):
                return
        response = await self.client.session.api.product.create(
            name=self.tf_name.value,
            type_=self.dd_nutrients_type.value,
            article_id=self.dd_articles.value,
            unit=self.dd_units.value
        )
        product_id = response.id
        await self.client.change_view(view=ProductView(product_id=product_id))
