# Base image with Miniconda and Debian
FROM continuumio/miniconda3

# Set working directory
WORKDIR /app

# Copy environment.yml and application files
COPY environment.yml .
COPY . .

# Create conda environment from environment.yml
RUN conda config --add channels conda-forge && \
    conda env create -f environment.yml && \
    conda clean -afy

# Activate conda environment and ensure it's available in the shell
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Expose the port Flask will run on
EXPOSE 5000

# Run the app
CMD ["conda", "run", "-n", "myenv", "python", "app.py"]
