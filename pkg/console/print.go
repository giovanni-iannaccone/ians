package console

import (
	"fmt"
)

func Print(color string, format string, args ...any) {
	fmt.Print(color)
	fmt.Printf(format, args...)
	fmt.Print(Reset)
}

func Println(color string, format string, args ...any) {
	Print(color, format, args...)
	fmt.Println()
}