FROM python:3.13.0-alpine3.19

WORKDIR /opt/hostcontrol
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENV APP_ENV=production
ENV TERM=xterm-256color
ENV HOSTCTL_HOSTS_PATH="/opt/hosts"
ENV HOSTCTL_DB_PATH="/opt/host_control_db"

CMD ["python", "main.py"]