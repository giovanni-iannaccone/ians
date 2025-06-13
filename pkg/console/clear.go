package console

import (
	"system"
)

func Clear() {
	if system.Name == "windows" {
		system.Exec("cls")
	} else {
		system.Exec("clear")
	}
}