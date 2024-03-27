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


from base64 import b64encode
from io import BytesIO
import os
from json import dumps
from functools import partial
from typing import Any

from flet_core import ScrollMode, AlertDialog, Container, Column, FilePickerUploadFile, Image, Row, \
    MainAxisAlignment, TextButton, IconButton, icons, FilePickerUploadEvent, colors, ListTile
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton, ProductChipButton
from app.controls.information import Text
from app.controls.information.search_bar import SearchBar
from app.controls.input import TextField
from app.controls.layout import ClientBaseView
from app.utils import Fonts, Error


class MealReportView(ClientBaseView):
    tf_comment: TextField
    tf_quantity: TextField
    dlg_modal: AlertDialog
    user_comment: str = ''
    products: list[dict]
    product: dict
    added_product_controls = None
    added_photo_controls = None
    file_name: str = None
    search_bar: Any

    def __init__(self, meal_id):
        super().__init__()
        self.add_photo_button = None
        self.photos = []
        self.added_products = []
        self.data_io = None
        self.meal_id = meal_id

    async def build(self):
        await self.set_type(loading=True)
        self.products = await self.client.session.api.client.products.get_list(
            type_=None,
        )
        await self.set_type(loading=False)

        self.tf_comment = TextField(
            value=self.user_comment,
            on_change=self.save_user_comment,
        )

        self.tf_quantity = TextField(
            label=await self.client.session.gtv(key='quantity'),
        )
        self.search_bar = SearchBar(
            on_change=self.on_search_product,
            bar_hint_text=await self.client.session.gtv(key='search'),
            controls=[
                ListTile(
                    title=Text(
                        value=await self.client.session.gtv(key=product['name_text']),
                    ),
                    on_click=self.close_dlg_modal,
                    data=product
                )
                for product in self.products
            ]
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
                        self.search_bar,
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
                Row(
                    controls=[
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='add'),
                                size=16,
                            ),
                            on_click=self.add_product
                        ),
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='close'),
                                size=16,
                            ),
                            on_click=self.close_dlg,
                        ),
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
            modal=False,
        )
        controls = []
        for self.product, quantity in self.added_products:
            controls.append(
                Row(
                    controls=[
                        ProductChipButton(
                            Text(
                                value=await self.client.session.gtv(
                                    key=self.product['name_text']
                                ) + ' ' + quantity + ' ' + await self.client.session.gtv(key='gr')
                            ).value,
                            on_click=None,
                        ),
                        IconButton(
                            icon=icons.DELETE,
                            on_click=partial(self.remove_product, self.product, quantity),
                        ),
                    ],
                    spacing=1,
                ),
            )
        self.added_product_controls = [
            Row(
                controls=controls,
            ),
        ]
        self.added_photo_controls = [
            Row(
                controls=[
                    Image(
                        src=f"data:image/jpeg;base64,{photo}",
                        width=150,
                        height=150,
                    )
                    for photo in self.photos
                ],
            )
        ]
        self.add_photo_button = FilledButton(
            content=Text(
                value=await self.client.session.gtv(key='add'),
            ),
            on_click=self.add_photo,
            disabled=len(self.photos) == 2,
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='client_meal_report_create_view'),
            main_section_controls=[
                self.dlg_modal,
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_guide_view'),
                    size=20,
                    font_family=Fonts.REGULAR,
                    color=colors.ON_BACKGROUND,
                ),
                Text(
                    value=await self.client.session.gtv(key='products'),
                    size=25,
                    font_family=Fonts.BOLD,
                    color=colors.ON_BACKGROUND,
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
                    color=colors.ON_BACKGROUND,
                ),
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_comment_guide_view'),
                    size=20,
                    font_family=Fonts.REGULAR,
                    color=colors.ON_BACKGROUND,
                ),
                self.tf_comment,
                Text(
                    value=await self.client.session.gtv(key='photos'),
                    size=25,
                    font_family=Fonts.BOLD,
                    color=colors.ON_BACKGROUND,
                ),
                Text(
                    value=await self.client.session.gtv(key='client_meal_report_text_photo_guide_view'),
                    size=20,
                    font_family=Fonts.REGULAR,
                    color=colors.ON_BACKGROUND,
                ),
                *self.added_photo_controls,
                self.add_photo_button,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='send_report'),
                    ),
                    on_click=self.create_report,
                ),
            ]
        )

    async def on_upload_progress(self, e: FilePickerUploadEvent):
        if e.progress is not None and e.progress < 1.0:
            pass
        else:
            path = f'upload/{e.file_name}'
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    image_data = f.read()
                self.data_io = BytesIO(image_data)
                encoded_image_data = b64encode(image_data).decode()
                self.file_name = e.file_name
                self.photos.append(encoded_image_data)
                await self.restart()
            else:
                pass

    async def upload_files(self, _):
        uf = []
        if self.client.session.filepicker.result.files:
            for f in self.client.session.filepicker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=await self.client.session.page.get_upload_url_async(f.name, 600),
                    )
                )
                await self.client.session.filepicker.upload_async([uf[-1]])
                await self.on_upload_progress(e=FilePickerUploadEvent(file_name=f.name, progress=1.0, error=None))

    async def add_photo(self, _):
        await self.client.session.filepicker.open_(
            on_select=self.upload_files,
            on_upload=self.on_upload_progress,
            allowed_extensions=['svg', 'jpg'],
        )

    async def remove_product(self, product_to_remove, quantity_to_remove, _):
        self.added_products = [(product, quantity) for (product, quantity) in self.added_products if not (
                product['id'] == product_to_remove['id'] and quantity == quantity_to_remove)]
        await self.restart()

    async def save_user_comment(self, event):
        self.user_comment = event.data

    async def close_dlg(self, _):
        self.dlg_modal.open = False
        await self.restart()

    async def open_dlg(self, _):
        self.dlg_modal.open = True
        await self.update_async()

    async def add_product(self, _):
        fields = [(self.tf_quantity, 1, 3, True)]
        for field, min_len, max_len, check_int in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len, check_int=check_int):
                return
        self.added_products.append((self.product, self.tf_quantity.value))
        await self.close_dlg(_)

    async def create_report(self, _):
        await self.set_type(loading=True)
        if len(self.added_products) > 0:
            product_list = [{"id": product[0]['id'], "value": int(product[1])} for product in self.added_products]
            product_list_json = dumps(product_list, ensure_ascii=False)
        else:
            product_list_json = None
        try:
            id_meal_report = await self.client.session.api.client.meals.reports.create(
                meal_id=self.meal_id,
                comment=self.tf_comment.value or None,
                products=product_list_json,
            )
            if self.data_io:
                await self.client.session.api.client.images.create(
                    model='meal_report',
                    model_id=id_meal_report,
                    file=self.data_io.read(),
                )
            await self.set_type(loading=False)
            await self.client.change_view(go_back=True, with_restart=True, delete_current=True)
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)

    async def on_search_product(self, search_text):
        filtered_products = []
        for product in self.products:
            product_name = await self.client.session.gtv(key=product['name_text'])
            if search_text.data.lower() in product_name.lower():
                filtered_products.append(product)

        self.search_bar.controls = [
            ListTile(
                title=Text(
                    value=await self.client.session.gtv(key=product['name_text']),
                ),
                on_click=self.close_dlg_modal,
                data=product
            )
            for product in filtered_products
        ]
        await self.update_async()

    async def close_dlg_modal(self, e):
        self.product = await self.client.session.api.client.products.get(id_=e.control.data['id'])
        await self.search_bar.close_view_async(await self.client.session.gtv(key=self.product['name_text']))
