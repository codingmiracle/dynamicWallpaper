import ctypes
import os.path
import suntime as sun
import time
import threading
import random


class dynamicWallpaper:
    def __init__(self, interval=60, theme="foresthouse"):
        self.interval = interval
        self.frame = 1
        self.theme = theme
        self.images = ["-house.jpg", "-cliff.jpg", "-mountain.jpg"]
        lat = 48.21
        long = 15.60
        self.sun = sun.Sun(lat, long)
        thread = threading.Thread(target=self.handleBackgroundActivity, args=())
        thread.daemon = True
        thread.start()

    def handleBackgroundActivity(self):
        down = 0
        while True:
            if self.theme == "day-night" or self.theme == "mountains":
                if self.frame < 10:
                    framestr = "00" + str(self.frame)
                elif self.frame < 100:
                    framestr = "0" + str(self.frame)
                else:
                    framestr = str(self.frame)

                ctypes.windll.user32.SystemParametersInfoW(20, 0,
                                                           "C:/Users/dagra/PycharmProjects/dynamicWallpaper/media/" + self.theme + "/ezgif-frame-" + framestr + ".jpg",
                                                           0)
                if self.theme == "day-night":
                    self.frame += 1
                    if self.frame > 190:
                        self.frame = 0
                elif self.theme == "mountains":
                    if down:
                        self.frame -= 1
                    else:
                        self.frame += 1
                    if self.frame > 119:
                        self.frame -= 1
                        down = 1
                    elif self.frame == 0:
                        self.frame += 1
                        down = 0
                time.sleep(self.interval)
            elif self.theme == "foresthouse":
                sr = int(self.sun.get_sunrise_time().strftime('%H')) + int(
                    self.sun.get_sunrise_time().strftime('%M')) / 60 - 1
                ss = int(self.sun.get_sunset_time().strftime('%H')) + int(
                    self.sun.get_sunrise_time().strftime('%M')) / 60 + 2
                t = int(time.strftime('%H')) + int(time.strftime('%M')) / 60

                diff = (ss - sr) / 7
                print(sr, ss, diff)
                ll = 1

                for i in range(4):
                    if sr + i * diff < t < ss - i * diff:
                        ll = 2 + i
                        print(ll)

                self.lastll = ll
                while True:
                    img = self.images[random.randint(0, 2)]
                    print("media/foresthouse/" + str(ll) + img)
                    if os.path.isfile("media/foresthouse/" + str(ll) + img):
                        break

                ctypes.windll.user32.SystemParametersInfoW(20, 0,
                                                           "C:/Users/dagra/PycharmProjects/dynamicWallpaper/media/foresthouse/" + str(ll) + img,
                                                           0)
                time.sleep(self.interval)


if __name__ == '__main__':
    dWal = dynamicWallpaper()
    while True:
        time.sleep(0.1)
