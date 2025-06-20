package siteMapper

import (
	"ascii"
	"console"
	"pool"
	
	"fmt"
	"os"
	"net/http"
	"runtime"
	"strings"
	"sync"
)

type submitFunction func(pool *pool.ThreadPool, prop properties, words *[]string, wg *sync.WaitGroup)

type properties struct {
	extensions 	[]string
	target 		string
}

type task struct {
	prop 	properties
	wg   	*sync.WaitGroup
	word 	string
}

var STATUS_NOT_FOUND int = 404

func (t *task) Execute() error {
	defer t.wg.Done()

	var url string = t.prop.target + t.word
	resp, _ := http.Get(url)
	if resp.StatusCode != STATUS_NOT_FOUND {
		console.Println(console.BoldGreen, "%s: %d", url, resp.StatusCode)
	}

	return nil
}

func (t *task) OnFailure(err error) {

}

func run(prop properties, words *[]string, submitTasks submitFunction) error {
	wg := &sync.WaitGroup{}
	wg.Add(len(*words))

	pool, err := pool.NewSimplePool(runtime.NumCPU(), 0)
	if err != nil {
		return err
	}

	pool.Start()
	defer pool.Stop()

	submitTasks(&pool, prop, words, wg)
	wg.Wait()
	return nil
}

func submitWords(pool *pool.ThreadPool, prop properties, words *[]string, wg *sync.WaitGroup) {
	for _, word := range *words {
		for _, extension := range prop.extensions {
			(*pool).AddWork(&task{
				prop: prop,
				word: word + extension,
				wg:   wg,
			})
		}
	}
}

func takeExtensions() []string {
	var extensions = []string{"/", "bak", "html", "inc", "js", "orig", "php"}

	var option string
	console.Print(console.BoldBlue, "This are the default extensions: %#v", extensions)
	console.Print(console.Reset, "Do you want to use these ? [y/n] ")
	fmt.Scanf("%s", &option)

	if option == "y" || option == "Y" {
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