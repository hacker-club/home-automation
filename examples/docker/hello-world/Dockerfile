# This Dockerfile is based on an existing debian image.
FROM debian:stable-slim

# We can customize the environment in which our containerized program
# will run. One way to do that is to install the required packages:
# our programs will run.
RUN apt-get update &&\
    apt-get install -y cowsay

# This is the command that will be executed when we run the container
# defined by this Dockerfile.
# Here, we simply call the cowsay program that we installed with the
# apt-get command above.
CMD ["/usr/games/cowsay", "hello, hackerclub.io (from Docker)"]