package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/rs/cors"
)

func setupGlobalLogger() {
	if err := os.MkdirAll("logs", 0755); err != nil {
		log.Fatalf("error creating log directory: %v", err)
	}

	logFile, err := os.OpenFile("logs/api1.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening log file: %v", err)
	}

	multiWriter := io.MultiWriter(os.Stdout, logFile)
	log.SetOutput(multiWriter)
	log.Println("Logger initialized for API 1 (Go)")
}

func logsHandler(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		getLogs(w, r)
	case http.MethodDelete:
		clearLogs(w, r)
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func getLogs(w http.ResponseWriter, r *http.Request) {
	log.Println("API 1: Log file requested.")
	logFilePath := "logs/api1.log"

	fileBytes, err := os.ReadFile(logFilePath)
	if err != nil {
		log.Printf("Error reading log file: %v", err)
		http.Error(w, "Could not read log file.", http.StatusInternalServerError)
		return
	}

	lines := strings.Split(strings.TrimSpace(string(fileBytes)), "\n")
	start := 0
	if len(lines) > 50 {
		start = len(lines) - 50
	}

	if len(lines) == 1 && lines[0] == "" {
		lines = []string{}
	}

	response := map[string][]string{
		"logs": lines[start:],
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func clearLogs(w http.ResponseWriter, r *http.Request) {
	log.Println("API 1: Clear log file requested.")
	logFilePath := "logs/api1.log"

	if err := os.Truncate(logFilePath, 0); err != nil {
		log.Printf("Error clearing log file: %v", err)
		http.Error(w, "Could not clear log file.", http.StatusInternalServerError)
		return
	}

	log.Println("API 1: Log file cleared successfully.")
	w.WriteHeader(http.StatusNoContent)
}

func callAPI2Handler(w http.ResponseWriter, r *http.Request) {
	log.Println("API 1: Received request to call API 2.")

	api2URL := os.Getenv("API2_URL")
	if api2URL == "" {
		api2URL = "http://api2:8002"
	}
	requestURL := api2URL + "/v1/data"

	log.Printf("API 1: Calling API 2 at %s", requestURL)
	resp, err := http.Get(requestURL)
	if err != nil {
		log.Printf("API 1: Error calling API 2: %v", err)
		http.Error(w, "Failed to communicate with API 2", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Printf("API 1: Error reading response from API 2: %v", err)
		http.Error(w, "Error reading response from API 2", http.StatusInternalServerError)
		return
	}

	log.Printf("API 1: Received successful response from API 2.")

	var dataFromAPI2 interface{}
	json.Unmarshal(body, &dataFromAPI2)

	finalResponse := map[string]interface{}{
		"message":              "Successfully called API 2 from Go",
		"response_from_api2": dataFromAPI2,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(finalResponse)
}

func main() {
	setupGlobalLogger()

	mux := http.NewServeMux()
	mux.HandleFunc("/v1/call-api2", callAPI2Handler)
	mux.HandleFunc("/logs", logsHandler)

	c := cors.New(cors.Options{
		AllowedOrigins: []string{"*"},
		AllowedMethods: []string{"GET", "POST", "DELETE", "OPTIONS"},
		AllowedHeaders: []string{"*"},
	})

	handler := c.Handler(mux)

	log.Println("API 1 (Go) starting on port 8001")
	if err := http.ListenAndServe(":8001", handler); err != nil {
		log.Fatalf("could not start server: %v", err)
	}
}
