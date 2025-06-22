package console

import (
	"fmt"
	"os"
)

func Error(format string, args ...any) {
	fmt.Print(BoldRed)
	fmt.Print("[ERROR] " + format + "\n", args)
	fmt.Print(Reset)
}

func Fatal(format string, args ...any) {
	Error(format, args...)
	os.Exit(1)
}