FROM python:3

ADD . /e-auction-django/

WORKDIR /e-auction-django/

COPY requirements.txt /e-auction-django

RUN pip3 install -r requirements.txt

COPY . /e-auction-django

WORKDIR /e-auction-django/

CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:8000", "commerce.wsgi:application"]