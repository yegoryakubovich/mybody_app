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

from flet_core import Page
from flet_manager.utils import Client
from mybody_api_client import MyBodyApiClient
from mybody_api_client.utils.base_section import ApiException

from app.utils.registration import Registration
from config import IS_TEST


class Session:
    client: Client
    page: Page
    token: str | None
    language: str | None
    text_pack_id: int | None
    text_pack_language: str | None
    text_pack: dict | None
    api: MyBodyApiClient
    registration: Registration

    def __init__(self, client: Client):
        self.client = client
        self.page = client.page
        self.account = None

    async def init(self):
        self.token = await self.get_cs(key='token')
        self.language = await self.get_cs(key='language')
        self.text_pack = await self.get_cs(key='text_pack')

        self.api = MyBodyApiClient(token=self.token, is_test=IS_TEST)

        try:
            self.account = await self.api.client.account.get()
            self.language = self.account.language
            if self.language != self.account.language:
                await self.set_cs(key='language', value=self.language)
        except ApiException:
            await self.set_cs(key='token', value=None)

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
    async def get_text_value(self, key):
        if key is not None:
            try:
                return self.text_pack[key]
            except KeyError:
                return f'404 {key}'
        else:
            return None

    async def gtv(self, key):
        return await self.get_text_value(key=key)
