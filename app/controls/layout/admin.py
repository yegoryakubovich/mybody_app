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


from typing import Any

from app.controls.layout.view import View


class Section:
    title: list
    controls: list

    def __init__(self, title: list, controls: list):
        self.title = title
        self.controls = controls

    async def get_controls(self) -> list:
        title_control = self.title[0]
        controls = [
            title_control
        ] + self.controls
        return controls


class AdminView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 0
        self.spacing = 0

    async def get_controls(
            self,
            title: str,
            main_section_controls: list,
            sections: list[Section] = None,
            on_create_click: Any = None,
    ) -> list:

        title_control = await self.get_title(title=title, on_create_click=on_create_click)

        controls = [title_control] + main_section_controls
        if sections is not None:
            for section in sections:
                controls += await section.get_controls()

        return controls
