# pyiamvortex
A python utility library used for getting all available AWS IAM actions and performing different operations on them.

## Summary
There is no available API to list out all of the available AWS IAM actions. This library uses the AWS Policy Generator to get all of the available actions and then parses them into a usable format.

Creating a `Vortex` is an operating environment where you initalize the backend of available AWS IAM actions in which you can perform different operations within this context.  The default backend is the AWS Policy Generator, but you can also create a `Vortex` with a custom backend.

This tool is useful for building AWS Least Privilege IAM policies.

## Install

```bash
pip install pyiamvortex
```

## Usage

### CLI

```bash
pyiamvortex get-aws-services # prints all available AWS services (i.e. ec2, s3, iam, etc.)
pyiamvortex get-aws-actions # prints all available AWS actions (i.e. ec2:DescribeInstances, s3:GetObject, etc.)
```

```bash
pyiamvortex get-aws-actions sts # prints all available AWS actions for the sts service
>>
[
    "sts:AssumeRole",
    "sts:AssumeRoleWithSAML",
    "sts:AssumeRoleWithWebIdentity",
    "sts:DecodeAuthorizationMessage",
    "sts:GetAccessKeyInfo",
    "sts:GetCallerIdentity",
    "sts:GetFederationToken",
    "sts:GetServiceBearerToken",
    "sts:GetSessionToken",
    "sts:SetSourceIdentity",
    "sts:TagSession"
]
```

```bash
pyiamvortex expand-aws-wildcard 'sts:AssumeRole*' # expands the wildcard to all available AWS actions that matches the pattern
>>
[
    "sts:AssumeRole",
    "sts:AssumeRoleWithSAML",
    "sts:AssumeRoleWithWebIdentity"
]
```

### Python Library

```python
from pyiamvortex import Vortex

vortex = Vortex() # initializes a vortex object with the default AWS actions map from AWS Policy Generator
print(vortex.get_aws_services()) # prints all available AWS services (i.e. ec2, s3, iam, etc.)
print(vortex.get_aws_actions()) # prints all available AWS actions (i.e. ec2:DescribeInstances, s3:GetObject, etc.)
print(vortex.get_aws_actions("s3")) # prints all available AWS actions for the s3 service (i.e. s3:GetObject, s3:PutObject, etc.)
```