# https://takaishikawa42.hatenablog.com/entry/2020/05/16/101423

FROM python:3.7.7-buster as builder

# Install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.7.7-slim-buster as runner
COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Install linux packages
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 git

WORKDIR work
