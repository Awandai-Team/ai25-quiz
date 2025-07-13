# Build Stage
FROM golang:1.16-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Final Image
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .
CMD ["./myapp"]