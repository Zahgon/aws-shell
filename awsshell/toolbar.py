# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from pygments.token import Token


class Toolbar(object):
    """Show information about the aws-shell in a tool bar.

    :type handler: callable
    :param handler: Wraps the callable `get_toolbar_items`.

    """

    def __init__(self, get_match_fuzzy, get_enable_vi_bindings,
                 get_show_completion_columns, get_show_help):
        self.handler = self._create_toolbar_handler(
            get_match_fuzzy, get_enable_vi_bindings,
            get_show_completion_columns, get_show_help)

    def _create_toolbar_handler(self, get_match_fuzzy, get_enable_vi_bindings,
                                get_show_completion_columns, get_show_help):
        """Create the toolbar handler.

        :type get_fuzzy_match: callable
        :param fuzzy_match: Gets the fuzzy matching config.

        :type get_enable_vi_bindings: callable
        :param get_enable_vi_bindings: Gets the vi (or emacs) key bindings
            config.

        :type get_show_completion_columns: callable
        :param get_show_completion_columns: Gets the show completions in
            multiple or single columns config.

        :type get_show_help: callable
        :param get_show_help: Gets the show help pane config.

        :rtype: callable
        :returns: get_toolbar_items.

        """
        pass
