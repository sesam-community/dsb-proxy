FROM python:3-alpine

WORKDIR /opt/service
COPY ./requirements.txt /opt/service/
RUN pip install -r requirements.txt

COPY ./service.py /opt/service/

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["service.py"]