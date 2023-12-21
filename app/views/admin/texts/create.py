#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
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

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.texts import TextView


class CreateTextView(View):
    route = '/admin'
    tf_value_default: TextField
    tf_key: TextField

    async def build(self):
        self.tf_value_default = TextField(
            label=await self.client.session.gtv(key='Name Default'),
        )
        self.tf_key = TextField(
            label=await self.client.session.gtv(key='Key'),
        )
        self.controls = [
            await self.get_header(),
            Container(
                Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='create_text'),
                            create_button=False,
                        ),
                        self.tf_value_default,
                        self.tf_key,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='Create'),
                                size=15,
                                font_family=Fonts.REGULAR,
                            ),
                            on_click=self.create_text,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_text(self, _):
        if len(self.tf_value_default.value) < 1 or len(self.tf_value_default.value) > 1024:
            self.tf_value_default.error_text = await self.client.session.gtv(key='value_default_min_max_letter')
        elif len(self.tf_key.value) < 2 or len(self.tf_key.value) > 128:
            self.tf_key.error_text = await self.client.session.gtv(key='key_min_max_letter')
        else:
            response = await self.client.session.api.text.create(
                value_default=self.tf_value_default.value,
                key=self.tf_key.value,
            )
            text_id = response.id
            await self.client.change_view(view=TextView(text_id=text_id))
        await self.update_async()
        for field in [
            self.tf_value_default,
            self.tf_key,
        ]:
            field.error_text = None
