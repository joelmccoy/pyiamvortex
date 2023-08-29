from typer.testing import CliRunner

from pyiamvortex.cli import main

from unittest.mock import patch
import json

runner = CliRunner()


@patch("pyiamvortex.vortex.Vortex.get_aws_actions")
def test_get_aws_actions(mock_get_aws_actions):
    expected_aws_actions = ["s3:GetObject", "s3:PutObject"]
    mock_get_aws_actions.return_value = expected_aws_actions
    result = runner.invoke(main, ["get-aws-actions"])
    result_aws_actions = json.loads(result.stdout)
    assert result.exit_code == 0
    assert result_aws_actions == expected_aws_actions


@patch("pyiamvortex.vortex.Vortex.get_aws_services")
def test_get_aws_services(mock_get_aws_services):
    expected_aws_services = ["s3", "ec2"]
    mock_get_aws_services.return_value = expected_aws_services
    result = runner.invoke(main, ["get-aws-services"])
    result_aws_actions = json.loads(result.stdout)
    assert result.exit_code == 0
    assert result_aws_actions == expected_aws_services


@patch("pyiamvortex.vortex.Vortex.expand_aws_wildcard")
def test_expand_aws_wildcard(mock_expand_aws_wildcard):
    expected_expanded = ["s3:PutObject", "s3:PutObjectTagging"]
    mock_expand_aws_wildcard.return_value = expected_expanded
    result = runner.invoke(main, ["expand-aws-wildcard", "s3:Put*"])
    result_aws_actions = json.loads(result.stdout)
    assert result.exit_code == 0
    assert result_aws_actions == expected_expanded
