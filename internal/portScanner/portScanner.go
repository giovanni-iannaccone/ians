package portScanner

import (
	"fmt"
	"net"
	"sync"
	"time"

	"github.com/giovanni-iannaccone/ians/pkg/ascii"
	"github.com/giovanni-iannaccone/ians/pkg/console"
	"github.com/giovanni-iannaccone/ians/pkg/jsonUtils"
	"github.com/giovanni-iannaccone/ians/pkg/progressbar"
)

var activePorts []string
var iterableLength uint = 0
var mu sync.Mutex

type submitFunction func(ch chan bool, data *map[string]string, addr string)

func printPorts(data *map[string]string) {
	var service string

	for _, port := range activePorts {
		service = (*data)[port]
		console.Println(console.BoldGreen, "%s:\t%s", port, service)
	}

	console.Println(console.Reset, "")
}

func run(data *map[string]string, submitTasks submitFunction, addr string) error {	
	ch := make(chan bool)
	go submitTasks(ch, data, addr)
	progressbar.DisplayProgressBar(iterableLength, ch)

	return nil
}

func scanPort(ch chan bool, addr string, port string) error {
	defer func() {
		ch <- true
	}()
	
	var host string = fmt.Sprintf("%s:%s", addr, port)
	conn, err := net.DialTimeout("tcp", host, time.Duration(5) * time.Second)
	if err == nil {
		mu.Lock()
		activePorts = append(activePorts, port)
		mu.Unlock()
		conn.Close()
	}

	return err
}

func submitTasksOnCompleteScan(ch chan bool, 
	_ *map[string]string, addr string,
) {
	for i := uint(1); i <= iterableLength; i++ {
		go scanPort(
			ch,
			addr,
			fmt.Sprintf("%d", i),
		)
	}
}

func submitTasksOnPartialScan(ch chan bool,
	data *map[string]string, addr string,
) {
	for port := range *data {
		go scanPort(
			ch,
			addr,
			port,
		)
	}
}

func Initialize() {
	var jsonData map[string]string
	var target string
	var option uint = 0
	var submitter submitFunction

	ascii.PortScanner()
	console.Println(console.BoldRed, "\n     A multithreaded port scanner\n")

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Type the target: ")
	fmt.Scanf("%s", &target)

	addrs, err := net.LookupIP(target)
	if err != nil {
		console.Fatal("Error acquiring IP address: %s", err.Error())
	}
	addr := addrs[0].String()

	err = jsonUtils.ExtractData("utils/common_ports.json", &jsonData)
	if err != nil {
		console.Error("Error reading JSON data: %s", err.Error())
	}

	console.Println(console.Reset, "IP address for %s acquired: %s", target, addr)

	for option != 1 && option != 2 {
		console.Println(console.BoldBlue, "\n[1] " + console.Reset + "For a base scan")
		console.Print(console.BoldBlue, "[2] " + console.Reset + "For a complete scan\n\n> ")
		fmt.Scanf("%d", &option)
	}

	if option == 1 {
		iterableLength = uint(len(jsonData))
		submitter = submitTasksOnPartialScan
	} else {
		iterableLength = 65535
		submitter = submitTasksOnCompleteScan
	}

	console.Println(console.Red, "\n%d ports will be scanned", iterableLength)
	console.Println(console.Red, "Scanner is ready, press ENTER to start...")
	fmt.Scanln()

	err = run(&jsonData, submitter, addr)
	if err != nil {
		console.Error(err.Error())
	}

	console.Println(console.Reset, "\n")
	printPorts(&jsonData)
	fmt.Scanln()
}
