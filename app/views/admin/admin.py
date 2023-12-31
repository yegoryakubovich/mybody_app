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


from typing import Any

from flet_core import ScrollMode
from flet_manager.utils import get_svg

from app.controls.layout import AdminBaseView
from .accounts.get_list import AccountListView
from .articles.get_list import ArticleListView
from .countries import CountryListView
from .currencies.get_list import CurrencyListView
from .exercises.get_list import ExerciseListView
from .languages.get_list import LanguageListView
from .permissions import PermissionListView
from .products.get_list import ProductListView
from .roles import RoleListView
from .services import ServiceListView
from .texts.get_list import TextListView
from .timezones.get_list import TimezoneListView
from .trainings.get_list import TrainingListView
from ...controls.button import ListItemButton


class Setting:
    name: str
    icon: str
    on_click: Any

    def __init__(self, name: str, icon: str, on_click: Any):
        self.name = name
        self.icon = icon
        self.on_click = on_click


class Section:
    settings: list[Setting]

    def __init__(self, settings: list[Setting]):
        self.settings = settings


class AdminView(AdminBaseView):
    route = '/admin'

    async def build(self):
        self.scroll = ScrollMode.AUTO
        self.bgcolor = '#FFFFFF'
        parts = [
            Setting(
                name='admin_account_get_list_view_title',
                icon='notifications',
                on_click=self.get_accounts,
            ),
            Setting(
                name='admin_article_get_list_view_title',
                icon='notifications',
                on_click=self.get_articles,
            ),
            Setting(
                name='admin_text_get_list_view_title',
                icon='notifications',
                on_click=self.get_texts,
            ),
            Setting(
                name='admin_product_get_list_view_title',
                icon='notifications',
                on_click=self.get_products,
            ),
            Setting(
                name='admin_language_get_list_view_title',
                icon='notifications',
                on_click=self.get_languages,
            ),
            Setting(
                name='admin_currency_get_list_view_title',
                icon='notifications',
                on_click=self.get_currencies,
            ),
            Setting(
                name='admin_timezone_get_list_view_title',
                icon='notifications',
                on_click=self.get_timezones,
            ),
            Setting(
                name='admin_country_get_list_view_title',
                icon='notifications',
                on_click=self.get_countries,
            ),
            Setting(
                name='admin_exercise_get_list_view_title',
                icon='notifications',
                on_click=self.get_exercises,
            ),
            Setting(
                name='admin_permission_get_list_view_title',
                icon='notifications',
                on_click=self.get_permissions,
            ),
            Setting(
                name='admin_role_get_list_view_title',
                icon='notifications',
                on_click=self.get_roles,
            ),
            Setting(
                name='admin_service_get_list_view_title',
                icon='notifications',
                on_click=self.get_services,
            ),
            Setting(
                name='trainings',
                icon='notifications',
                on_click=self.get_trainings,
            ),
        ]

        main_sections_controls = [
            ListItemButton(
                icon=get_svg(path=f'assets/icons/{setting.icon}.svg'),
                name=await self.client.session.gtv(key=setting.name),
                on_click=setting.on_click,
            )
            for setting in parts
        ]

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_view_title'),
            main_section_controls=main_sections_controls,
        )

    async def coming_soon(self):
        pass

    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def get_articles(self, _):
        await self.client.change_view(view=ArticleListView())

    async def get_texts(self, _):
        await self.client.change_view(view=TextListView())

    async def get_accounts(self, _):
        await self.client.change_view(view=AccountListView())

    async def get_products(self, _):
        await self.client.change_view(view=ProductListView())

    async def get_languages(self, _):
        await self.client.change_view(view=LanguageListView())

    async def get_currencies(self, _):
        await self.client.change_view(view=CurrencyListView())

    async def get_timezones(self, _):
        await self.client.change_view(view=TimezoneListView())

    async def get_countries(self, _):
        await self.client.change_view(view=CountryListView())

    async def get_services(self, _):
        await self.client.change_view(view=ServiceListView())

    async def get_exercises(self, _):
        await self.client.change_view(view=ExerciseListView())

    async def get_trainings(self, _):
        await self.client.change_view(view=TrainingListView())

    async def get_permissions(self, _):
        await self.client.change_view(view=PermissionListView())

    async def get_roles(self, _):
        await self.client.change_view(view=RoleListView())
