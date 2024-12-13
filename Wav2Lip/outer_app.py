import os

def find(search, filename):
    for root, dirs, files in os.walk(search):
        if filename in files:
            print("Found file:", os.path.join(root, filename))
            return True
    print("File not found")
    return False

    
search = 'results/'
filename  = 'result_voice.mp4'

if(find(search, filename)):
    print("1")

