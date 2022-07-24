FROM bitnami/minideb:buster
# docker build -t ghcr.io/urlstechie/urlchecker .
WORKDIR /code
ENV PATH /opt/conda/bin:${PATH}
ENV LANG C.UTF-8
ENV SHELL /bin/bash
RUN apt-get update && \
    /bin/bash -c "install_packages wget bzip2 ca-certificates git unzip gnupg2 && \
    install_packages libglib2.0-dev libnss3 libfontconfig1 libgconf-2-4 && \
    install_packages libxcb-randr0-dev libxcb-xtest0-dev libxcb-xinerama0-dev libxcb-shape0-dev libxcb-xkb-dev && \
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    rm Miniconda3-latest-Linux-x86_64.sh && \
    conda create --name urlchecker && \
    conda clean --all -y"

# Google chrome binary
RUN /bin/bash -c 'wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get -y install google-chrome-stable'

COPY . /code
RUN /bin/bash -c "source activate urlchecker && \
    which python && \
    which pip && \
    pip install --upgrade certifi && \
    pip install git+https://github.com/danger89/fake-useragent.git && \
    pip install .[all]"
# Download chrome driver for selenium
RUN /bin/bash -c "wget https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip"
RUN echo "source activate urlchecker" > ~/.bashrc
ENV PATH /code:/opt/conda/envs/urlchecker/bin:${PATH}
ENTRYPOINT ["urlchecker"]
CMD ["check", "--help"]
