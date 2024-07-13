FROM python:3.10

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD ['python3', '-m', 'emqx_deepstack_exhook']