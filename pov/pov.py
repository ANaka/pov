import cv2
import datetime
import fn
import os
from pathlib import Path

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
        got_image, image = self.cam.read()
        return image
    
    def close(self):
        self.cam.release()
        
    def save_image(self):
        now = get_current_timestamp()
        img = self.get_image()
        filepath = self.savedir.joinpath(f'{now}.jpg').as_posix()
        cv2.imwrite(filepath, img)
        self.most_recent_image_filepath = filepath
        
    

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