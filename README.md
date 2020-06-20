# aws-ip-range-api

## Table of Contents
- [What does it do ?](https://github.com/groorj/aws-ip-range-api#what-does-it-do)
- [This project uses](https://github.com/groorj/aws-ip-range-api#this-project-uses)
- [Where does the information comes from](https://github.com/groorj/aws-ip-range-api#where-does-the-information-comes-from)
- [Get started](https://github.com/groorj/aws-ip-range-api#get-started)
- [How to use it](https://github.com/groorj/aws-ip-range-api#how-to-use-it)

## What does it do

Sometimes you need to validate the source IP address in your applications. If you are running your workloads on AWS, you might need to validate if:
- The IP address is an valid AWS IP
- What AWS region that IP address belongs to
- What is the service associated with the said IP address

If this is your use case, this project might help you.

It uses AWS API Gateway to provide you with an REST API to query an IP address. You can use this code to deploy your own API and integrate with your applications.

## This project uses

- The [Serverless Framework](https://www.serverless.com/)
- [AWS API Gateway](https://aws.amazon.com/api-gateway/)
- Python3
- Serverless plugins
  - serverless-python-requirements

## Where does the information comes from

AWS provides a list of IP ranges in a json format. You can find the file here:

[https://ip-ranges.amazonaws.com/ip-ranges.json](https://ip-ranges.amazonaws.com/ip-ranges.json)

An example of how the file looks like:

```json
    {
      "ip_prefix": "18.191.0.0/16",
      "region": "us-east-2",
      "service": "EC2",
      "network_border_group": "us-east-2"
    },
```

## Get started

- Install the Serveless Framework
- Install the serverless-python-requirements plugin

```bash
sls plugin install -n serverless-python-requirements
```

- Deploy the serverless architecture by running:

```bash
serverless --aws-profile <YOUR_PROFILE_NAME> deploy
```

Replace <YOUR_PROFILE_NAME> with your [AWS profile name](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html).

If the deployment is successful, you will see the API Gateway endpoints created:

```text
  GET - https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/health/check
  GET - https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/{ip}
  GET - https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/{ip}/region
  GET - https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/{ip}/service
```

## How to use it

### Get all avaliable information for a valid AWS IP address
```bash
curl https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/18.228.93.48
```

**Result:**
```json
{
  "data": {
    "ip_prefix": "18.228.0.0/16",
    "region": "sa-east-1",
    "service": "EC2",
    "network_border_group": "sa-east-1"
  }
}
```

### Get the region of a valid AWS IP address
```bash
curl -vvvv https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/52.1.1.1/region
```

**Result:**
```json
{
  "region": "us-east-1"
}
```

### Get the service associated with a valid AWS IP address
```bash
curl https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/3.17.184.157/service
```

**Result:**
```json
{
  "service": "EC2"
}
```

### Get all avaliable information for a non-AWS IP address
```bash
curl https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/127.0.0.1
```

**Result:**
```json
{
  "data": "unknown"
}
```

### Get the region of a non-AWS IP address
```bash
curl https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/127.0.0.1/region
```

**Result:**
```json
{
  "region": "unknown"
}
```

### Get the service associated with a non-AWS IP address
```bash
curl https://qe0fnc7qn7.execute-api.us-east-2.amazonaws.com/prod/127.0.0.1/service
```

**Result:**
```json
{
  "service": "unknown"
}

## Clean up

- Destroy the serverless architecture by running:

```bash
serverless --aws-profile <YOUR_PROFILE_NAME> remove
```

## Notes
Running this code will create AWS resources in your account that might not be included in the free tier.