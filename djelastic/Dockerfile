FROM python:3.9-slim

# set work directory
WORKDIR /usr/src/djelastic

RUN pip install --upgrade pip

ENV LIBRARY_PATH=/lib:/usr/lib

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# copy project
COPY . .

# install dependencies
RUN pip install -r requirements.txt


RUN sed -i 's/\r$//g' /usr/src/djelastic/entrypoint.sh
RUN chmod +x /usr/src/djelastic/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/djelastic/entrypoint.sh"]