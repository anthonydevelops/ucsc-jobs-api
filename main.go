package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

// Job struct (Model)
type Job struct {
	DateApproved   string `json:"dateapproved"`
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

func storeJSON() [][]Job {
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
var jobs = storeJSON()

// Get all jobs
func getJobs(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(jobs)
}

// Get non-workstudy jobs
func getNWSJobs(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(jobs[0])
}

// Get workstudy jobs
func getWSJobs(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(jobs[1])
}

// Get job filtered by title
func getJob(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	for i := 0; i < len(jobs); i++ {
		for j := 0; j < len(jobs[i]); j++ {
			if jobs[i][j].Title == params["title"] {
				json.NewEncoder(w).Encode(jobs[i][j])
				return
			}
		}

	}
	json.NewEncoder(w).Encode(&Job{})
}

func main() {
	// Initilize the router
	r := mux.NewRouter()

	// Route handles & endpoints
	r.HandleFunc("/jobs", getJobs).Methods("GET")
	r.HandleFunc("/jobs/nonworkstudy", getNWSJobs).Methods("GET")
	r.HandleFunc("/jobs/workstudy", getWSJobs).Methods("GET")
	r.HandleFunc("/jobs/{title}", getJob).Methods("GET")

	// Start server
	log.Fatal(http.ListenAndServe(":8000", r))
}
