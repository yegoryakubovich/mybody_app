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


from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.accounts.service.meal.report.create import AccountMealReportCreateView


class AccountMealReportView(AdminBaseView):
    route = '/admin/account/meal/report/get'
    tf_comment: Text
    tf_not_report: Text
    products: list[dict]
    report: dict

    def __init__(self, meal_report_id):
        super().__init__()
        self.meal_report_id = meal_report_id

    async def build(self):
        await self.set_type(loading=True)
        self.report = await self.client.session.api.admin.meals.reports.get(
            id_=self.meal_report_id,
        )
        if self.report:
            self.products = []
            for i, product in enumerate(self.report['products']['products_id']):
                product_info = await self.client.session.api.client.products.get(id_=product['product']['products_id'])
                # Находим соответствующий продукт в self.meal['products']
                meal_product = self.report['products']['products_id'][i]
                if meal_product is not None:
                    product_info['meal_product'] = meal_product
                self.products.append(product_info)
        await self.set_type(loading=False)
        if self.report:
            self.tf_comment = Text(
                value=self.report['comment'],
                size=20,
                font_family=Fonts.MEDIUM,
            )
            button = FilledButton(
                content=Text(
                    value=await self.client.session.gtv(key='delete'),
                ),
                on_click=self.delete_meal_report,
            )
            on_create_click = None
            controls = [self.tf_comment, button]
        else:
            self.tf_not_report = Text(
                value=await self.client.session.gtv(key='not_report'),
                size=20,
                font_family=Fonts.MEDIUM,
            )
            on_create_click = self.create_training_report
            controls = [self.tf_not_report]

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='report'),
            on_create_click=on_create_click,
            main_section_controls=controls,
        )

    async def delete_meal_report(self, _):
        await self.client.session.api.admin.meals.reports.delete(
            id_=self.meal_report_id,
        )
        await self.client.change_view(go_back=True, with_restart=True, delete_current=True)

    async def create_training_report(self, _):
        await self.client.change_view(AccountMealReportCreateView())
