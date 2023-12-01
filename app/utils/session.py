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

from flet_core import Page
from flet_manager.utils import Client
from mybody_api_client import MyBodyApiClient


class Session:
    client: Client
    page: Page
    token: str | None
    language: str | None
    api: MyBodyApiClient

    def __init__(self, client: Client):
        self.client = client
        self.page = client.page

    async def init(self):
        self.token = await self.get_cs(key='token')
        self.language = await self.get_cs(key='language')

        self.api = MyBodyApiClient(token=self.token)
        account = await self.api.account.get()

        if account.state == 'error':
            self.token = None
            await self.set_cs(key='token', value=self.token)

            from app.views.authentication import AuthenticationView

            # Return view
            if not self.client.session.language:
                from app.views.set_language import SetLanguageView

                # Go to Set Language
                return SetLanguageView(
                    languages=await self.client.session.api.language.get_list(),
                    next_view=AuthenticationView(),
                )
            else:
                # Go to Auth
                return AuthenticationView()

        else:
            if self.language != account.language:
                await self.set_cs(key='language', value=self.language)
            self.language = account.language
            from app.views.main import MainView
            # Go to Main
            return MainView()

    # Client storage
    async def get_cs(self, key: str) -> Any:
        try:
            value = await self.page.client_storage.get_async(key=f'mybody.{key}')
            if value == 'null':
                value = None
            return value
        except RecursionError:
            return None

    async def set_cs(self, key: str, value: Any) -> None:
        if value is None:
            value = 'null'
        return await self.page.client_storage.set_async(key=f'mybody.{key}', value=value)

    # Texts
    @staticmethod
    async def get_text_value(key):
        # FIXME
        return key.title()

    async def gtv(self, key):
        return await self.get_text_value(key=key)
