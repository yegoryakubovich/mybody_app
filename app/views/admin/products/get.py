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
from app.controls.input import Dropdown
from app.controls.layout import AdminBaseView


class ProductView(AdminBaseView):
    route = '/admin/product/get'
    product = dict
    articles = list[dict]
    dd_type = Dropdown
    dd_articles = Dropdown
    dd_units = Dropdown
    snack_bar = SnackBar

    def __init__(self, product_id):
        super().__init__()
        self.product_id = product_id

    async def build(self):
        await self.set_type(loading=True)
        self.product = await self.client.session.api.client.product.get(
            id_=self.product_id
        )
        self.articles = await self.client.session.api.client.article.get_list(
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
        self.snack_bar = SnackBar(
            content=Text(
                value=await self.client.session.gtv(key='successful'),
            ),
        )
        self.dd_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=self.product['type'],
            options=nutrients_type_options,
        )
        self.dd_units = Dropdown(
            label=await self.client.session.gtv(key='unit'),
            value=self.product['unit'],
            options=nutrients_unit_options,
        )
        self.dd_articles = Dropdown(
            label=await self.client.session.gtv(key='article'),
            value=self.product['article'],
            options=article_options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.product['name_text']),
            main_section_controls=[
                self.dd_type,
                self.dd_units,
                self.dd_articles,
                self.snack_bar,
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
        )

    async def delete_product(self, _):
        await self.client.session.api.admin.product.delete(
            id_=self.product_id
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def update_product(self, _):
        try:
            await self.client.session.api.admin.product.update(
                id_=self.product_id,
                type_=self.dd_type.value,
                unit=self.dd_units.value,
                article_id=self.dd_articles.value or 0,
            )
            self.snack_bar.open = True
            await self.update_async()
        except ApiException:
            await self.set_type(loading=False)
            return await self.client.session.error(code=0)
