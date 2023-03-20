FROM python:3.11.1-slim

# Create app directory
WORKDIR /app

# Install G++ Compiler
RUN apt-get update
RUN apt-get install -y g++
RUN apt-get install -y build-essential

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]