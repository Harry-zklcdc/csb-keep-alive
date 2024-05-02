FROM ubuntu:22.04

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends wget python3 python3-pip curl jq && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    pip3 install -r /app/requirements.txt

RUN bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install && \
    bash -c "$(curl -L wgcf-cli.vercel.app)" && \
    wgcf-cli -r && \
    wgcf-cli -g xray

RUN TEMPLATE=$(jq -Rs . wgcf.json.xray.json | sed 's/^"//' | sed 's/"$//') && \
    sed -i "s|{{TEMPLATE}}|${TEMPLATE}|g" config.json

ENV HTTPS_PROXY=http://127.0.0.1:10808