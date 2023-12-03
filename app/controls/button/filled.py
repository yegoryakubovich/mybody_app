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


from flet_core import FilledButton as FletFilledButton, ButtonStyle, MaterialState, RoundedRectangleBorder, padding


class FilledButton(FletFilledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style = ButtonStyle(
            padding={
                MaterialState.DEFAULT: padding.symmetric(horizontal=54, vertical=14),
            },
            shape={
                MaterialState.DEFAULT: RoundedRectangleBorder(radius=4),
            },
        )
