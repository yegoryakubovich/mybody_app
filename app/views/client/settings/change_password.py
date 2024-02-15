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


from collections import defaultdict
from datetime import date
from typing import Any

from flet_core import Column, Container, Image, Row, ScrollMode, Text, padding, AlertDialog, colors
from flet_core import icons as FletIcons
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.input import TextField
from app.controls.layout import ClientBaseView
from app.utils import Fonts


class ChangePasswordView(ClientBaseView):
    old_password_tf: TextField
    old_password_repeat_tf: TextField
    new_password_tf: TextField
    controls_container: Container

    async def build(self):
        # self.client.session.account
        self.old_password_tf = TextField(
            label=await self.client.session.gtv(key='change_password_enter_current_password'),
            password=True,
            can_reveal_password=True,

        )
        self.old_password_repeat_tf = TextField(
            label=await self.client.session.gtv(key='change_password_repeat_current_password'),
            password=True,
        )
        self.new_password_tf = TextField(
            label=await self.client.session.gtv(key='change_password_enter_new_password'),
            password=True,
            can_reveal_password=True,
        )
        self.controls_container = Container(
            content=Column(
                controls=[
                    self.old_password_tf,
                    self.old_password_repeat_tf,
                    self.new_password_tf,
                    FilledButton(
                        text=await self.client.session.gtv(key='next'),
                        on_click=self.switch_tf,
                    )
                ],
                spacing=10,
            ),
            padding=padding.only(bottom=15),
        )
        controls = [
            self.controls_container
        ]
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='change_password'),
            main_section_controls=controls,
        )

    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def switch_tf(self, _):
        self.old_password_tf.error_text = None
        self.old_password_repeat_tf.error_text = None
        self.new_password_tf.error_text = None
        if self.old_password_tf.value != self.old_password_repeat_tf.value:
            self.old_password_tf.error_text = await self.client.session.gtv(key='change_password_do_not_match')
            await self.update_async()
            return

        try:
            await self.client.session.api.client.accounts.change_password(
                current_password=self.old_password_tf.value,
                new_password=self.new_password_tf.value,
            )
        except ApiException as e:
            if e.code == 2000:
                self.old_password_tf.error_text = e.message
            elif e.code == 2003:
                self.new_password_tf.error_text = e.message
            await self.update_async()
            return
        self.controls_container = Container(
            content=Column(
                [
                    Text(
                        value=await self.client.session.gtv(key='change_password_success'),
                        size=15,
                        font_family=Fonts.SEMIBOLD,
                    ),
                    FilledButton(
                        text=await self.client.session.gtv(key='go_back'),
                        on_click=self.go_back,
                    )
                ]
            )
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='change_password'),
            main_section_controls=[self.controls_container],
        )
        await self.update_async()