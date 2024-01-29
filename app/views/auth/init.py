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


from app.controls.input import Dropdown
from app.controls.layout import AuthView
from app.utils import Session
from app.views.main import MainView
from app.views.auth.language import LanguageView
from app.views.auth.authentication import AuthenticationView
from config import settings


class InitView(AuthView):
    dropdown: Dropdown
    languages: list

    async def get_text_pack(self, language: str):
        text_pack = await self.client.session.api.client.text.get_pack(language=language)
        await self.client.session.set_cs(key='text_pack', value=text_pack)

    async def on_load(self):
        await self.set_type(loading=True)
        self.client.session = Session(client=self.client)
        await self.client.session.init()
        await self.set_type(loading=False)

        # If not language
        if not self.client.session.language:
            await self.client.change_view(view=LanguageView())
            return

        await self.get_text_pack(language=self.client.session.language)

        # If not token
        if not self.client.session.token:
            await self.client.change_view(view=AuthenticationView())
            return

        # Get account service
        account_services = await self.client.session.api.client.account.get_list_services()
        account_service = None
        for as_ in account_services:
            if as_.service_id == settings.service_id:
                account_service = as_

        if account_service:
            self.client.session.account_service = account_service
        else:
            # Переход на покупку
            # await self.client.session.error(0)
            pass

        await self.client.change_view(view=MainView())
