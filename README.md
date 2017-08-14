# cv-playground

Clone and consume this repo to test about computer vision.

# Usage

```sh
git clone https://github.com/mh-cbon/cv-playground.git
# do the required setup steps (golang,opencv etc see below).
cd cv-playground
```

- put your python script using cv2 / scipy etc into scripts.
- add input pictures into `input`
- run `sh run.sh <py script>`
- browse to `http://localhost:8080/`

Everytime the python scripts are updated, `run.sh` executes the python script,
go hit the `refresh button` in the web ui to check the results.

### api helpers

In your python scripts import `save.py`, and make use of its api to save
various pre-processing steps and check their results.

The web ui will take advantage of this to re order the pictures display on screen.

```python
import save

src = cv2.imread(srcFile)
img = src.copy()

save.src(fileOutDir, filename, src) # saves an original source

img = cv2.bilateralFilter(img,20,75,75)
save.int(fileOutDir, filename, "bilateral", img) # will save an intermediary changes as int-N-bilateral

save.dst(fileOutDir, filename, dst) # saves the final result
```

All other scripts found into `scripts/` are fuctions i found on the internet,
or some i wrote myself, you might ignore them completely.

# setup

fedora 26 as of august 2017

```sh
# get go https://golang.org/dl/
sudo dnf install opencv opencv-devel python-opencv python-scipy -y
go get github.com/loov/watchrun
pip install imutils --user
```

Here i have been using that to work with python2.7, and opencv3.3.

# why ?

Becasue it does not use the opencv window api
you might run that over `vagrant ssh` + port forwarding, which might be handy.

Otherwise, its just good at checking the effect of a script on multiple inputs,
it helps to practice computer vision.
