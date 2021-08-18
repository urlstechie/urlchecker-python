FROM bitnami/minideb:buster
# docker build -t urlschecker .
WORKDIR /code
ENV PATH /opt/conda/bin:${PATH}
ENV LANG C.UTF-8
ENV SHELL /bin/bash
RUN apt-get update && \
    /bin/bash -c "install_packages wget bzip2 ca-certificates git && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    conda create --name urlchecker && \
    conda clean --all -y"
COPY . /code
RUN /bin/bash -c "source activate urlchecker && \
    which python && \
    which pip && \
    pip install --upgrade certifi && \
    pip install ."
RUN echo "source activate urlchecker" > ~/.bashrc
ENV PATH /opt/conda/envs/urlchecker/bin:${PATH}
ENTRYPOINT ["urlchecker"]
CMD ["check", "--help"]
