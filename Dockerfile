FROM python:3.10

VOLUME /config.yaml

COPY . .

RUN python3 setup.py install

CMD ['emqx_deepstack_exhook', '/config.yaml']