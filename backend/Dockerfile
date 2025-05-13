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

RUN /bin/bash -c "source activate ielts && \
    python -m nltk.downloader punkt && \
    python -m nltk.downloader punkt_tab && \
    python -m nltk.downloader stopwords && \
    python -m nltk.downloader averaged_perceptron_tagger_eng && \
    mfa model download acoustic english_us_arpa && \
    mfa model download dictionary english_us_arpa && \
    python3 -m spacy download en_core_web_sm"

COPY . .

EXPOSE 5000

CMD ["/bin/bash", "-c", "source activate ielts && gunicorn --bind 0.0.0.0:5000 --preload --workers 2 --threads 2 wsgi:app --timeout 300"]