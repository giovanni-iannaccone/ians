package console

import (
	"github.com/giovanni-iannaccone/ians/pkg/system"
)

func Clear() {
	if system.Name == "windows" {
		system.Exec("cls")
	} else {
		system.Exec("clear")
	}
}