FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 VENV=/opt/venv
WORKDIR /app
RUN python -m venv $VENV
ENV PATH="/opt/venv/bin:$PATH"
COPY open/requirements.txt open/requirements-dev.txt /app/
RUN /opt/venv/bin/python -m pip install --no-cache-dir -r /app/requirements.txt -r /app/requirements-dev.txt
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app /opt/venv
USER appuser
COPY --chown=appuser:appuser open /app/open
EXPOSE 8000
CMD ["/opt/venv/bin/uvicorn","open.api.main:app","--host","0.0.0.0","--port","8000"]
