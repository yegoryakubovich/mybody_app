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


from flet_core import Container, alignment, Column

from app.controls.buttons import FilledButton
from app.controls.layouts import View
from app.utils import Session
from app.views import AuthenticationView


class SplashView(View):
    route = '/splash'

    async def init_session(self):
        self.client.session = Session()

    async def go_authentication(self, _):
        await self.client.change_view(view=AuthenticationView())

    async def build(self):
        # FIXME
        await self.init_session()

        self.controls = [
            Column(
                controls=[
                    Container(
                        content=FilledButton(
                            text='Authentication',
                            on_click=self.go_authentication,
                        ),
                        expand=True,
                        alignment=alignment.center,
                    ),
                ],
                expand=True,
            ),
        ]
