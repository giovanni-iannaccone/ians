package portScanner

import (
	"ascii"
	"console"
	"jsonUtils"
	"pool"

	"fmt"
	"net"
	"os"
	"runtime"
	"strings"
	"sync"
	"time"
)

var activePorts []string
var iterableLength uint = 0
var loopIndex uint = 0
var mu sync.Mutex

type submitFunction func(pool *pool.ThreadPool, data *map[string]string, wg *sync.WaitGroup, addr string)

type scanTask struct {
	addr string
	port string
	wg   *sync.WaitGroup
}

func (s *scanTask) Execute() error {
	defer s.wg.Done()

	var host string = fmt.Sprintf("%s:%s", s.addr, s.port)
	conn, err := net.DialTimeout("tcp", host, time.Duration(1)*time.Second)
	if err == nil {
		mu.Lock()
		activePorts = append(activePorts, s.port)
		mu.Unlock()
		conn.Close()
	}

	mu.Lock()
	loopIndex++
	mu.Unlock()

	return err
}

func (s *scanTask) OnFailure(err error) {

}

func displayProgress() {
	const barMaxWidth uint = 38

	for {
		var barWidth uint = barMaxWidth * loopIndex / iterableLength
		var bar string = strings.Repeat("▉", int(barWidth)) + strings.Repeat("-", int(barMaxWidth - barWidth))
		var progress string = fmt.Sprintf("%.1f", float32(loopIndex) / float32(iterableLength) * 100)

		console.Print(console.BoldBlue, "[%s] %s\r", bar, progress)

		if progress == "100.0" {
			return
		}
	}
}

func printPorts(data *map[string]string) {
	var service string

	for _, port := range activePorts {
		service = (*data)[port]
		console.Println(console.BoldGreen, "%s:\t%s" + console.Reset, port, service)
	}
}

func run(data *map[string]string, submitTasks submitFunction, addr string) error {
	wg := &sync.WaitGroup{}
	wg.Add(int(iterableLength))
	
	pool, err := pool.NewSimplePool(runtime.NumCPU(), 0)
	if err != nil {
		return err
	}

	pool.Start()
	defer pool.Stop()

	go displayProgress()
	submitTasks(&pool, data, wg, addr)

	wg.Wait()
	return nil
}

func submitTasksOnCompleteScan(pool *pool.ThreadPool, _ *map[string]string, wg *sync.WaitGroup, addr string) {
	for i := uint(1); i <= iterableLength; i++ {
		(*pool).AddWork(&scanTask{
			addr: addr,
			port: fmt.Sprintf("%d", i),
			wg:   wg,
		})
	}
}

func submitTasksOnPartialScan(pool *pool.ThreadPool, data *map[string]string, wg *sync.WaitGroup, addr string) {
	for port := range *data {
		(*pool).AddWork(&scanTask{
			addr: addr,
			port: port,
			wg:   wg,
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
		console.Error("Error acquiring IP address: %s", err)
		os.Exit(1)
	}
	addr := addrs[0].String()

	err = jsonUtils.ExtractData("utils/common_ports.json", &jsonData)
	if err != nil {
		console.Error("Error reading JSON data: %s", err)
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

	console.Println(console.Red, "\nScanner is ready, press ENTER to start...")
	fmt.Scanln()

	err = run(&jsonData, submitter, addr)
	if err != nil {
		console.Error("Error during scan: %s", err)
	}

	console.Println(console.Reset, "\n")
	printPorts(&jsonData)
	fmt.Scanln()
}
