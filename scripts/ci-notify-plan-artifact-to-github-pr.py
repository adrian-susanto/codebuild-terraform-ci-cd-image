#!/usr/bin/env python
# Notify Plan Artifact to Github Pull Request

import os
import sys

from jinja2 import Environment, FileSystemLoader

import notify_github as gh

if not os.path.isfile('artifact/terraform.tfplan'):
    print("artifact/terraform.tfplan not found. Skipping this step")
    sys.exit(0)

command = os.popen('terraform show artifact/terraform.tfplan -no-color')
tf_plan = command.read()
command.close()

f = open("artifact/metadata.json", "r")
metadata = f.read()

template = Environment(
    loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__)) + "/templates")
).get_template("terraform_output.j2")
message = template.render(
    metadata_json=metadata,
    file_name="terraform.tfplan",
    terraform_output=tf_plan
)

gh.send_pr_comment(payload=message)
