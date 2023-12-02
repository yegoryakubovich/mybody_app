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


from flet_manager.views import BaseView

from app.controls.information.loading import Loading
from app.utils import Session


class View(BaseView):
    title = 'My Body'
    controls_last: list = []
    session: Session

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = 0
        self.spacing = 0

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
