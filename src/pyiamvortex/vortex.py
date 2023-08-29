"""Module for Vortex class and helper functions"""
import requests_cache
from requests import Response
import json
from datetime import timedelta


class Vortex:
    """An Vortex instance that is used for interacting with AWS IAM Services and Actions"""

    def __init__(self, aws_actions_map: dict[str, list[str]] = {}) -> None:
        if aws_actions_map:
            self._aws_actions_map: dict[str, list[str]] = aws_actions_map
        else:
            self._aws_actions_map: dict[str, list[str]] = _get_aws_actions_map()

        self.all_aws_actions: list[str] = self.get_aws_actions()

    @property
    def aws_actions_map(self) -> dict[str, list[str]]:
        return self._aws_actions_map

    def get_aws_services(self) -> list[str]:
        """Returns a sorted list of aws services (e.g. ec2, s3)"""
        return sorted(list(self._aws_actions_map.keys()))

    def get_aws_actions(self, aws_service: list[str] = None) -> list[str]:
        """Returns a list of sorted AWS actions (e.g. ec2:DescribeInstances, s3:GetObject)"""
        if aws_service and aws_service not in self._aws_actions_map.keys():
            raise ValueError(
                f"Invalid AWS Service: {aws_service}. Valid services are: {self.get_aws_services()}"
            )

        # Only return actions specified service if provided
        if aws_service:
            return sorted(
                [
                    f"{service}:{action}"
                    for service in self._aws_actions_map.keys()
                    if service == aws_service
                    for action in self._aws_actions_map.get(service)
                ]
            )
        # Return all actions otherwise
        return sorted(
            [
                f"{service}:{action}"
                for service in self._aws_actions_map.keys()
                for action in self._aws_actions_map.get(service)
            ]
        )

    def expand_aws_wildcard(self, aws_action: str) -> list[str]:
        """Returns a list of expanded AWS actions from an aws action with a wildcard (e.g. ec2:*, ec2:Describe*)"""
        if aws_action == "*":
            return self.all_aws_actions

        if aws_action.endswith("*"):
            return sorted(
                [
                    action
                    for action in self.all_aws_actions
                    if action.startswith(aws_action.rstrip("*"))
                ]
            )

        if aws_action in self.all_aws_actions:
            return [aws_action]

        # return none if no match
        return []


def _get_aws_actions_map() -> dict[str, list[str]]:
    """
    Grabs javascript data from AWS Policy Generator and parses
    Returns a dictionary that maps AWS service name to its list of actions.
    """
    # cache the reponse for policygen data
    session = requests_cache.CachedSession(
        "policygen_cache", use_cache_dir=True, expire_after=timedelta(days=1)
    )

    response: Response = session.get(
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
