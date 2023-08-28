"""Module for Vortex class and helper functions"""
import requests
from requests import Response
import json


class Vortex:
    """An Vortex instance that is used for interacting with AWS IAM Services and Actions"""

    def __init__(self, aws_actions_map: dict[str, list[str]] = {}) -> None:
        if aws_actions_map:
            self._aws_actions_map: dict[str, list[str]] = aws_actions_map
        else:
            self._aws_actions_map: dict[str, list[str]] = _get_aws_actions_map()

    @property
    def aws_actions_map(self) -> dict[str, list[str]]:
        return self._aws_actions_map

    def get_aws_services(self) -> list[str]:
        return list(self._aws_actions_map.keys())

    def get_aws_actions(self) -> list[str]:
        return [
            f"{service}:{action}"
            for service in self._aws_actions_map.keys()
            for action in self._aws_actions_map.get(service)
        ]


def _get_aws_actions_map() -> dict[str, list[str]]:
    """
    Grabs javascript data from AWS Policy Generator and parses
    Returns a dictionary that maps AWS service name to its list of actions.
    """
    response: Response = requests.get(
        "https://awspolicygen.s3.amazonaws.com/js/policies.js"
    )

    # Strip the javascript variable to be left with json data
    stripped: str = (
        str(response.content).lstrip("b'app.PolicyEditorConfig=").rstrip("'")
    )
    data: dict = json.loads(stripped)

    return _parse_policygen_data(data)


def _parse_policygen_data(data: dict) -> list[str]:
    """
    Parses the JSON from AWS Policy Generator and returns the AWS Actions map
    """
    aws_actions_map: dict[str, list[str]] = {}
    for service in data["serviceMap"].values():
        for action in service["Actions"]:
            service_name = service["StringPrefix"]
            if aws_actions_map.get(service_name):
                aws_actions_map[service_name].append(action)
            else:
                aws_actions_map[service_name] = [action]

    return aws_actions_map
