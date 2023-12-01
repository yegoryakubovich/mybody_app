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


from flet_core import Container, alignment, Column, MainAxisAlignment, CrossAxisAlignment

from app.controls.button import FilledButton
from app.controls.layout import View
from app.utils import Session


class SplashView(View):
    route = '/splash'

    async def init(self, _):
        await self.set_type(loading=True)
        self.client.session = Session(client=self.client)
        view = await self.client.session.init()
        await self.set_type(loading=False)
        await self.client.change_view(view=view)

    async def clear_cs(self, _):
        self.client.session = Session(client=self.client)
        await self.client.session.set_cs(key='language', value=None)
        await self.client.session.set_cs(key='token', value=None)

    async def build(self):
        self.controls = [
            Column(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                FilledButton(
                                    text='Start',
                                    on_click=self.init,
                                ),
                                FilledButton(
                                    text='Clear CS',
                                    on_click=self.clear_cs,
                                ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        alignment=alignment.center,
                    ),
                ],
                expand=True,
            ),
        ]
