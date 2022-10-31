from filetype import guess
path = "C:\\Users\\anandwal\\OneDrive - MONSTER.Com (India) Pvt Ltd\\Desktop\\MASTER\\procyon\\app\\resume_parser\\tmp\\110053586.doc"

kind = filetype.guess(path)
print(kind)