package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"github.com/mongodb/mongo-go-driver/mongo"
)

// Job struct (Model)
type Job struct {
	EmploymentDate string `json:"employmentdate"`
	FilingDate     string `json:"filingdate"`
	Hours          string `json:"hours"`
	Pay            string `json:"pay"`
	Schedule       string `json:"schedule"`
	SkillsPref     string `json:"skillspref"`
	SkillsRequired string `json:"skillsreq"`
	Title          string `json:"title"`
	Unit           string `json:"unit"`
}

func parseJSON() [][]Job {
	data, err := os.Open("./lib/data.json")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully opened data.json")

	defer data.Close()

	// Turn JSON into a Go array
	jsonValues, _ := ioutil.ReadAll(data)
	var jobs [][]Job

	json.Unmarshal(jsonValues, &jobs)

	// Iterate over Go jobs array
	return jobs
}

// Read JSON
var jobs = parseJSON()

func getJobs(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(jobs)
}

func main() {
	// Get DB config key
	uri, err := ioutil.ReadFile("keys.txt")
	if err != nil {
		fmt.Print(err)
	}
	key := string(uri)
	fmt.Println(key)

	// Connect to mongoDB
	client, err := mongo.Connect(context.TODO(), key)
	if err != nil {
		log.Fatal(err)
	}

	// Check the connection
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Connected to MongoDB!")

	// Initilize the router
	r := mux.NewRouter()

	// Route handles & endpoints
	r.HandleFunc("/jobs", getJobs).Methods("GET")
	// r.HandleFunc("/jobs/nonworkstudy", getNWSJobs).Methods("GET")
	// r.HandleFunc("/jobs/workstudy", getWSJobs).Methods("GET")
	// r.HandleFunc("/jobs/{id}", getJob).Methods("GET")

	// Start server
	log.Fatal(http.ListenAndServe(":8000", r))
}
