# Vast.ai dashboard — zero-dependency image (~55 MB)
FROM python:3.12-alpine

LABEL org.opencontainers.image.title="vast-dashboard" \
      org.opencontainers.image.description="Vast.ai telemetry + instance control dashboard" \
      org.opencontainers.image.source="https://github.com/3p4e/3p4e"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VAST_DASH_HOST=0.0.0.0 \
    VAST_DASH_PORT=8090

WORKDIR /app

# no pip installs: the server uses the standard library only
COPY server.py index.html ./

# unprivileged user
RUN addgroup -S dash && adduser -S -G dash -h /app dash \
    && chown -R dash:dash /app
USER dash

EXPOSE 8090

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8090/healthz', timeout=4).status==200 else 1)"

ENTRYPOINT ["python", "server.py"]
