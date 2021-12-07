ARG BASE_IMAGE=senzing/senzing-base:1.6.3
FROM ${BASE_IMAGE}

ENV REFRESHED_AT=2021-12-05

LABEL Name="senzing/accountant-aws-marketplace" \
      Maintainer="support@senzing.com" \
      Version="1.0.2"

HEALTHCHECK CMD ["/app/accountant-aws-marketplace.py"]

# Run as "root" for system installation.

USER root

# Install packages via PIP.

RUN pip3 install \
      boto3

# Copy files from repository.

COPY ./rootfs /
COPY ./accountant-aws-marketplace.py /app/

# Make non-root container.

USER 1001

# Runtime execution.

WORKDIR /app
CMD ["/app/sleep-infinity.sh"]
