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

from app.controls.input import TextField
from app.controls.layout import View


class TrainingView(View):
    route = '/admin'
    tf_key = TextField
    tf_value_default = TextField
    text = list[dict]

    def __init__(self, text_id):
        super().__init__()
        self.text_id = text_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.text.get(
            id_=self.text_id
        )
        self.text = response.text
        await self.set_type(loading=False)

        self.tf_key = TextField(
            label=await self.client.session.gtv(key='key'),
            value=await self.client.session.gtv(key=self.text['key'])
        )
        self.tf_value_default = TextField(
            label=await self.client.session.gtv(key='value_default'),
            value=await self.client.session.gtv(key=self.text['value_default'])
        )
        self.scroll = ScrollMode.AUTO
