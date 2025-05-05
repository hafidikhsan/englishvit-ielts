FROM mmcauliffe/montreal-forced-aligner:latest

RUN pip install flask

COPY entrypoint.sh /entrypoint.sh
COPY app.py /app.py

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
