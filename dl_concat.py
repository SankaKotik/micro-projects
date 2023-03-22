import os

mylist_text = ''
with open ('list.txt') as file:
    for num, line in enumerate (file, start=1):
        os.system (f'wget {line.rstrip ()} -O {num}.mp3')
        mylist_text += f'file {num}.mp3\n'

with open ('mylist.txt', 'w+') as file:
    file.write (mylist_text)

os.system ('ffmpeg -hide_banner -f concat -i mylist.txt -c copy out.mp3')
print ('All files concatenated!')