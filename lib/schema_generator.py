#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2020-2021 Barcelona Supercomputing Center (BSC), Spain
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

from model import *


def setOwner(author, institution, contact, url):
    """

    :param author:
    :param institution:
    :param contact:
    :param url:
    :return:
    """
    return Owner(author, institution, contact, url)


def setCloud(launcher, workflow_type, minimum_v_ms, initial_v_ms, default_cloud):
    """

    :param launcher:
    :param workflow_type:
    :param minimum_v_ms:
    :param initial_v_ms:
    :param default_cloud:
    :return:
    """
    return Cloud(launcher, workflow_type, minimum_v_ms, initial_v_ms, default_cloud)


def setInfrastructure(memory, cpus, executable, cloud):
    """

    :param memory:
    :param cpus:
    :param executable:
    :param cloud:
    :return:
    """
    clouds = Clouds(cloud)
    return Infrastructure(memory, cpus, executable, clouds)


def is_required(param):
    """

    :param param:
    :return:
    """
    if "?" in param:
        return False
    else:
        return True


def is_multiple(param):
    """

    :param param:
    :return:
    """
    if "File" in param:
        return False
    else:
        return True


def setInputs(inputs):
    """

    :param inputs:
    :return:
    """
    input_files, arguments = [], []
    for input in inputs:
        if input['type'].find("File") != -1:  # create new InputFile
            new_file = InputFile(
                name=input['id'],
                description="",  # TODO inp['doc']
                help=None,
                file_type=[],
                data_type=[],
                required=is_required(input['type']),
                allow_multiple=is_multiple(input['type'])
            )
            input_files.append(new_file)

        else:  # create new Argument
            new_argument = Argument(
                name=input['id'],
                description="",  # TODO inp['doc']
                help=None,
                type=input['type'],
                default=None
            )
            arguments.append(new_argument)

    return input_files, arguments


def setAgent(owner, keywords, infrastructure, input_files, arguments):  # TODO
    """

    :param owner:
    :param keywords:
    :param infrastructure:
    :param input_files:
    :param arguments:
    :return:
    """
    return Agent(
        id="my_agent_id",
        name="My Agent",
        title="My Agent Complete Name",
        short_description="This is a one or two lines description of what 'My Agent' does.",
        long_description="This is a longer description of what 'My Agent' does. It includes information about the software use for it, the supported inputs, the expected results, etc.",
        url="https://github.com/.../MyAgent",
        publication="https://dx.doi.org/xx.xxxx/xxxx/xxxxxx",
        owner=owner,
        keywords=keywords,
        keywords_agent=keywords,
        status=0,
        infrastructure=infrastructure,
        input_files=input_files,
        input_files_public_dir=[],
        input_files_combinations=[],
        arguments=arguments,
        has_custom_viewer=False,
        output_files=[]
    )
