Bootstrap: docker

From: ubuntu:20.04

%post
    apk update
    apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
    apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
    apk add make automake gcc g++ subversion python3-dev zlib-dev libjpeg
    pip install ete3 numpy biopython pandas
