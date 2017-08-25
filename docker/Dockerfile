FROM tensorflow/tensorflow
MAINTAINER Johny.Zheng <shun.johny@gmail.com>

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents
# kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# Clusters tab is now provided by IPython parallel
RUN pip install ipyparallel

RUN ipcluster nbextension enable

# Set localtime
COPY ./release/docker/localtime /etc/localtime

EXPOSE 8888
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
