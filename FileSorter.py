from os import scandir,rename
from os.path import splitext,exists,join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directories to target
source_dr="/Users/Ahmad/Downloads"
destination_dir_music="D:/Music"
destination_dir_videos="D:/Videos"
destination_dir_images="D:/Images"
destination_dir_docs="D:/Documents"
# destination_dir_sfx=""

#Supported Images/Vids/Audio types
image_ext=['.jpg','.jpeg','.jif','.jpe','.jfif','.png','.gif','.k25','.bmp','.dib','.heif','heic','.ind','indd','indt']
video_ext=['.webm','.mpg','.mp2','.mp4v','.m4v','.avi','.vmv','.mov','.flv','.qt','.mpeg','.mpe','.mpv','.ogg','.mp4']
audio_ext=['.m4a','.flac','.mp3','.wav','.wma','.aac']
document_ext=['.doc','.docx','.odt','.pdf','.xls','.xlsx','.ppt','.pptx']

def unique_folder(destination,name):
    filename,extension=splitext(name)
    counter=1

    # check if file exists, if yes then add a number after the filename
    while exists(f"{destination}/{filename}"):
        name=f"{filename}({str(counter)}){extension}"
        counter+=1
    return name

def move_file(dest,entry,name):
    if exists(f"{dest}/{name}"):
        unique_name=unique_folder(dest,name)
        old_name=join(dest,name)
        new_name=join(dest,new_name)
        rename(old_name,new_name)
    move(entry,dest)



class MoverHandler(FileSystemEventHandler):
    #function will run whenever there is a change in source_directory "source_dir"
    #.upper is for not missing out any files having uppercase extensions
    def on_modified(self,event):
        with scandir(source_dr) as enteries:
            for entry in enteries:
                name=entry.name
                self.check_aud_files(entry,name)
                self.check_vid_files(entry,name)
                self.check_images_files(entry,name)
                self.check_doc_files(entry,name)


    def check_aud_files(self,entry,name):
        for audio in audio_ext:
            if name.endswith(audio) or name.endswith(audio.upper()):
                # if entry.stat().st_size >10_000_000 or "SFX" in name: #greater than 10MB audio file
                #     dest=destination_dir_sfx
                # else:
                #     dest=destination_dir_music
                dest = destination_dir_music
                move_file(dest,entry,name)
                logging.info(f"Moved audio file:{name}")
    
    def check_vid_files(self,entry,name):
        for video in video_ext:
            if name.endswith(video) or name.endswith(video.upper()):
                move_file(destination_dir_videos,entry,name)
                logging.info(f"Moved Video file{name}")

    def check_doc_files(self,entry,name):
        for doc in document_ext:
            if name.endswith(doc) or name.endswith(doc.upper()):
                move_file(destination_dir_docs,entry,name)
                logging.info(f"Moved Document file{name}")

    def check_images_files(self,entry,name):
        for img in image_ext:
            if name.endswith(img) or name.endswith(img.upper()):
                move_file(destination_dir_images,entry,name)
                logging.info(f"Moved Image file{name}")


if __name__ =="__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    path=source_dr
    event_handler=MoverHandler()
    observer=Observer()
    observer.schedule(event_handler,path,recursive=True)
    observer.start()
    try:
        while True:
            sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

  