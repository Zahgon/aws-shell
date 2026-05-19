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
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys


class KeyManager(object):
    """A custom :class:`prompt_toolkit.KeyBindingManager`.

    Handles togging of:
        * Fuzzy or substring matching.
        * Vi or Emacs key bindings.
        * Multi or single columns in the autocompletion menu.
        * Showing or hiding the help pane.

    :type manager: :class:`prompt_toolkit.KeyBindingManager`
    :param manager: A custom `KeyBindingManager`.
    """

    def __init__(self, get_match_fuzzy, set_match_fuzzy,
                 get_enable_vi_bindings, set_enable_vi_bindings,
                 get_show_completion_columns, set_show_completion_columns,
                 get_show_help, set_show_help, stop_input_and_refresh_cli):
        self.manager = None
        self._create_key_manager(
            get_match_fuzzy, set_match_fuzzy,
            get_enable_vi_bindings, set_enable_vi_bindings,
            get_show_completion_columns, set_show_completion_columns,
            get_show_help, set_show_help, stop_input_and_refresh_cli)

    def _create_key_manager(self, get_match_fuzzy, set_match_fuzzy,
                            get_enable_vi_bindings, set_enable_vi_bindings,
                            get_show_completion_columns,
                            set_show_completion_columns,
                            get_show_help, set_show_help,
                            stop_input_and_refresh_cli):
        """Create and initialize the keybinding manager.

        :type get_fuzzy_match: callable
        :param get_fuzzy_match: Gets the fuzzy matching config.

        :type set_fuzzy_match: callable
        :param set_fuzzy_match: Sets the fuzzy matching config.

        :type get_enable_vi_bindings: callable
        :param get_enable_vi_bindings: Gets the vi (or emacs) key bindings
            config.

        :type set_enable_vi_bindings: callable
        :param set_enable_vi_bindings: Sets the vi (or emacs) key bindings
            config.

        :type get_show_completion_columns: callable
        :param get_show_completion_columns: Gets the show completions in
            multiple or single columns config.

        type set_show_completion_columns: callable
        :param set_show_completion_columns: Sets the show completions in
            multiple or single columns config.

        :type get_show_help: callable
        :param get_show_help: Gets the show help pane config.

        :type set_show_help: callable
        :param set_show_help: Sets the show help pane config.

        :type stop_input_and_refresh_cli: callable
        param stop_input_and_refresh_cli: Stops input by raising an
            `InputInterrupt`, forces a cli refresh to ensure certain
            options take effect within the current session.

        :rtype: :class:`prompt_toolkit.KeyBindingManager`
        :return: A custom `KeyBindingManager`.

        """
        pass
