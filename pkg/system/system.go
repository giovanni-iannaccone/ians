package system

import (
	"os"
	"os/exec"
	"runtime"
)

var Name string = runtime.GOOS

func Exec(command string) error {
	var cmd *exec.Cmd = exec.Command(command)
	
	cmd.Dir, _ = os.Getwd()
	cmd.Stdout = os.Stdout

	return cmd.Run()
}