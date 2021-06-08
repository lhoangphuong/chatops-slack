FROM debian:latest

WORKDIR /usr/src/app

# Install python3
RUN apt-get update && apt-get install -y \
python3 python3-pip && \
pip3 install --upgrade pip && \
pip3 install howdoi && \
# Install docker
apt update -y && \
apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y && \
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
apt update && \
apt-cache policy docker-ce && \
apt install docker-ce -y && \
service docker start && \
rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./chatbot.py" ]