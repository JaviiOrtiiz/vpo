#!/bin/bash
docker run -d -v /home/pablo/vpo:/app --restart always --name vpo --privileged vpo
