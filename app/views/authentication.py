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

from app.controls.buttons import FilledButton
from app.controls.informations import Text
from app.controls.inputs import TextField
from app.controls.layouts import AuthView


class AuthenticationView(AuthView):
    route = '/authentication'

    async def build(self):
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='login'),
            controls=[
                Column(
                    controls=[
                        TextField(
                            label=await self.client.session.gtv(key='username'),
                        ),
                        TextField(
                            label=await self.client.session.gtv(key='password'),
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='login'),
                                size=16,
                            ),
                        ),
                    ],
                    spacing=20,
                ),
            ],
        )
