#
FROM python:3.11

# 
WORKDIR /app

COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
EXPOSE 8000
