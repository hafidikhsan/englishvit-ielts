FROM mmcauliffe/montreal-forced-aligner:latest

RUN pip install flask

COPY entrypoint.sh /entrypoint.sh
COPY app.py /app.py
# Copy all the files in the tf directory
COPY tf /tf

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
