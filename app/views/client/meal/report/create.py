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

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import ClientBaseView
from app.utils import Fonts


class MealReportView(ClientBaseView):
    tf_comment: TextField
    tf_product: TextField
    products: list[dict]
    bottom_sheet = None
    nutrient_type = None

    def __init__(self):
        super().__init__()
        self.bottom_sheet = None
        self.product_suggestions = []

    async def build(self):
        await self.set_type(loading=True)
        self.products = await self.client.session.api.client.product.get_list(
            type_=self.nutrient_type,
        )
        await self.set_type(loading=False)
        self.scroll = ScrollMode.ALWAYS
        self.tf_comment = TextField()

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='client_meal_report_create_view'),
            main_section_controls=[
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_guide_view'),
                    size=18,
                    font_family=Fonts.REGULAR,
                ),
                Text(
                    value=await self.client.session.gtv(key='products'),
                    size=25,
                    font_family=Fonts.BOLD,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='add'),
                    ),
                    on_click=self.add_product,
                ),
                Text(
                    value=await self.client.session.gtv(key='comment'),
                    size=25,
                    font_family=Fonts.BOLD,
                ),
                self.tf_comment,
                Text(
                    value=await self.client.session.gtv(key='photos'),
                    size=25,
                    font_family=Fonts.BOLD,
                ),
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_photo_guide_view'),
                    size=18,
                    font_family=Fonts.REGULAR,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='add'),
                    ),
                    on_click=self.add_photo,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='send_report'),
                    ),
                    on_click=self.send_report,
                ),
            ],
        )

    async def add_product(self, _):
        pass

    async def add_photo(self, _):
        pass

    async def send_report(self, _):
        pass
