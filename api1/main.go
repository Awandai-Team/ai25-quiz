package main

import (
    "fmt"
    "io"
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

func callAPI2(w http.ResponseWriter, r *http.Request) {
    start := time.Now()
    log.Printf("Started %s %s from %s", r.Method, r.URL.Path, r.RemoteAddr)
    log.Printf("API1: Making request to API2")
    
    // Make GET request to API2
    resp, err := http.Get("http://api2:8000/items/42?delay=1")
    if err != nil {
        log.Printf("Error calling API2: %v", err)
        http.Error(w, "Error calling API2", http.StatusInternalServerError)
        return
    }
    defer resp.Body.Close()
    
    // Read response body
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        log.Printf("Error reading API2 response: %v", err)
        http.Error(w, "Error reading API2 response", http.StatusInternalServerError)
        return
    }
    
    // Return combined response
    w.Header().Set("Content-Type", "application/json")
    fmt.Fprintf(w, `{
        "api1_message": "Hello from API1 (Go)",
        "api2_response": %s,
        "timestamp": "%s"
    }`, string(body), time.Now().Format(time.RFC3339))
    
    log.Printf("API1: Successfully called API2 and returned response")
    duration := time.Since(start)
    log.Printf("Completed %s in %v", r.URL.Path, duration)
}

func main() {
    http.HandleFunc("/v1/foo", logging(foo))
    http.HandleFunc("/v1/bar", logging(bar))

    // This endpoint calls API2 and returns combined result from API1 and API2 
    http.HandleFunc("/v1/call-api2", logging(callAPI2))

    fmt.Println("Server running on http://localhost:8001")
    fmt.Println("Hit Ctrl+C to kill the server")
    log.Fatal(http.ListenAndServe(":8001", nil))
}
