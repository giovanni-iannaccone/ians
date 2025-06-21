package portScanner

import (
	"ascii"
	"console"
	"jsonUtils"
	"pool"
	"progressbar"

	"fmt"
	"net"
	"runtime"
	"sync"
	"time"
)

var activePorts []string
var iterableLength uint = 0
var mu sync.Mutex

type submitFunction func(pool *pool.ThreadPool, data *map[string]string, addr string, ch chan(bool))

type scanTask struct {
	addr	string
	ch   	chan bool
	port 	string
}

func (s *scanTask) Execute() error {
	var host string = fmt.Sprintf("%s:%s", s.addr, s.port)
	conn, err := net.DialTimeout("tcp", host, time.Duration(5) * time.Second)
	if err == nil {
		mu.Lock()
		activePorts = append(activePorts, s.port)
		mu.Unlock()
		conn.Close()
	}

	s.ch <- true
	return err
}

func (s *scanTask) OnFailure(err error) {

}

func printPorts(data *map[string]string) {
	var service string

	for _, port := range activePorts {
		service = (*data)[port]
		console.Println(console.BoldGreen, "%s:\t%s", port, service)
	}

	console.Println(console.Reset, "")
}

func run(data *map[string]string, submitTasks submitFunction, addr string) error {	
	pool, err := pool.NewSimplePool(runtime.NumCPU(), 0)
	if err != nil {
		return err
	}

	pool.Start()
	defer pool.Stop()

	ch := make(chan bool)
	go submitTasks(&pool, data, addr, ch)
	progressbar.DisplayProgressBar(iterableLength, ch)

	return nil
}

func submitTasksOnCompleteScan(pool *pool.ThreadPool, _ *map[string]string, 
	addr string, ch chan bool,
) {
	for i := uint(1); i <= iterableLength; i++ {
		(*pool).AddWork(&scanTask{
			addr: addr,
			ch: ch,
			port: fmt.Sprintf("%d", i),
		})
	}
}

func submitTasksOnPartialScan(pool *pool.ThreadPool, data *map[string]string, 
	addr string, ch chan bool,
) {
	for port := range *data {
		(*pool).AddWork(&scanTask{
			addr: addr,
			ch: ch,
			port: port,
		})
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
