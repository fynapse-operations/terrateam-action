FROM ghcr.io/terrateamio/action-base:latest

COPY entrypoint.sh /entrypoint.sh
COPY entrypoint_gitlab.sh /entrypoint_gitlab.sh
COPY entrypoint_github.sh /entrypoint_github.sh
COPY terrat_runner /terrat_runner

COPY proxy/bin /usr/local/proxy/bin

ENV INFRACOST_VERSION v0.10.42
RUN ARCH=$(uname -m | sed 's/x86_64/amd64/g' | sed 's/aarch64/arm64/g') && \
    curl -fsSL -o /tmp/infracost-linux-${ARCH}.tar.gz "https://github.com/infracost/infracost/releases/download/${INFRACOST_VERSION}/infracost-linux-${ARCH}.tar.gz" && \
    tar -C /tmp -xzf /tmp/infracost-linux-${ARCH}.tar.gz && \
    mv /tmp/infracost-linux-${ARCH} /usr/local/bin/infracost && \
    rm -f /tmp/infracost-linux-${ARCH}.tar.gz


ENTRYPOINT ["/entrypoint.sh"]
