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


from flet_core import Image, Container, padding, alignment, Column, ScrollMode
from flet_manager.utils import get_svg

from app.controls.information import Text
from app.controls.layout.view import View
from app.utils import Fonts


class AuthView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll = ScrollMode.AUTO

    @staticmethod
    async def get_controls(
            controls: list,
            title: str = None,
    ) -> list:

        controls = [
            Container(
                content=Column(
                    controls=[
                        # Header
                        Container(
                            content=Image(
                                src=get_svg(
                                    path='assets/icons/logos/logo_2_full.svg',
                                ),
                                height=56,
                            ),
                            alignment=alignment.center,
                            padding=padding.symmetric(vertical=32, horizontal=96),
                        ),
                        # Body
                        Column(
                            controls=[
                                Container(
                                    Text(
                                        value=title,
                                        size=36,
                                        font_family=Fonts.SEMIBOLD,
                                    ),
                                ),
                            ] + controls,
                        ),
                    ],
                    width=640,
                ),
                alignment=alignment.center,
                padding=10,
            ),
        ]
        return controls
