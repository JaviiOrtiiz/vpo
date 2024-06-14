#!/bin/bash
docker run -d -v /vpo:/app --restart always --name vpo --privileged vpo
