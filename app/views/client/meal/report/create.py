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

from flet_core import ScrollMode, AlertDialog, Container, Column, FilePicker, Image, ImageFit
from flet_core.dropdown import Option

from app.controls.button import FilledButton, ProductChipButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import ClientBaseView
from app.utils import Fonts


class MealReportView(ClientBaseView):
    tf_comment: TextField
    dd_product: Dropdown
    tf_quantity: TextField
    dlg_modal: AlertDialog
    products: list[dict]
    product: dict
    added_products = []
    bottom_sheet = None
    nutrient_type = None
    added_product_controls = None
    file_picker: FilePicker
    photos = []

    async def build(self):
        await self.set_type(loading=True)
        self.products = await self.client.session.api.client.product.get_list(
            type_=self.nutrient_type,
        )
        await self.set_type(loading=False)

        product_options = [
            Option(
                text=await self.client.session.gtv(key=product['name_text']),
                key=product['id'],
            ) for product in self.products
        ]
        self.tf_comment = TextField()
        self.dd_product = Dropdown(
            label=await self.client.session.gtv(key='product'),
            value=product_options[0].key,
            options=product_options,
        )
        self.tf_quantity = TextField(
            label=await self.client.session.gtv(key='quantity'),
        )
        self.dlg_modal = AlertDialog(
            content=Container(
                content=Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='add_product'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        self.dd_product,
                        Text(
                            value=await self.client.session.gtv(key='weight'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        self.tf_quantity,
                    ],
                ),
                height=220,
            ),
            actions=[
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='add'),
                        size=16,
                    ),
                    on_click=self.add_product
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='close'),
                        size=16,
                    ),
                    on_click=self.close_dlg,
                ),
            ],
            modal=False,
        )
        self.added_product_controls = [
            ProductChipButton(
                Text(
                    value=await self.client.session.gtv(key=product['name_text']) + ' ' + quantity + ' ' +
                          await self.client.session.gtv(key='gr')
                ).value,
                on_click=None,
            )
            for product, quantity in self.added_products
        ]
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='client_meal_report_create_view'),
            main_section_controls=[
                self.dlg_modal,
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_guide_view'),
                    size=20,
                    font_family=Fonts.REGULAR,
                ),
                Text(
                    value=await self.client.session.gtv(key='products'),
                    size=25,
                    font_family=Fonts.BOLD,
                ),
                *self.added_product_controls,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='add'),
                    ),
                    on_click=self.open_dlg,
                ),
                Text(
                    value=await self.client.session.gtv(key='comment'),
                    size=25,
                    font_family=Fonts.BOLD,
                ),
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_comment_guide_view'),
                    size=20,
                    font_family=Fonts.REGULAR,
                ),
                self.tf_comment,
                Text(
                    value=await self.client.session.gtv(key='photos'),
                    size=25,
                    font_family=Fonts.BOLD,
                ),
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_photo_guide_view'),
                    size=20,
                    font_family=Fonts.REGULAR,
                ),
                *[Image(
                    src=f"data:image/jpeg;base64,{base64.b64encode(photo.content).decode()}",
                    fit=ImageFit.CONTAIN,
                ) for photo in self.photos],
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='add'),
                    ),
                    on_click=None,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='send_report'),
                    ),
                    on_click=self.send_report,
                ),
            ]
        )

    async def add_photo(self, _):
        pass

    async def close_dlg(self, _):
        self.dlg_modal.open = False
        await self.update_async()

    async def open_dlg(self, _):
        self.dlg_modal.open = True
        await self.update_async()

    async def add_product(self, _):
        await self.close_dlg(_)
        product_id = self.dd_product.value
        quantity = self.tf_quantity.value
        product = await self.client.session.api.client.product.get(id_=product_id)
        self.added_products.append((product, quantity))
        await self.restart()
        await self.update_async()

    async def send_report(self, _):
        pass
