FROM python:3.7

RUN apt-get update \
	&& apt-get install -y antiword abiword unrtf poppler-utils libjpeg-dev tesseract-ocr

# pstotext: Remove from install because it is in unstable distribution

WORKDIR /root/src

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
