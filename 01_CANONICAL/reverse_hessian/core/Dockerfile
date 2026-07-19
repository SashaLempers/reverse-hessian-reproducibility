FROM python:3.13.5-slim
WORKDIR /work
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONHASHSEED=0
CMD ["./reproduce_all.sh"]
