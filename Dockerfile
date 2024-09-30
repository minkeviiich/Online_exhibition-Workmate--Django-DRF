FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

WORKDIR /code/workmate

CMD ["/bin/bash", "/code/entrypoint.sh"]