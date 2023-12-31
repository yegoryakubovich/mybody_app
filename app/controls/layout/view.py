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


from flet_core import Container, Image, alignment, padding, BoxShadow, Row, MainAxisAlignment
from flet_manager.utils import get_svg
from flet_manager.views import BaseView

from app.controls.information import Text
from app.controls.information.loading import Loading
from app.utils import Fonts


class View(BaseView):
    title = 'My Body'
    controls_last: list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 0
        self.spacing = 0

    @staticmethod
    async def get_header():
        return Container(
            content=Image(
                src=get_svg(
                    path='assets/icons/logos/logo_2_full.svg',
                ),
                height=34,
            ),
            alignment=alignment.center,
            padding=padding.symmetric(vertical=18, horizontal=96),
            bgcolor='#FFFFFF',  # FIXME
            shadow=BoxShadow(
                color='#DDDDDD',  # FIXME
                spread_radius=1,
                blur_radius=20,
            ),
        )

    async def get_title(self, title: str, go_back_button=True, on_create_click=None):

        async def go_back(_):
            await self.client.change_view(go_back=True)

        left_controls = [
            Container(
                content=Image(
                    src=get_svg(path='assets/icons/arrow_back.svg'),
                    height=20,
                    color='#000000',
                ),
                ink=True,
                on_click=go_back,
            ),
            Text(
                value=title,
                size=36,
                font_family=Fonts.SEMIBOLD,
            ),
        ]

        right_controls = []

        if on_create_click:
            right_controls.append(
                Container(
                    content=Row(
                        controls=[
                            Image(
                                src=get_svg(path='assets/icons/addition.svg'),
                                height=10,
                                color='#FFFFFF',
                            ),
                            Text(
                                value='Create',
                                size=13,
                                font_family=Fonts.SEMIBOLD,
                                color='#FFFFFF',
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=7,
                    border_radius=24,
                    bgcolor='#008F12',
                    on_click=on_create_click,
                ),
            )

        return Row(
            controls=[
                Container(
                    content=Row(controls=left_controls),
                ),
                Container(
                    content=Row(controls=right_controls),
                ),
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )

    async def set_type(self, loading: bool = False):
        if loading:
            self.controls_last = self.controls
            self.controls = [
                Loading(infinity=True, color='#008F12'),
            ]
            await self.update_async()
        else:
            loading_control = self.controls[0]
            loading_control.infinity = False

            self.controls = self.controls_last
            await self.update_async()
