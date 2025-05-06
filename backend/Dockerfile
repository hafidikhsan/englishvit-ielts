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

SHELL ["conda", "run", "-n", "ielts", "/bin/bash", "-c"]

RUN mfa model download dictionary english_us_arpa
RUN mfa model download acoustic english_us_arpa

RUN python3 -m spacy download en_core_web_sm

COPY . .

EXPOSE 5000

CMD ["/bin/bash", "-c", "conda run -n ielts gunicorn --bind 0.0.0.0:5000 wsgi:app --timeout 120"]