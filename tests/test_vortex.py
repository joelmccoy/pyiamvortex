from pyiamvortex.vortex import Vortex, _get_aws_actions_map
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture(scope="module")
def dummy_aws_actions_map() -> dict[str, list[str]]:
    return {
        "ec2": ["DescribeInstances", "RunInstances"],
        "s3": ["GetObject", "PutObject"],
        "iam": ["CreateUser"],
    }


@patch("pyiamvortex.vortex._get_aws_actions_map")
def test_init_with_aws_actions_map(mock_get_aws_actions_map: dict[str, list[str]]):
    dummy_aws_actions_map = {
        "ec2": ["DescribeInstances", "RunInstances"],
    }
    mock_get_aws_actions_map.return_value = dummy_aws_actions_map
    vortex = Vortex()
    assert vortex.aws_actions_map == dummy_aws_actions_map


def test_get_aws_services(dummy_aws_actions_map: dict[str, list[str]]):
    vortex = Vortex(dummy_aws_actions_map)
    expected_services = ["ec2", "iam", "s3"]
    assert vortex.get_aws_services() == expected_services


def test_get_aws_actions(dummy_aws_actions_map: dict[str, list[str]]):
    vortex = Vortex(dummy_aws_actions_map)
    expected_actions = [
        "ec2:DescribeInstances",
        "ec2:RunInstances",
        "iam:CreateUser",
        "s3:GetObject",
        "s3:PutObject",
    ]
    assert vortex.get_aws_actions() == expected_actions


def test_get_aws_actions_filter_by_service(dummy_aws_actions_map: dict[str, list[str]]):
    vortex = Vortex(dummy_aws_actions_map)
    expected_actions = ["ec2:DescribeInstances", "ec2:RunInstances"]
    assert vortex.get_aws_actions(aws_service="ec2") == expected_actions


def test_get_aws_actions_invalid_service(dummy_aws_actions_map: dict[str, list[str]]):
    vortex = Vortex(dummy_aws_actions_map)
    with pytest.raises(ValueError) as e:
        assert vortex.get_aws_actions(aws_service="ABC")
        assert (
            str(e.value)
            == "Invalid AWS Service: ABC. Valid services are: ['ec2', 'iam', 's3']"
        )


def test_expand_aws_wildcard_wildcard():
    aws_actions_map = {
        "ec2": ["DescribeInstances", "DescribeVpcAttribute", "RunInstances"],
    }
    vortex = Vortex(aws_actions_map)
    assert vortex.expand_aws_wildcard("*") == [
        "ec2:DescribeInstances",
        "ec2:DescribeVpcAttribute",
        "ec2:RunInstances",
    ]
    assert vortex.expand_aws_wildcard("ec2:*") == [
        "ec2:DescribeInstances",
        "ec2:DescribeVpcAttribute",
        "ec2:RunInstances",
    ]
    assert vortex.expand_aws_wildcard("ec2:Describe*") == [
        "ec2:DescribeInstances",
        "ec2:DescribeVpcAttribute",
    ]
    assert vortex.expand_aws_wildcard("ec2:De*") == [
        "ec2:DescribeInstances",
        "ec2:DescribeVpcAttribute",
    ]


def test_expand_aws_wildcard_exact_match():
    aws_actions_map = {
        "ec2": ["DescribeInstances", "DescribeVpcAttribute", "RunInstances"],
    }
    vortex = Vortex(aws_actions_map)
    assert vortex.expand_aws_wildcard("ec2:DescribeInstances") == [
        "ec2:DescribeInstances"
    ]


def test_expand_aws_wildcard_no_match():
    aws_actions_map = {
        "ec2": ["DescribeInstances", "DescribeVpcAttribute", "RunInstances"],
    }
    vortex = Vortex(aws_actions_map)
    assert vortex.expand_aws_wildcard("ec2:DescribeInstancesSILLY") == []


@patch("pyiamvortex.vortex.requests_cache.CachedSession.get")
def test_get_aws_actions_map(mock_requests_get: str):
    mock_response = MagicMock()
    mock_requests_get.return_value = mock_response
    mock_response.content = 'b\'app.PolicyEditorConfig={"serviceMap":\
        {"Amazon EC2":{"StringPrefix":"ec2","Actions":\
        ["DescribeInstances","RunInstances"]}}}\''
    assert _get_aws_actions_map() == {
        "ec2": ["DescribeInstances", "RunInstances"],
    }
