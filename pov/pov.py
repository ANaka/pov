import cv2
import datetime
import fn
import os
from PIL import Image
from pathlib import Path
import time

class Camera(object):
    """for recording images from streaming source. right now assumes only one video source will be available
    
    >> cam = Camera()
    >> im = cam.get_image()
    >> cam.save_image()
    >> cam.close()
    """    
    def __init__(self, savedir=None):
        self._camera_index = get_camera_index()
        self.cam = cv2.VideoCapture(self._camera_index)
        self.plot_id = fn.get_current_plot_id()
        if savedir == None:
            savedir = f'/home/naka/Videos/pov/{self.plot_id}'
        self.savedir = Path(savedir)
        
        if not self.savedir.exists():
            os.mkdir(self.savedir)
        
    def get_image(self):
        got_image, _image = self.cam.read()
        image = cv2.cvtColor(_image, cv2.COLOR_RGB2BGR)
        return image
    
    def close(self):
        self.cam.release()
        
    def save_image(self):
        now = get_current_timestamp()
        img = self.get_image()
        filepath = self.savedir.joinpath(f'{now}.jpg').as_posix()
        cv2.imwrite(filepath, img)
        self.most_recent_image_filepath = filepath
        
    def preview(self):
        img = self.get_image()
        return Image.fromarray(img)
    
    def video_preview(self):
        
        print('hit q to quit')
        while(True):
            frame = self.get_image()
        
            # Display the resulting frame
            cv2.imshow('frame', frame)
            
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Destroy all the windows
        cv2.destroyAllWindows()
        
    def get_video(self, wait_time=0.):
        print('hit q to quit')
        while(True):
            frame = self.get_image()
            now = get_current_timestamp()
            frame = self.get_image()
            filepath = self.savedir.joinpath(f'{now}.jpg').as_posix()
            cv2.imwrite(filepath, frame)
            # Display the resulting frame
            cv2.imshow('frame', frame)
            
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(wait_time)
        
    

def return_camera_indices():
#     https://stackoverflow.com/questions/8044539/listing-available-devices-in-python-opencv
    
    # checks the first 10 indices.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

def get_camera_index():
    camera_indices = return_camera_indices()
    assert len(camera_indices) > 0, 'No camera detected'
    assert len(camera_indices) < 2, 'Multiple cameras detected and I have not yet planned for this'
    return camera_indices[0]

def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d_T%H-%M-%S-%f')