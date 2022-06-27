# YOLOv5 🚀 by Ultralytics, GPL-3.0 license

# Start FROM Nvidia PyTorch image https://ngc.nvidia.com/catalog/containers/nvidia:pytorch
FROM t12nakatani/petal-maml

# Install linux packages
RUN apt update && apt install -y zip htop screen libgl1-mesa-glx gcc

# Install python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt
