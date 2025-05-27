FROM continuumio/miniconda3

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY environment.yml .

RUN conda config --add channels conda-forge && \
    conda env create -f environment.yml && \
    conda clean -afy

COPY . .

EXPOSE 5000

CMD ["/bin/bash", "-c", "source activate ielts && gunicorn --preload --bind 0.0.0.0:5000 --workers 8 wsgi:app --timeout 300"]