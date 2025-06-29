package files

import (
	"console"

	"os"
	"strings"
)

func ReadLineByLine(path string, printErrors bool) []string {
	buffer, err := os.ReadFile(path)
	if err != nil {
		if printErrors {
			console.Error(err.Error())
		} else {
			return nil
		}
	}

	return strings.Split(string(buffer), "\n")
}