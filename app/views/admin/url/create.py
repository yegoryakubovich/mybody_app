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


from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AdminBaseView
from app.utils import Error


class UrlCreateView(AdminBaseView):
    route = '/admin/url/create'
    tf_name: TextField
    tf_redirect: TextField

    async def build(self):
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.tf_redirect = TextField(
            label=await self.client.session.gtv(key='redirect'),
        )

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_url_create_view_title'),
            main_section_controls=[
                self.tf_name,
                self.tf_redirect,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_url,
                ),
            ],
         )

    async def create_url(self, _):
        fields = [(self.tf_name, 1, 64), (self.tf_redirect, 1, 1024)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                return
        try:
            await self.set_type(loading=True)
            await self.client.session.api.admin.urls.create(
                name=self.tf_name.value,
                redirect=self.tf_redirect.value,
            )
            await self.set_type(loading=False)
            await self.client.change_view(go_back=True, with_restart=True, delete_current=True)
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
