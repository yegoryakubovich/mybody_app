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


import base64

from flet_core import Column, Image
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView
from app.utils import Fonts


class ReportListView(AdminBaseView):
    route = '/admin/account/meal/report/get'
    tf_not_report: Text
    products: list[dict]
    report: dict
    meal: dict
    image_data: str = None
    meals_reports: dict
    training_report: dict
    tf_comment: Text
    tf_not_report: Text

    def __init__(self, meals_reports_ids, training_report_id, training_id):
        super().__init__()
        self.meals_reports_ids = meals_reports_ids
        self.training_id = training_id
        self.training_report_id = training_report_id

    async def build(self):
        await self.set_type(loading=True)
        for meal_report_id in self.meals_reports_ids:
            try:
                report = await self.client.session.api.admin.meals.reports.get(id_=meal_report_id)
                if report['images']:
                    response = await self.client.session.api.client.images.get(id_str=report['images'][0]['id_str'])
                    image_data = await response.read()
                else:
                    image_data = None
                self.meals_reports[meal_report_id] = {'report': report, 'image_data': image_data}
            except ApiException:
                self.meals_reports[meal_report_id] = {}
        try:
            self.training_report = await self.client.session.api.admin.trainings.reports.get(
                id_=self.training_report_id,
            )
        except ApiException:
            self.training_report = {}
        await self.set_type(loading=False)

        controls = []
        if self.training_report:
            if self.training_report['comment']:
                comment = Text(
                    value=f'{await self.client.session.gtv(key="comment")}: {self.report["comment"]}',
                    size=20,
                    font_family=Fonts.MEDIUM,
                )
                controls.append(comment)

            product_text = Text(
                value=f'{await self.client.session.gtv(key="products")} :',
                size=20,
                font_family=Fonts.MEDIUM,
            )
            controls.append(product_text)

            product_buttons = Column(
                controls=[
                    Text(
                        value=f'{await self.client.session.gtv(key=product["name_text"])} '
                              f'{product["meal_product"]["value"]} {await self.client.session.gtv(key="gr")}'
                    )
                    for product in self.products
                ],
            )
            controls.append(product_buttons)

            if self.image_data:
                base64_image = base64.b64encode(self.image_data).decode()
                image = Image(src=f"data:image/jpeg;base64,{base64_image}")
                controls.append(image)

            button = FilledButton(
                content=Text(value=await self.client.session.gtv(key='delete')),
                on_click=self.delete_meal_report,
            )
            controls.append(button)
        else:
            not_report_text = Text(
                value=await self.client.session.gtv(key='not_report'),
                size=20,
                font_family=Fonts.MEDIUM,
            )
            controls.append(not_report_text)

        if self.training_report:
            self.tf_comment = Text(
                value=self.report['comment'],
                size=20,
                font_family=Fonts.MEDIUM,
            )
            button = FilledButton(
                content=Text(
                    value=await self.client.session.gtv(key='delete'),
                ),
                on_click=self.delete_training_report,
            )
            controls = [self.tf_comment, button]
        else:
            self.tf_not_report = Text(
                value=await self.client.session.gtv(key='not_report'),
                size=20,
                font_family=Fonts.MEDIUM,
            )
            controls = [self.tf_not_report]

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='report'),
            main_section_controls=controls,
        )

    async def delete_training_report(self, _):
        await self.client.session.api.admin.trainings.reports.delete(
            id_=self.training_report_id,
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def delete_meal_report(self, _):
        await self.client.session.api.admin.meals.reports.delete(
            id_=self.meal['meal_report_id'],
        )
        await self.client.change_view(go_back=True, with_restart=True, delete_current=True)
