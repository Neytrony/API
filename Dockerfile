# pull official base image
#FROM python:3.9.6-alpine
FROM python:3.9

# copy project
#COPY . .

# set work directory
RUN mkdir -p /usr/src/app && mkdir -p /usr/src/app/mediafiles && mkdir -p /usr/src/app/mediafiles/logs/


#WORKDIR /Users/User/Documents/Project/TelegramsBot/evcmo_pay_bot/telebot
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt update \
    && apt install -y \
    gcc \
    #postgresql-dev \
    python3-dev
    
    # libcogl-pango-dev \
    # libcairo2-dev \
    # libtool \
    # linux-headers-amd64 \
    # musl-dev \
    # libffi-dev \
    # libssl-dev \
    # libjpeg-dev \
    # zlib1g-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]





# ====

# # pull official base image
# FROM python:3.9

# # copy project
# #COPY . .

# # set work directory
# RUN mkdir -p /usr/src/app &&  mkdir -p /usr/src/app/download &&  mkdir -p /usr/src/app/logs && mkdir -p /usr/src/app/files


# #WORKDIR /Users/User/Documents/Project/TelegramsBot/evcmo_pay_bot/telebot
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # copy project
# COPY . /usr/src/app

# # running migrations
# #RUN python manage.py migrate
 