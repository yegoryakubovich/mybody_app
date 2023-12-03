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


from flet_core import ListView, padding
from flet_manager.utils import get_svg

from app.controls.layout.view import View
from app.controls.navigation import BottomNavigation, BottomNavigationTab
from .tabs import HomeTab, StatsTab, AccountTab


class Tab:
    def __init__(self, name: str, icon_path: str, control):
        self.name = name
        self.icon = get_svg(path=icon_path)
        self.control = control


TABS = [
    Tab(
        name='Home',
        icon_path='assets/icons/plan.svg',
        control=HomeTab,
    ),
    Tab(
        name='Statistcs',
        icon_path='assets/icons/stats.svg',
        control=StatsTab,
    ),
    Tab(
        name='Account',
        icon_path='assets/icons/account.svg',
        control=AccountTab,
    ),
]


class MainView(View):
    tab_selected: BottomNavigationTab
    tab_default: BottomNavigationTab
    body: ListView

    async def change_tab(self, tab: BottomNavigationTab):
        if not tab.name != self.tab_selected.name:
            return

        await self.tab_selected.set_state(activated=False)
        self.tab_selected = tab
        await self.tab_selected.set_state(activated=True)
        await self.set_body(control=self.tab_selected.control)

    async def set_body(self, control):
        control = control(client=self.client, view=self)
        await control.build()
        await control.on_load()
        self.body.controls = [await control.get()]
        await self.body.update_async()

    async def on_load(self):
        self.tab_selected = self.tab_default
        await self.tab_default.set_state(activated=True)
        await self.set_body(control=self.tab_selected.control)

    async def build(self):
        self.body = ListView(expand=True, padding=padding.only(bottom=36))
        tabs = [
            BottomNavigationTab(
                name=tab.name,
                icon=tab.icon,
                control=tab.control,
            )
            for tab in TABS
        ]
        self.tab_default = tabs[0]

        self.controls = [
            # Header
            await self.get_header(),

            # Body
            self.body,

            # Bottom Navigation
            BottomNavigation(
                on_click_tab=self.change_tab,
                tabs=tabs,
            ),
        ]
