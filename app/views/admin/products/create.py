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


from flet_core import ScrollMode
from flet_core.dropdown import Option
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error


class ProductCreateView(AdminBaseView):
    route = '/admin/product/create'
    articles = list[dict]
    tf_name: TextField
    dd_type = Dropdown
    dd_articles = Dropdown
    dd_unit = Dropdown
    tf_fats = TextField
    tf_proteins = TextField
    tf_carbohydrates = TextField
    tf_calories = TextField

    async def build(self):
        await self.set_type(loading=True)
        self.articles = await self.client.session.api.client.articles.get_list(
        )
        await self.set_type(loading=False)
        nutrients_type_dict = {
            await self.client.session.gtv(key='proteins'): 'proteins',
            await self.client.session.gtv(key='fats'): 'fats',
            await self.client.session.gtv(key='carbohydrates'): 'carbohydrates',
        }
        nutrients_unit_dict = {
            await self.client.session.gtv(key='gr'): 'gr',
            await self.client.session.gtv(key='ml'): 'ml',
        }
        article_options = [
            Option(
                text=article['name_text'],
                key=article['id']
            ) for article in self.articles
        ]
        nutrients_type_options = [
            Option(
                text=nutrient_type,
                key=nutrients_type_dict[nutrient_type],
            ) for nutrient_type in nutrients_type_dict
        ]
        nutrients_unit_options = [
            Option(
                text=nutrient_unit,
                key=nutrients_unit_dict[nutrient_unit],
            ) for nutrient_unit in nutrients_unit_dict
        ]
        self.tf_name, self.tf_fats, self.tf_proteins, self.tf_carbohydrates, self.tf_calories = [
            TextField(
                label=await self.client.session.gtv(key=key),
            )
            for key in ['name', 'fats', 'proteins', 'carbohydrates', 'calories']
        ]
        self.dd_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=list(nutrients_type_dict.values())[0],
            options=nutrients_type_options,
        )
        self.dd_unit = Dropdown(
            label=await self.client.session.gtv(key='units'),
            value=list(nutrients_unit_dict.values())[0],
            options=nutrients_unit_options,
        )
        self.dd_articles = Dropdown(
            label=await self.client.session.gtv(key='article'),
            options=article_options,
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_product_create_view_title'),
            main_section_controls=[
                self.tf_name,
                self.dd_type,
                self.dd_unit,
                self.tf_fats,
                self.tf_proteins,
                self.tf_carbohydrates,
                self.tf_calories,
                self.dd_articles,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_product,
                ),
            ],
         )

    async def create_product(self, _):
        await self.set_type(loading=True)
        from app.views.admin.products.get import ProductView
        fields = [(self.tf_name, 1, 32)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                await self.set_type(loading=False)
                return
        fields = [(self.tf_fats, True), (self.tf_proteins, True), (self.tf_carbohydrates, True)]
        for field, check_int in fields:
            if not await Error.check_field(self, field, check_int):
                await self.set_type(loading=False)
                return
        try:
            product_id = await self.client.session.api.admin.products.create(
                name=self.tf_name.value,
                type_=self.dd_type.value,
                unit=self.dd_unit.value,
                fats=self.tf_fats.value,
                proteins=self.tf_proteins.value,
                carbohydrates=self.tf_carbohydrates.value,
                calories=self.tf_calories.value or 0,
                article_id=self.dd_articles.value or 0,
            )
            await self.set_type(loading=False)
            await self.client.change_view(view=ProductView(product_id=product_id), delete_current=True)
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
