FROM nvidia/cuda:11.6.2-base-ubuntu20.04
# ------------------------------------------------------------------
# Close noninteractive
ENV DEBIAN_FRONTEND noninteractive
# ------------------------------------------------------------------
USER root
WORKDIR /workspace
# ------------------------------------------------------------------
# Install requirements.sh & entrypoint.sh
COPY ./docker /workspace/docker
RUN chmod u+x /workspace/docker/install.sh \
                && /workspace/docker/install.sh