# Copyright 2022 H2O.ai, Inc.
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

import json
from bokeh.util.version import __version__ as bokeh_version
from bokeh.model import Model
from bokeh.embed import json_item

from h2o_nitro import box, Box, Plugin, Script

# Javascript function for embedding the Bokeh plot.
# See: http://docs.bokeh.org/en/latest/docs/user_guide/embed.html#json-items
# Here, we export one function called embed(), which we can later invoke from our Python box().
_bokeh_embed_js = '''
exports.embed = (context, element, data) => {
    Bokeh.embed.embed_item(JSON.parse(data.model), element.id);
};
'''


def bokeh_plugin():
    """
    Creates a Nitro plugin for the currently installed version of Bokeh.
    :return: A plugin
    """
    return Plugin(
        name='bokeh',
        scripts=[
            # Install the Bokeh library.
            Script(source=f'https://cdnjs.cloudflare.com/ajax/libs/bokeh/{bokeh_version}/bokeh.min.js'),
            # Install our custom Bokeh-embedding Javascript.
            Script(source=_bokeh_embed_js, type='inline'),
        ],
    )


def bokeh_box(model: Model) -> Box:
    """
    Creates a Nitro box from a Bokeh model.
    :param model: A Bokeh model (plots, widgets, etc.)
    :return: A box
    """
    # Render the box using our custom embed() function defined in the "bokeh" plugin.
    return box(mode='plugin:bokeh.embed', data=dict(model=json.dumps(json_item(model))))
