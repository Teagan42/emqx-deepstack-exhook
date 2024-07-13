FROM python:3.10

VOLUME /config.yaml

COPY . .

RUN pip3 install .

CMD ["emqx_deepstack_exhook", "/config.yaml"]
