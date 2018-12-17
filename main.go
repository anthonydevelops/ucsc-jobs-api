package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

// Job struct (Model)
type Job struct {
	ID             string `json:"id"`
	Title          string `json:"title"`
	Unit           string `json:"unit"`
	Pay            int    `json:"pay"`
	FilingDate     string `json:"filingdate"`
	EmploymentDate string `json:"employmentdate"`
	Hours          int    `json:"hours"`
	Schedule       string `json:"schedule"`
	SkillsRequired string `json:"skillsrequired"`
	SkillsPref     string `json:"skillspref"`
}

func main() {
	// Init router
	r := mux.NewRouter()

	// Get JSON data from web scraper

	// Route handles & endpoints
	r.HandleFunc("/jobs", getJobs).Methods("GET")
	r.HandleFunc("/jobs/nonworkstudy", getNWSJobs).Methods("GET")
	r.HandleFunc("/jobs/workstudy", getWSJobs).Methods("GET")
	r.HandleFunc("/jobs/{id}", getJob).Methods("GET")

	// Start server
	log.Fatal(http.ListenAndServe(":8000", r))
}
