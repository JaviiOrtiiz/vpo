#!/bin/bash
docker run -d -v "$HOME/vpo":/app --restart always --name vpo --privileged vpo
