package system

import (
	"os"
	"os/exec"
	"runtime"
	"strings"
)

var Name string = runtime.GOOS

func Exec(command string) error {
	splitArray := strings.Split(command, " ")
	main := splitArray[0]
	args := splitArray[1:]
	var cmd *exec.Cmd = exec.Command(main, args...)
	
	cmd.Stdout = os.Stdout

	return cmd.Run()
}