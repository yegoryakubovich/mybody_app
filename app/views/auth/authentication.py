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


from flet_core import Column, Row, Container, padding
from mybody_api_client.utils.base_section import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AuthView
from app.utils import Fonts


class AuthenticationView(AuthView):
    tf_username: TextField
    tf_password: TextField

    async def authenticate(self, _):
        await self.set_type(loading=True)

        # Create session
        username = self.tf_username.value
        password = self.tf_password.value
        try:
            session = await self.client.session.api.client.session.create(
                username=username,
                password=password,
            )
        except ApiException:
            await self.set_type(loading=False)
            return await self.client.session.error(code=0)
        
        # Get result, set in CS
        token = session
        await self.client.session.set_cs(key='token', value=token)

        # Change view
        self.client.page.views.clear()
        view = await self.client.session.init()
        await self.set_type(loading=False)
        await self.client.change_view(view=view)

    async def go_registration(self, _):
        from app.views.auth.registration import RegistrationFirstView
        await self.client.change_view(view=RegistrationFirstView(), delete_current=True)

    async def build(self):
        self.tf_username = TextField(
            label=await self.client.session.gtv(key='username'),
        )
        self.tf_password = TextField(
            label=await self.client.session.gtv(key='password'),
            password=True,
        )

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='authorization'),
            controls=[
                Column(
                    controls=[
                        self.tf_username,
                        self.tf_password,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='sign_in'),
                                size=16,
                            ),
                            on_click=self.authenticate,
                            horizontal_padding=54,
                        ),
                        Container(
                            content=Row(
                                controls=[
                                    Text(
                                        value=await self.client.session.gtv(key='authentication_view_question'),
                                        size=16,
                                        font_family=Fonts.REGULAR,
                                    ),
                                    Text(
                                        value=await self.client.session.gtv(key='create'),
                                        size=16,
                                        font_family=Fonts.SEMIBOLD,
                                        color='#008F12',  # FIXME
                                    ),
                                ],
                                spacing=4,
                            ),
                            on_click=self.go_registration,
                            ink=True,
                            padding=padding.symmetric(vertical=4),
                        ),
                    ],
                    spacing=20,
                ),
            ],
        )
