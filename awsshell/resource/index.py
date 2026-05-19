"""Index and retrive information from the resource JSON.

The classes are organized as follows:

* ResourceIndexBuilder - Takes a boto3 resource and converts into the
  index format we need to do server side completions.
* CompleterDescriber - Takes the index from ResourceIndexBuilder and looks
  up how to perform the autocompletion.  Note that this class does
  *not* actually do the autocompletion.  It merely tells you how
  you _would_ do the autocompletion if you made the appropriate
  service calls.
* ServerSideCompleter - The thing that does the actual autocompletion.
  You tell it the command/operation/param you're on, and it will
  return a list of completions for you.

"""
import os
import logging
from collections import namedtuple

import jmespath
from botocore import xform_name
from botocore.exceptions import BotoCoreError

LOG = logging.getLogger(__name__)

# service - The name of the AWS service
# operation - The name of the AWS operation
# params - A dict of params to send in the request (not implemented yet)
# path - A JMESPath expression to select the expected elements.
ServerCompletion = namedtuple('ServerCompletion',
                              ['service', 'operation', 'params', 'path'])


def extract_field_from_jmespath(expression):
    result = jmespath.compile(expression)
    current = result.parsed
    while current['children']:
        current = current['children'][0]
    if current['type'] == 'field':
        return current['value']


class ResourceIndexBuilder(object):
    def __init__(self):
        pass

    def build_index(self, resource_data):
        # First we need to go through the 'resources'
        # key and map all of its actions back to the
        # resource name.
        index = {
            'operations': {},
            'resources': {},
        }
        service = resource_data['service']
        if 'hasMany' in service:
            for model in service['hasMany'].values():
                resource_name = model['resource']['type']
                for identifier in model['resource']['identifiers']:
                    first_identifier = model['resource']['identifiers'][0]
                    index['resources'][resource_name] = {
                        'operation': model['request']['operation'],
                        # TODO: map all the identifiers.
                        # We're only taking the first one for now.
                        'resourceIdentifier': {
                            first_identifier['target']: first_identifier['path']
                        }
                    }
        for resource_name, model in resource_data['resources'].items():
            if resource_name not in index['resources']:
                continue
            if 'actions' in model:
                resource_actions = model['actions']
                for action_model in resource_actions.values():
                    op_name = action_model['request']['operation']
                    current = {}
                    index['operations'][op_name] = current
                    for param in action_model['request']['params']:
                        if param['source'] == 'identifier':
                            field_name = extract_field_from_jmespath(
                                param['target'])
                            current[field_name] = {
                                'resourceName': resource_name,
                                'resourceIdentifier': param['name'],
                            }
        return index


class CompleterDescriber(object):
    """Describes how to autocomplete a resource.

    You give this class a service/operation/param and it will
    describe to you how you can autocomplete values for the
    provided parameter.

    It's up to the caller to actually take that description
    and make the appropriate service calls + filtering to
    extract out the server side values.

    """
    def __init__(self, resource_index):
        self._index = resource_index

    def describe_autocomplete(self, service, operation, param):
        """Describe operation and args needed for server side completion.

        :type service: str
        :param service: The AWS service name.

        :type operation: str
        :param operation: The AWS operation name.

        :type param: str
        :param param: The name of the parameter being completed.  This must
            match the casing in the service model (e.g. InstanceIds, not
            --instance-ids).

        :rtype: ServerCompletion
        :return: A ServerCompletion object that describes what API call to make
            in order to complete the response.

        """
        pass


class CachedClientCreator(object):
    def __init__(self, session):
        #: A botocore.session.Session object.  Only the
        #: create_client() method is used.
        self._session = session
        self._client_cache = {}



class CompleterDescriberCreator(object):
    """Create and cache CompleterDescriber objects."""
    def __init__(self, loader):
        #: A botocore.loader.Loader
        self._loader = loader
        self._describer_cache = {}
        self._services_with_completions = None

    def create_completer_query(self, service_name):
        """Create a CompleterDescriber for a service.

        :type service_name: str
        :param service_name: The name of the service, e.g. 'ec2'

        :return: A CompleterDescriber object.

        """
        pass




class ServerSideCompleter(object):
    def __init__(self, client_creator, describer_creator):
        self._client_creator = client_creator
        self._describer_creator = describer_creator

    def retrieve_candidate_values(self, service, operation, param):
        """Retrieve server side completions.

        :type service: str
        :param service: The service name, e.g. 'ec2', 'iam'.

        :type operation: str
        :param operation: The operation name, in the casing
            used by the CLI (words separated by hyphens), e.g.
            'describe-instances', 'delete-user'.

        :type param: str
        :param param: The param name, as specified in the service
            model, e.g. 'InstanceIds', 'UserName'.

        :rtype: list
        :return: A list of possible completions for the
            service/operation/param combination.  If no
            completions were found an empty list is returned.

        """
        pass


def main():
    # Generate the latest autocompletion indices from
    # boto3.  You'll need to do this if you pull in
    # a new boto3 version that has updated resource models.
    import sys
    import json
    import os
    import boto3.session
    data_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data')
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    session = boto3.session.Session()
    loader = session._loader
    builder = ResourceIndexBuilder()
    for resource_name in session.get_available_resources():
        api_version = loader.determine_latest_version(
            resource_name, 'resources-1')
        model = loader.load_service_model(resource_name, 'resources-1',
                                          api_version)
        index = builder.build_index(model)
        output_file = os.path.join(data_dir, resource_name, api_version,
                                   'completions-1.json')
        if not os.path.isdir(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        with open(output_file, 'w') as f:
            f.write(json.dumps(index, indent=2))


if __name__ == '__main__':
    main()
