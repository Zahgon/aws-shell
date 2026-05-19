"""Module for building the autocompletion indices."""
from __future__ import print_function
import os
import json

from six import BytesIO
from docutils.core import publish_string
import awscli.clidriver
from awscli.argprocess import ParamShorthandDocGen
try:
    from botocore.docs.bcdoc import textwriter
except ImportError:
    from awscli.bcdoc import textwriter

from awsshell import determine_doc_index_filename
from awsshell.utils import remove_html
from awsshell import docs


SHORTHAND_DOC = ParamShorthandDocGen()


def new_index():
    return {'arguments': [], 'argument_metadata': {},
            'commands': [], 'children': {}}


def index_command(index_dict, help_command):
    arg_table = help_command.arg_table
    for arg in arg_table:
        arg_obj = arg_table[arg]
        metadata = {
            'required': arg_obj.required,
            'type_name': arg_obj.cli_type_name,
            'minidoc': '',
            'example': '',
            # The name used in the API call/botocore,
            # typically CamelCased.
            'api_name': getattr(arg_obj, '_serialized_name', '')
        }
        if arg_obj.documentation:
            metadata['minidoc'] = remove_html(
                arg_obj.documentation.split('\n')[0])
        if SHORTHAND_DOC.supports_shorthand(arg_obj.argument_model):
            service_name, op_name = help_command.event_class.rsplit('.', 1)
            example = SHORTHAND_DOC.generate_shorthand_example(
                cli_argument=arg_obj,
                service_id=service_name,
                operation_name=op_name,
            )
            metadata['example'] = example

        index_dict['arguments'].append('--%s' % arg)
        index_dict['argument_metadata']['--%s' % arg] = metadata
    for cmd in help_command.command_table:
        index_dict['commands'].append(cmd)
        # Each sub command will trigger a recurse.
        child = new_index()
        index_dict['children'][cmd] = child
        sub_command = help_command.command_table[cmd]
        sub_help_command = sub_command.create_help_command()
        index_command(child, sub_help_command)


def write_index(output_filename=None):
    driver = awscli.clidriver.create_clidriver()
    help_command = driver.create_help_command()
    index = {'aws': new_index()}
    current = index['aws']
    index_command(current, help_command)

    result = json.dumps(index)
    if not os.path.isdir(os.path.dirname(output_filename)):
        os.makedirs(os.path.dirname(output_filename))
    with open(output_filename, 'w') as f:
        f.write(result)










def convert_rst_to_basic_text(contents):
    """Convert restructured text to basic text output.

    This function removes most of the decorations added
    in restructured text.

    This function is used to generate documentation we
    can show to users in a cross platform manner.

    Basic indentation and list formatting are kept,
    but many RST features are removed (such as
    section underlines).

    """
    pass


class FileRenderer(object):

    def __init__(self):
        self._io = BytesIO()




class BasicTextWriter(textwriter.TextWriter):


class BasicTextTranslator(textwriter.TextTranslator):

    # The botocore TextWriter has additional formatting
    # for literals, for the aws-shell docs we don't want any
    # special processing so these nodes are noops.

    def visit_literal(self, node):
        pass

    def depart_literal(self, node):
        pass
