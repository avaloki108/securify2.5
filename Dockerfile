FROM ubuntu:24.04
ARG SOLC=0.5.12

# install basic packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    locales \
    wget \
    curl \
    build-essential \
    graphviz \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# set correct locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# install souffle 2.5
RUN wget https://github.com/souffle-lang/souffle/releases/download/2.5/x86_64-ubuntu-2404-souffle-2.5-Linux.deb -O /tmp/souffle.deb && \
    apt-get update && apt-get install -y /tmp/souffle.deb && \
    rm -rf /var/lib/apt/lists/* /tmp/souffle.deb

# install the required solc version
RUN curl -L https://github.com/ethereum/solidity/releases/download/v$SOLC/solc-static-linux > /usr/bin/solc-$SOLC && \
    chmod +x /usr/bin/solc-$SOLC && \
    ln -s /usr/bin/solc-$SOLC /usr/local/bin/solc

COPY requirements.txt /requirements.txt

WORKDIR /sec

# copy and compile securify
COPY . /sec
ENV PYTHONPATH /sec

# install securify requirements
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r /requirements.txt && \
    python3 -m pip install --no-cache-dir .

RUN cd /sec/securify/staticanalysis/libfunctors/ && ./compile_functors.sh

RUN cd /sec/securify/staticanalysis/souffle_analysis && \
        souffle --dl-program=../dl-program \
        --fact-dir=/sec/securify/staticanalysis/facts_in \
        --output-dir=/sec/securify/staticanalysis/facts_out \
        -L../libfunctors -w analysis.dl


ENV LD_LIBRARY_PATH /sec/securify/staticanalysis/libfunctors

# Check that everything works and create a cache of the available patterns
# Should be removed
RUN cd /sec/securify/ && securify staticanalysis/testContract.sol

ENTRYPOINT ["python3", "securify/__main__.py"]
