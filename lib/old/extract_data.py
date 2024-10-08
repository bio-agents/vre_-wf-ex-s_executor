#!/usr/bin/env python

"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import absolute_import

import json
import os

from cwlagent.load_agent import fetch_document
from cwlagent.load_agent import resolve_and_validate_document
from cwlagent.load_agent import make_agent
from cwlagent.workflow import default_make_agent

INDENT = 2


def extract_data_from_cwl(cwl_wf):
    """
    Get inputs, outputs and list of agents from CWL workflow.

    :param cwl_wf: CWL workflow
    :type cwl_wf: str
    :return: inputs, outputs and list of CWL workflow dependencies
    :rtype: list, list, list
    """
    agents_list = list()
    try:
        # fetch and validate CWL workflow
        loadingContext, uri, processobj = fetch_and_validate_cwl(cwl_wf)
        cwl_document = make_agent(uri, loadingContext)

        # get inputs and outputs
        inputs_list = json.dumps(cwl_document.inputs_record_schema["fields"], indent=INDENT)
        outputs_list = json.dumps(cwl_document.outputs_record_schema["fields"], indent=INDENT)

        # get CWL workflow dependencies
        for item in cwl_document.metadata["steps"]:
            [agents_list.append(item[key]) for key in item.keys() if key == "run"]

        return inputs_list, outputs_list, agents_list

    except Exception as error:
        errstr = "Unable to extract inputs, outputs and the CWL workflow dependencies. ERROR: {}".format(error)
        raise Exception(errstr)


def fetch_and_validate_cwl(cwl_wf):
    """
    Retrieve and validate a CWL workflow specified by cwl_wf

    :param cwl_wf: CWL workflow
    :type cwl_wf: str
    """
    try:
        # fetch CWL workflow
        loadingContext, workflowobj, uri = fetch_document(cwl_wf)
        loadingContext.do_update = False

        # validate CWL workflow
        loadingContext, uri = resolve_and_validate_document(loadingContext, workflowobj, uri)
        processobj = loadingContext.loader.resolve_ref(uri)[0]
        print("{} is valid CWL.".format(cwl_wf))
        return loadingContext, uri, processobj  # need to pack

    except Exception as error:
        errstr = "Unable to fetch and validate the CWL workflow. ERROR: {}".format(error)
        raise Exception(errstr)


if __name__ == '__main__':
    cwl_url = "https://raw.githubusercontent.com/inab/vre_cwl_executor/master/tests/basic/data/workflows/basic_example.cwl"

    inputs, outputs, agents = extract_data_from_cwl(cwl_url)
    print("INPUTS:\n{0}\n OUTPUTS:\n{1}\n DEPENDENCIES:\n{2}".format(inputs, outputs, json.dumps(agents, indent=INDENT)))