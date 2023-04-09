FROM ubuntu:20.04

RUN apt update && \
    apt install -y libxml2-dev libxslt-dev libffi-dev gcc musl-dev gcc libssl-dev curl && \
    apt install -y make automake gcc g++ subversion python3-dev zlib1g-dev libjpeg-dev && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    python3 -m pip install ete3 numpy biopython pandas six && \
    apt install -y bash

ENV PATH=/usr/local/bin:$PATH
ENV LC_ALL=C

CMD ["/bin/bash"]