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
from flet_core import Column
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.client.meal.report import MealReportView


class AccountMealReportView(AdminBaseView):
    route = '/admin/account/meal/report/get'
    tf_comment: Text
    tf_not_report: Text
    products: list[dict]
    report: dict
    meal: dict

    def __init__(self, meal_id):
        super().__init__()
        self.meal_id = meal_id

    async def build(self):
        await self.set_type(loading=True)
        self.meal = await self.client.session.api.admin.meals.get(
            id_=self.meal_id,
        )
        try:
            self.report = await self.client.session.api.admin.meals.reports.get(
                id_=self.meal['meal_report_id'],
            )
        except ApiException:
            self.report = {}
        await self.set_type(loading=False)
        if self.report:
            self.products = []
            for i, product in enumerate(self.report['products']):
                product_info = await self.client.session.api.client.products.get(id_=product['product_id'])
                # Находим соответствующий продукт в self.meal['products']
                meal_product = self.report['products'][i]
                if meal_product:
                    product_info['meal_product'] = meal_product
                self.products.append(product_info)
        if self.report:
            self.tf_comment = Text(
                value=f'{await self.client.session.gtv(key="comment")}' ': ' f'{self.report["comment"]}',
                size=20,
                font_family=Fonts.MEDIUM,
            )
            button = FilledButton(
                content=Text(
                    value=await self.client.session.gtv(key='delete'),
                ),
                on_click=self.delete_meal_report,
            )
            product_text = [
                Text(
                    value=f'{await self.client.session.gtv(key="products")}' + ':',
                    size=20,
                    font_family=Fonts.MEDIUM,
                )
            ]
            product_buttons = [
                Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(
                                key=product['name_text']) + ' ' + str(product['meal_product']['value']) + ' ' +
                                  await self.client.session.gtv(key='gr')
                        )
                        for product in self.products
                    ],
                ),
            ]
            controls = product_text + product_buttons + [self.tf_comment, button]
            on_create_click = None
        else:
            self.tf_not_report = Text(
                value=await self.client.session.gtv(key='not_report'),
                size=20,
                font_family=Fonts.MEDIUM,
            )
            controls = [self.tf_not_report]
            on_create_click = self.create_training_report

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='report'),
            on_create_click=on_create_click,
            main_section_controls=controls,
        )

    async def delete_meal_report(self, _):
        await self.client.session.api.admin.meals.reports.delete(
            id_=self.meal['meal_report_id'],
        )
        await self.client.change_view(go_back=True, with_restart=True, delete_current=True)

    async def create_training_report(self, _):
        await self.client.change_view(MealReportView(meal_id=self.meal_id))
