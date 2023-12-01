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


from flet_core import Column

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AuthView


class AuthenticationView(AuthView):
    route = '/authentication'
    tf_username: TextField
    tf_password: TextField

    async def auntificate(self, _):
        await self.set_type(loading=True)

        # Create session
        username = self.tf_username.value
        password = self.tf_password.value
        session = await self.client.session.api.session.create(
            username=username,
            password=password,
        )

        # Get result, set in CS
        token = session.token
        await self.client.session.set_cs(key='token', value=token)

        # Change view
        view = await self.client.session.init()
        await self.set_type(loading=False)
        await self.client.change_view(view=view)

    async def build(self):
        self.tf_username = TextField(
            label=await self.client.session.gtv(key='username'),
        )
        self.tf_password = TextField(
            label=await self.client.session.gtv(key='password'),
            password=True,
        )

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='login'),
            controls=[
                Column(
                    controls=[
                        self.tf_username,
                        self.tf_password,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='login'),
                                size=16,
                            ),
                            on_click=self.auntificate,
                        ),
                    ],
                    spacing=20,
                ),
            ],
        )
