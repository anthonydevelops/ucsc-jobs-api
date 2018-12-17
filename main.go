package main

import (
	"context"
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
	// Get DB config key
	uri, err := ioutil.ReadFile("keys.txt")
	if err != nil {
		fmt.Print(err)
	}
	key := string(uri)

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

	// Get JSON data from web scraper
	data, err := os.Open("./lib/data.json")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully opened data.json")

	defer data.Close()

	// Route handles & endpoints
	// r.HandleFunc("/jobs", getJobs).Methods("GET")
	// r.HandleFunc("/jobs/nonworkstudy", getNWSJobs).Methods("GET")
	// r.HandleFunc("/jobs/workstudy", getWSJobs).Methods("GET")
	// r.HandleFunc("/jobs/{id}", getJob).Methods("GET")

	// Start server
	log.Fatal(http.ListenAndServe(":8000", r))
}
