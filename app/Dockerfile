# reference: https://docs.docker.com/engine/reference/builder/#entrypoint
FROM python:3

RUN mkdir /home/app
WORKDIR /home/app
#COPY ./ /app
#RUN pip install -r requirements.txt
#EXPOSE 7001

ENTRYPOINT [ "/home/app/entrypoint.sh" ]
