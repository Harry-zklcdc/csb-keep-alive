FROM ubuntu:22.04

run apt-get update && apt-get install -y wget python3 python3-pip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    pip3 install -r requirements.txt