FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install django
RUN pip install requests
RUN pip install pandas
RUN pip install sklearn
EXPOSE 8080