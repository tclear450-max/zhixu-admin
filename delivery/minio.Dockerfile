FROM golang:1.24-alpine AS builder
ENV GOPROXY=https://goproxy.cn,direct CGO_ENABLED=0
WORKDIR /src
ADD vendor/minio-source.tar.gz /src/
RUN cd minio-* && go build -trimpath -ldflags="-s -w" -o /minio .
FROM python:3.13-alpine
COPY --from=builder /minio /usr/local/bin/minio
EXPOSE 9000 9001
ENTRYPOINT ["minio"]
