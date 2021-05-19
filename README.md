# accountant-aws-marketplace

## Synopsis

The `accountant-aws-marketplace` is an exploration of how to work with
[AWS Marketplace Metering Service integration](https://docs.aws.amazon.com/marketplace/latest/userguide/entitlement-and-metering-for-paid-products.html).

This repository is purposefully independent of Senzing.
That is, it is not used in Senzing deployments outside of the
[AWS Marketplace](https://docs.aws.amazon.com/marketplace/latest/userguide/what-is-marketplace.html).

## Overview

The exploration looks at:

1. Using the python
   [boto3](https://aws.amazon.com/sdk-for-python/)
   library for AWS MarketPlace
   [meter_usage()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering.Client.meter_usage) invocations in
   [accountant-aws-marketplace.py](accountant-aws-marketplace.py).
1. Using Docker's
   [HEALTHCHECK](https://docs.docker.com/engine/reference/builder/#healthcheck)
   as a method of periodic polling which does not require injecting AWS-specific code
   into the the primary code running in the Docker container in
   [Dockerfile](Dockerfile).
1. Using docker-compose's [healthcheck](https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck)
   in
   [docker-compose.yaml](docker-compose.yaml).
1. Using AWS Cloudformation template's
   [HealthCheck](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-taskdefinition-containerdefinitions.html#cfn-ecs-taskdefinition-containerdefinition-healthcheck)
   in
   [cloudformation.yaml](cloudformation.yaml).

### Contents

1. [Preamble](#preamble)
    1. [Legend](#legend)
1. [Related artifacts](#related-artifacts)
1. [Expectations](#expectations)
1. [Demonstrate using Command Line Interface](#demonstrate-using-command-line-interface)
    1. [Prerequisites for CLI](#prerequisites-for-cli)
    1. [Download](#download)
    1. [Environment variables for CLI](#environment-variables-for-cli)
    1. [Run command](#run-command)
1. [Develop](#develop)
    1. [Prerequisites for development](#prerequisites-for-development)
    1. [Clone repository](#clone-repository)
    1. [Build Docker image](#build-docker-image)
    1. [Test with docker-compose](#test-with-docker-compose)
    1. [Test with AWS Cloudformation](#test-with-aws-cloudformation)
1. [Advanced](#advanced)
    1. [Configuration](#configuration)
1. [Errors](#errors)
1. [References](#references)

## Preamble

At [Senzing](http://senzing.com),
we strive to create GitHub documentation in a
"[don't make me think](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/dont-make-me-think.md)" style.
For the most part, instructions are copy and paste.
Whenever thinking is needed, it's marked with a "thinking" icon :thinking:.
Whenever customization is needed, it's marked with a "pencil" icon :pencil2:.
If the instructions are not clear, please let us know by opening a new
[Documentation issue](https://github.com/Senzing/template-python/issues/new?template=documentation_request.md)
describing where we can improve.   Now on with the show...

### Legend

1. :thinking: - A "thinker" icon means that a little extra thinking may be required.
   Perhaps there are some choices to be made.
   Perhaps it's an optional step.
1. :pencil2: - A "pencil" icon means that the instructions may need modification before performing.
1. :warning: - A "warning" icon means that something tricky is happening, so pay attention.

## Related artifacts

1. [DockerHub](https://hub.docker.com/r/senzing/accountant-aws-marketplace)

## Expectations

- **Time:** Budget 40 minutes to get the demonstration up-and-running, depending on CPU and network speeds.
- **Background knowledge:** This repository assumes a working knowledge of:
  - [Docker](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/docker.md)
  - [docker-compose](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/docker-compose.md)
  - [AWS Cloudformation](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/aws-cloudformation.md)
  - [AWS Marketplace](https://github.com/Senzing/knowledge-base/blob/master/WHATIS/aws-marketplace.md)

## Demonstrate using Command Line Interface

### Prerequisites for CLI

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. Install Python dependencies:
    1. See [requirements.txt](requirements.txt) for list
        1. [Installation hints](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-python-dependencies.md)

### Download

1. Get a local copy of
   [accountant-aws-marketplace.py](accountant-aws-marketplace.py).
   Example:

    1. :pencil2: Specify where to download file.
       Example:

        ```console
        export SENZING_DOWNLOAD_FILE=~/accountant-aws-marketplace.py
        ```

    1. Download file.
       Example:

        ```console
        curl -X GET \
          --output ${SENZING_DOWNLOAD_FILE} \
          https://raw.githubusercontent.com/Senzing/accountant-aws-marketplace/master/accountant-aws-marketplace.py
        ```

    1. Make file executable.
       Example:

        ```console
        chmod +x ${SENZING_DOWNLOAD_FILE}
        ```

1. :thinking: **Alternative:** The entire git repository can be downloaded by following instructions at
   [Clone repository](#clone-repository)

### Environment variables for CLI

1. `accountant-aws-marketplace.py` uses the AWS
   [boto3](https://aws.amazon.com/sdk-for-python/)
   python library.
   [Configure](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
   your environment with
   [AWS configure credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials).

### Run command

1. Run the command.
   Example:

   ```console
   ${SENZING_DOWNLOAD_FILE}
   ```

## Develop

The following instructions are used when modifying and building the Docker image.

### Prerequisites for development

:thinking: The following tasks need to be complete before proceeding.
These are "one-time tasks" which may already have been completed.

1. The following software programs need to be installed:
    1. [git](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-git.md)
    1. [make](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-make.md)
    1. [docker](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/install-docker.md)

### Clone repository

For more information on environment variables,
see [Environment Variables](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md).

1. Set these environment variable values:

    ```console
    export GIT_ACCOUNT=senzing
    export GIT_REPOSITORY=accountant-aws-marketplace
    export GIT_ACCOUNT_DIR=~/${GIT_ACCOUNT}.git
    export GIT_REPOSITORY_DIR="${GIT_ACCOUNT_DIR}/${GIT_REPOSITORY}"
    ```

1. Using the environment variables values just set, follow steps in [clone-repository](https://github.com/Senzing/knowledge-base/blob/master/HOWTO/clone-repository.md) to install the Git repository.

### Build Docker image

1. **Option #1:** Using `docker` command and GitHub.

    ```console
    sudo docker build \
      --tag senzing/accountant-aws-marketplace \
      https://github.com/senzing/accountant-aws-marketplace.git
    ```

1. **Option #2:** Using `docker` command and local repository.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo docker build --tag senzing/accountant-aws-marketplace .
    ```

1. **Option #3:** Using `make` command.

    ```console
    cd ${GIT_REPOSITORY_DIR}
    sudo make docker-build
    ```

    Note: `sudo make docker-build-development-cache` can be used to create cached Docker layers.

### Test with docker-compose

1. :pencil2: Set Environment variables.
   For more options, see [Environment variables for CLI](#environment-variables-for-cli).
   Example:

    ```console
    export AWS_ACCESS_KEY_ID=AAAAAAAAAAAAAAAAAAAA
    export AWS_DEFAULT_REGION=us-east-1
    export AWS_SECRET_ACCESS_KEY=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    export AWS_SESSION_TOKEN=xxxxxxxxxxxxxxxx...
    ```

1. Run `docker-compose`.
   Example:

    ```console
    cd ${GIT_REPOSITORY_DIR}
    docker-compose up
    ```

### Test with AWS Cloudformation

1. Visit [AWS Cloudformation console](https://console.aws.amazon.com/cloudformation/home)
1. "Create stack" > "With new resources (standard)"
1. Select :radio_button: Upload a template file
1. Click "Choose file" button
1. Select [cloudformation.yaml](cloudformation.yaml)
1. Click "Next" button and continue to deploy

## Advanced

### Configuration

Configuration values specified by environment variable or command line parameter.

- **[AWS_ACCESS_KEY_ID](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#aws_access_key_id)**
- **[AWS_DEFAULT_REGION](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#aws_default_region)**
- **[AWS_SECRET_ACCESS_KEY](https://github.com/Senzing/knowledge-base/blob/master/lists/environment-variables.md#aws_secret_access_key)**

## Errors

1. See [docs/errors.md](docs/errors.md).

## References
