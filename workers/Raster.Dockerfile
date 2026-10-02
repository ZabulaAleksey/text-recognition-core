FROM python@sha256:88310c082760d93ac7c74d579e95e53a4ab6ea52dd8901abc61a103daf488ac4
COPY raster_requirements.txt /opt/trc/raster_requirements.txt
COPY pillow-12.3.0-cp313-cp313-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl /opt/trc/wheels/
RUN python -I -m pip install --no-index --no-deps --require-hashes --no-compile --disable-pip-version-check --find-links=/opt/trc/wheels -r /opt/trc/raster_requirements.txt && rm -rf /opt/trc/wheels
COPY raster_worker.py /opt/trc/raster_worker.py
COPY license-notices/ /opt/trc/license-notices/
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /opt/trc
USER 65532:65532
ENTRYPOINT ["python", "-I", "-B", "/opt/trc/raster_worker.py"]
CMD []
