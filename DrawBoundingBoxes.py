import cv2

class BboxPlot():
    def __init__(self,img,targets,classes):
        self.image=img
        self.targets=targets
        self.classes=classes
    def yolov8Plot(self,save_path='',img_name=''):
        for box in self.targets.boxes:
            c, p,x, y, w, h = box
            cv2.rectangle(self.image, (int(x), int(y)), (int(w), int(h)), (255, 255, 0), 2)
            ind=int(c)-1
            cv2.putText(self.image,str(self.classes[ind]),(int(x),int(y-10)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0))
        cv2.imwrite(save_path+"/" + img_name, self.image)
        return self.image