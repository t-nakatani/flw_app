FROM python:3.7

# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx gcc git

# Install python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt
WORKDIR work
