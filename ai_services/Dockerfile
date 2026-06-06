FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip \
    libgl1-mesa-glx libglib2.0-0 curl && \
    rm -rf /var/lib/apt/lists/* && \
    ln -sf /usr/bin/python3.11 /usr/bin/python && \
    python -m pip install --upgrade pip

WORKDIR /app

COPY ai_services/requirements.txt .                                                                                                                    
RUN python -m pip install --no-cache-dir -r requirements.txt   

COPY ai_services/ ./ai_services/                                                                                                                                             

EXPOSE 8001

HEALTHCHECK --interval=60s --timeout=15s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

    CMD ["python", "-m", "uvicorn", "ai_services.main:app", "--host", "0.0.0.0", "--port", "8001"]
