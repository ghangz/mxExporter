# Copyright (c) 2025 by MetaX Integrated Circuits (Shanghai) Co., Ltd.

ARG ARCH=amd64
ARG BASEREG=registry.access.redhat.com
FROM --platform=linux/${ARCH} redhat:9-minimal AS builder

ARG ARCH=amd64
ARG BASEREG=registry.access.redhat.com
FROM --platform=linux/${ARCH} ${BASEREG}/ubi9/ubi-minimal:9.7

LABEL maintainer="Metax Developers <support-sw@metax-tech.com>"

RUN microdnf update -y && microdnf install -y \
    python3 \
    python3-pip && \
    microdnf clean all

RUN pip3 install --upgrade pip setuptools & pip3 install prometheus_client grpcio protobuf

COPY LICENSE /licenses/

ARG VERSION
LABEL name="MetaX Data Exporter" \
      vendor="MetaX" \
      version="${VERSION}" \
      release="N/A" \
      maintainer="container@metax-tech.com" \
      summary="The mx-exporter is a standalone app the exports MetaX GPU metrics to Prometheus server" \
      description="The mx-exporter support collecting metrics including GPU utilization, \
memory usage, temperature, power consumption, bandwidth, ECC, etc."

WORKDIR /opt/mxexporter/
COPY ["mx_exporter/*", "dep/*", "./mx_exporter/"]
ENTRYPOINT ["python3", "-u", "-m", "mx_exporter"]
