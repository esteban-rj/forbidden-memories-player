# Use Python 3.12 slim image as base
FROM python:3.12-slim

WORKDIR /card-finder-mcp

# Install minimal OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen

COPY . ./

CMD ["uv", "run", "python", "main.py"] 