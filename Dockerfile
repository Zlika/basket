FROM debian:12.1-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-selenium chromium-driver && \
    rm -rf /var/lib/apt/lists/*
COPY import_matchs.py .
ENTRYPOINT ["python3", "import_matchs.py"]
CMD ["id_fbi", "password_fbi", "id_kali", "password_kali"]
