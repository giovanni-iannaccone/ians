package chat

import (
	"fmt"
	"net"
	"reflect"
	
	"github.com/giovanni-iannaccone/ians/pkg/console"
)

func connect(ip string, port uint, needPasswd *bool) (net.Conn, error) {
	passwd := make([]byte, 4)
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		return nil, err
	}

	n, err := conn.Read(passwd)
	if err != nil {
		conn.Close()
		return nil, err
	}

	if reflect.DeepEqual(passwd[:n], PASSWORD_SET) {
		*needPasswd = true
		return conn, nil
	}

	return conn, nil
}

func receive(server net.Conn) {
	var msg = make([]byte, 1024)

	for {
		if n, err := server.Read(msg); err == nil && n > 0 {
			fmt.Printf("\r%s\n> ", msg[:n])
		}
	}
}

func sendAndReceive(server net.Conn) error {
	var message string
	go receive(server)

	for {
		fmt.Printf("> ")
		console.Scan(&message)
		server.Write([]byte(message))
	}
}

func startClient(ip *string, port uint, nickname *string) {
	var needPasswd bool = false
	server, err := connect(*ip, port, &needPasswd)

	if err != nil {
		console.Fatal(err.Error())
	
	} else if needPasswd {
		var buffer []byte
		var passwd string

		console.Print(console.BoldBlue, "[+] " + console.Reset + "Password: ")
		fmt.Scanf("%s", &passwd)

		server.Write([]byte(passwd))
		server.Read(buffer)
		console.Println(console.Reset, "%s", string(buffer))

		for reflect.DeepEqual(buffer, WRONG_PASSWORD) {
			console.Print(console.BoldBlue, "[+] " + console.Reset + "Password: ")
			fmt.Scanf("%s", &passwd)

			server.Write([]byte(passwd))
			server.Read(buffer)
		}
	}

	server.Write([]byte(*nickname))
	sendAndReceive(server)
}
