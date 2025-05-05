FROM condaforge/miniforge3

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

RUN conda clean -afy
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

ENV CONDA_DEFAULT_ENV=myenv
ENV PATH="/opt/conda/envs/myenv/bin:$PATH"

CMD ["/bin/bash"]
