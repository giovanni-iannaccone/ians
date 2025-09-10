package chat

import (
	"bufio"
	"fmt"
	"os"
	"net"
	"strings"
	
	"github.com/giovanni-iannaccone/ians/pkg/console"
)

var PASSWORD_SET = []byte("1")
var PASSWORD_NOT_SET = []byte("0")

var BLOCKED_MESSAGE = []byte("You are blocked and can't enter this room")
var REMOVED_MESSAGE = []byte("You have been removed from this room")

var CORRECT_PASSWORD = []byte("Welcome")
var WRONG_PASSWORD = []byte("Wrong password")

type User struct {
	addr 	 	string
	conn 		net.Conn
	nickname 	string
}

var blockedUsers []string
var users []*User

func addUserToList(conn *net.Conn, nickname *string) {
	user := User{
		addr: (*conn).RemoteAddr().String(),
		conn: *conn,
		nickname: *nickname,
	}
	
	users = append(users, &user)
}

func block(nickname *string) {
	for i, user := range users {
		if *nickname == (*user).nickname {
			(*user).conn.Close()
			blockedUsers = append(blockedUsers, (*user).addr)
			users = append(users[:i], users[i + 1:]...)
			break
		}
	}
}

func broadcast(from string, msg []byte) {
	msg = []byte(fmt.Sprintf("%s: %s", from, string(msg)))

	for i, client := range users {
        _, err := (*client).conn.Write(msg)
        if err != nil {
            (*client).conn.Close()
            users = append(users[:i], users[i+1:]...)
        }
    }
}

func getNickname(conn *net.Conn, nickname *string) {
	var buffer = make([]byte, 1024)
	n, _ := (*conn).Read(buffer)
	*nickname = string(buffer[:n])
}

func getPassword(conn *net.Conn, password *string) {
	var passwd = make([]byte, 1024)
	(*conn).Read(passwd)
	for string(passwd) != *password {
		(*conn).Write([]byte(WRONG_PASSWORD))
		(*conn).Read(passwd)
	}

	(*conn).Write([]byte(CORRECT_PASSWORD))
}

func handleConnection(conn net.Conn, password *string) {
	if isBlocked(conn.RemoteAddr().String()) {
		conn.Write(BLOCKED_MESSAGE)
		conn.Close()
		return
	}

	if *password != "" {
		conn.Write([]byte(PASSWORD_SET))
		getPassword(&conn, password)
	} else {
		conn.Write([]byte(PASSWORD_NOT_SET))
	}

	var nickname string
	getNickname(&conn, &nickname)

	addUserToList(&conn, &nickname)

	console.Print(console.BoldGreen, "\r%s entered the chat\n" + console.Reset + ">", nickname)

	msg := make([]byte, 1024)
	for {
		if n, err := conn.Read(msg); err == nil && n > 0 {
			broadcast(nickname, msg[:n])
		}
	}
}

func isBlocked(user string) bool {
	for _, blocked := range blockedUsers {
		if blocked == user {
			return true
		}
	}

	return false
}

func parseCmd(cmd *string) {
    command := strings.Fields(*cmd)

    switch command[0] {
    case "help":
        printMenu()

    case "block":
        if len(command) > 1 {
            block(&command[1])
        }

    case "clear":
        console.Clear()

    case "exit":
        os.Exit(0)

    case "info":
        if len(command) > 1 {
            printInfo(&command[1])
        }

    case "ls":
        printAllUsers()

    case "remove":
        if len(command) > 1 {
            remove(&command[1])
        }
    }
}

func printAllUsers() {
	for _, user := range users {
		console.Println(console.Green, "%s", (*user).nickname)
	}
}

func printInfo(nickname *string) {
	for _, user := range users {
		if (*user).nickname == *nickname {
			console.Println(console.Green, "%s -> %s", user.nickname, user.addr)
		}
	}
}

func printMenu() {
	console.Println(console.BoldBlue, "[+] " + console.Reset + "Servers's host has special 'powers', type:")
    console.Println(console.BoldBlue, "-block 'nickname'" + console.Reset + "\tblock a user")
	console.Println(console.BoldBlue, "-clear" + console.Reset + "\t\t\tclear the screen")
	console.Println(console.BoldBlue, "-exit" + console.Reset + "\t\t\tclose the room for everybody")
	console.Println(console.BoldBlue, "-info 'nickname'" + console.Reset + "\tget information about nickname (his ip & port )")
	console.Println(console.BoldBlue, "-ls" + console.Reset + " \t\t\tshow all connected user")
	console.Println(console.BoldBlue, "-remove 'nickname'" + console.Reset + "\tremove an user")
}

func remove(nickname *string) {
	for i, user := range users {
		if (*user).nickname == *nickname {
			(*user).conn.Write(REMOVED_MESSAGE)
			(*user).conn.Close()
			users = append(users[:i], users[i + 1:]...)
			break
		}
	}
}

func startServer(ip string, port uint, password *string) error {
	ln, err := net.Listen("tcp", fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		return err
	}

	for {
        conn, _ := ln.Accept()
        go handleConnection(conn, password)
    }
}

func startShell() {
	var cmd string
	in := bufio.NewReader(os.Stdin)

	fmt.Scanln()
	for {
		fmt.Printf("> ")
		cmd, _= in.ReadString('\n')

		parseCmd(&cmd)
	}
}