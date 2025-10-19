FROM ubuntu:20.04
RUN apt-get update && apt-get install -y curl
COPY hello.txt /app/
WORKDIR /app
CMD ["cat", "hello.txt"]