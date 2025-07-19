FROM golang:1.16-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download
RUN echo "Dependencies cached."

COPY . .

RUN go build -o /api1-server .

FROM alpine:latest

COPY --from=builder /api1-server /api1-server

EXPOSE 8001
CMD ["/api1-server"]
