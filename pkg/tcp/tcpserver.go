package tcp

import (
	"fmt"
	"net"
)

func StartTcpServer(ip string, port uint, queueSize int, onConnection func(net.Conn)) error {
	ln, err := net.Listen("tcp", fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		return err
	}
	
	for i := 0; i < queueSize; i++ {
		conn, _ := ln.Accept()
		onConnection(conn)
	}

	return nil
}

func StartTcpGoroutineServer(ip string, port uint, queueSize int, onConnection func(net.Conn)) error {
	ln, err := net.Listen("tcp", fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		return err
	}
	
	for i := 0; i < queueSize; i++ {
		conn, _ := ln.Accept()
		go onConnection(conn)
	}

	return nil
}