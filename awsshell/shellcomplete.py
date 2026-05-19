"""Autocompletion integration with python prompt toolkit.

This module integrates the low level autocomplete functionality
provided in awsshell.autocomplete and integrates it with the
interface required for autocompletion in the python prompt
toolkit.

If you're interested in the heavy lifting of the autocompletion
logic, see awsshell.autocomplete.

"""
import os
import logging

import botocore.session
from prompt_toolkit.completion import Completer, Completion

from awsshell import fuzzy


LOG = logging.getLogger(__name__)


class AWSShellCompleter(Completer):
    """Completer class for the aws-shell.

    This is the completer used specifically for the aws shell.
    Not to be confused with the AWSCLIModelCompleter, which is more
    low level, and can be reused in contexts other than the
    aws shell.
    """
    def __init__(self, completer, server_side_completer=None):
        self._completer = completer
        if server_side_completer is None:
            server_side_completer = self._create_server_side_completer()
        self._server_side_completer = server_side_completer


    def change_profile(self, profile_name):
        """Change the profile used for server side completions."""
        pass






