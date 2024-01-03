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


from flet_core import Column
from flet_manager.utils import Client

from app.controls.layout import View


class BaseTab(Column):
    def __init__(self, client: Client, view: View, **kwargs):
        super().__init__(**kwargs)
        self.client = client
        self.view = view

    async def build(self):
        pass

    async def on_load(self):
        await self.view.client.page.update_async()

    async def get(self):
        return self
