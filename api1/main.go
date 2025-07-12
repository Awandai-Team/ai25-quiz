package main

import (
    "fmt"
    "log"
    "net/http"
    "strings"
    "time"
)

// Dummy token for demonstration
const validToken = "mysecrettoken"


// Logging middleware
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        log.Printf("Started %s %s from %s", r.Method, r.URL.Path, r.RemoteAddr)
        next.ServeHTTP(w, r)
        duration := time.Since(start)
        log.Printf("Completed %s in %v", r.URL.Path, duration)
    })
}

// Authentication middleware
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        authHeader := r.Header.Get("Authorization")
        if !strings.HasPrefix(authHeader, "Bearer ") || strings.TrimPrefix(authHeader, "Bearer ") != validToken {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    })
}

// Handlers
func publicHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "This is a public endpoint: %s\n", r.URL.Path)
}

func privateHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "This is a protected endpoint: %s\n", r.URL.Path)
}

func logging(f http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        log.Println(r.URL.Path)
        f(w, r)
    }
}

func foo(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "foo")
    start := time.Now()
    log.Printf("Started %s %s from %s", r.Method, r.URL.Path, r.RemoteAddr)
    duration := time.Since(start)
    log.Printf("Completed %s in %v", r.URL.Path, duration)
}

func bar(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "bar")
    start := time.Now()
    log.Printf("Started %s %s from %s", r.Method, r.URL.Path, r.RemoteAddr)
    duration := time.Since(start)
    // Authentication
    // http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    //   authHeader := r.Header.Get("Authorization")
    //   if (!strings.HasPrefix(authHeader, "Bearer ") || strings.TrimPrefix(authHeader, "Bearer ") != validToken) {
    //       http.Error(w, "Unauthorized", http.StatusUnauthorized)
    //   }
    // }
    log.Printf("Completed %s in %v", r.URL.Path, duration)
}

func main() {
    http.HandleFunc("/v1/foo", logging(foo))
    http.HandleFunc("/v1/bar", logging(bar))


    fmt.Println("Server running on http://localhost:8001")
    fmt.Println("Hit Ctrl+C to kill the server")
    log.Fatal(http.ListenAndServe(":8001", nil))
}
