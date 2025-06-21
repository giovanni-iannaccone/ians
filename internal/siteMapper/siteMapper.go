package siteMapper

import (
	"ascii"
	"console"
	"pool"
	"progressbar"

	"fmt"
	"net/http"
	"os"
	"runtime"
	"strings"
)

type submitFunction func(pool *pool.ThreadPool, prop properties, words *[]string, ch chan bool)

type properties struct {
	extensions 	[]string
	target 		string
}

type task struct {
	ch 		chan bool
	prop 	properties
	word 	string
}

var STATUS_NOT_FOUND int = 404

func (t *task) Execute() error {
	defer func() {
		t.ch <- true
	}()

	var url string = t.prop.target + t.word
	resp, err := http.Get(url)
	if err != nil {
		return err
	}

	if resp.StatusCode != STATUS_NOT_FOUND {
		console.Println(console.BoldGreen, "%s: %d" + strings.Repeat(" ", 50) + "\n", t.word, resp.StatusCode)
	}

	resp.Body.Close()
	return nil
}

func (t *task) OnFailure(err error) {

}

func run(prop properties, words *[]string, submitTasks submitFunction) error {
	var totalWords uint = uint(len(*words) * len(prop.extensions))
	console.Println(console.Red, "%d words will be tryed", totalWords)

	pool, err := pool.NewSimplePool(runtime.NumCPU(), 0)
	if err != nil {
		return err
	}

	pool.Start()
	defer pool.Stop()

	ch := make(chan bool)
	go submitTasks(&pool, prop, words, ch)
	progressbar.DisplayProgressBar(totalWords, ch)

	return nil
}

func submitWords(pool *pool.ThreadPool, prop properties, words *[]string, ch chan bool) {
	for _, word := range *words {
		for _, extension := range prop.extensions {
			(*pool).AddWork(&task{
				ch: 	ch,
				prop: 	prop,
				word: 	word + extension,
			})
		}
	}
}

func takeExtensions() []string {
	var extensions = []string{"", "bak", "html", "inc", "js", "orig", "php"}

	var option string
	console.Println(console.BoldBlue, "This are the default extensions: %s", console.FmtArray(extensions))
	console.Print(console.Reset, "Do you want to use these ? [y/n] ")
	fmt.Scanf("%s", &option)

	if option != "y" && option != "Y" {
		var extensionsRaw string

		console.Print(console.BoldBlue, "[+] " + console.Reset + "Write your extensions separated by space: ")
		console.Scan(&extensionsRaw)
		extensions = strings.Split(extensionsRaw, " ")
	}

	return extensions
}

func Initialize() {
	ascii.SiteMapper()
	console.Println(console.BoldRed, "\t\tA site directories's bruteforce tool")

	var target string
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Type the target: ")
	fmt.Scanf("%s", &target)

	var extensions []string = takeExtensions()

	var path string
	console.Print(console.BoldBlue, "[+] " + console.Reset + "Enter the wordlist's path: ")
	fmt.Scanf("%s", &path)

	buffer, err := os.ReadFile(path)
	if err != nil {
		console.Fatal(err.Error())
	}

	var words []string = strings.Split(string(buffer), "\n")

	console.Println(console.Red, "\nMapper is ready, press ENTER to start...")
	fmt.Scanln()

	err = run(properties{extensions, target}, &words, submitWords)
	if err != nil {
		console.Error(err.Error())
	}

	console.Println(console.Reset, "\n")
	fmt.Scanln()
}