FROM python:3.10.11

WORKDIR /root/Exon

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

EXPOSE 3000

CMD ["bash", "start"]
