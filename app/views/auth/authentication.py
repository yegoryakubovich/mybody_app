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


from flet_core import Column, Row, Container, padding, colors, MainAxisAlignment, border_radius
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AuthView
from app.utils import Fonts, Error


class AuthenticationView(AuthView):
    tf_username: TextField
    tf_password: TextField

    async def authenticate(self, _):
        fields = [(self.tf_username, 5, 32), (self.tf_password, 7, 32)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                return
        # Create session
        try:
            await self.set_type(loading=True)
            session = await self.client.session.api.client.sessions.create(
                username=self.tf_username.value.replace(' ', ''),
                password=self.tf_password.value.replace(' ', ''),
            )
            await self.set_type(loading=False)
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
        
        # Get result, set in CS
        token = session.token
        await self.client.session.set_cs(key='token', value=token)

        # Change view
        self.client.page.views.clear()
        await self.set_type(loading=False)
        from app.views.auth.init import InitView
        await self.client.change_view(view=InitView())

    async def go_registration(self, _):
        from app.views.auth.registration import RegistrationFirstView
        await self.client.change_view(view=RegistrationFirstView(), delete_current=True)

    async def go_language(self, _):
        from app.views.auth import LanguageView
        await self.client.change_view(view=LanguageView(), delete_current=True)

    async def build(self):
        self.tf_username = TextField(
            label=await self.client.session.gtv(key='username'),
        )
        self.tf_password = TextField(
            label=await self.client.session.gtv(key='password'),
            password=True,
            can_reveal_password=True,
        )

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='authorization'),
            controls=[
                Column(
                    controls=[
                        self.tf_username,
                        self.tf_password,
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='sign_in'),
                                        size=16,
                                    ),
                                    on_click=self.authenticate,
                                    horizontal_padding=54,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='language'),
                                        size=16,
                                    ),
                                    on_click=self.go_language,
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        Container(
                            content=Row(
                                controls=[
                                    Text(
                                        value=await self.client.session.gtv(key='authentication_view_question'),
                                        size=16,
                                        font_family=Fonts.REGULAR,
                                        color=colors.ON_BACKGROUND,
                                    ),
                                    Text(
                                        value=await self.client.session.gtv(key='create'),
                                        size=16,
                                        font_family=Fonts.SEMIBOLD,
                                        color=colors.PRIMARY,
                                    ),
                                ],
                                spacing=4,
                            ),
                            on_click=self.go_registration,
                            ink=True,
                            padding=padding.symmetric(vertical=4),
                            border_radius=border_radius.all(6),
                        ),
                    ],
                    spacing=20,
                ),
            ],
        )
