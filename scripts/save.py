import os
import cv2

def countFiles(inDir, prefix):
    ret = 0
    for f in os.listdir(inDir):
        if os.path.isfile(inDir+"/"+f) and f.startswith(prefix):
            ret+=1
    return ret

def moment(toDir, filename, moment, img):
    return cv2.imwrite(toDir + "/" + moment + "--" + filename, img)

def src(toDir, filename, img):
    return moment(toDir, filename, "src", img)

def int(toDir, filename, name, img):
    cnt = countFiles(toDir, "int-")
    name = "int-"+str(cnt)+"-"+name
    return moment(toDir, filename, name, img)

def dst(toDir, filename, img):
    return moment(toDir, filename, "dst", img)
