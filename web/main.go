package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

var toRead = "cwd"

func main() {
	cwd, err := os.Getwd()
	if err != nil {
		panic(err)
	}
	if strings.HasSuffix(cwd, "web") {
		os.Chdir("..")
		cwd, _ = os.Getwd()
		log.Println("changed directory to ", cwd)
	}

	if len(os.Args) > 0 {
		toRead = os.Args[1]
	}

	http.HandleFunc("/files", filesHandler)
	http.Handle("/node_modules/", http.StripPrefix("/node_modules/", http.FileServer(http.Dir("./web/node_modules"))))
	x := filepath.Base(toRead)
	http.Handle("/"+x+"/", http.StripPrefix("/"+x+"/", http.FileServer(http.Dir(toRead))))
	http.Handle("/", http.FileServer(http.Dir("web")))

	fmt.Println("listen on http://localhost:8080/")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func filesHandler(w http.ResponseWriter, r *http.Request) {
	ignoreDirs := []string{".bzr", ".hg", ".git"}
	files, err := listFiles(toRead, ignoreDirs)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	out, err := json.MarshalIndent(files, "", "  ")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Length", fmt.Sprint(len(out)))
	fmt.Fprint(w, string(out))
}

func listFiles(dir string, ignoreDirs []string) ([]string, error) {
	ret := []string{}
	err := filepath.Walk(dir, func(path string, info os.FileInfo, werr error) error {
		if werr == nil {
			if info.IsDir() {
				pathDir := filepath.Base(path)
				for _, d := range ignoreDirs {
					if d == pathDir {
						return filepath.SkipDir
					}
				}
			} else {
				path = path[len(dir):]
				if strings.HasSuffix(path, "/") {
					path = path[1:]
				}
				ret = append(ret, path)
			}
		}
		return nil
	})
	return ret, err
}
