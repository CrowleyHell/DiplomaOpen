import glob
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import cv2
import os
from PIL import Image

SAVING_FRAMES_PER_SECOND = 60

def get_saving_frames_durations(cap, saving_fps):
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def pic(id):
    video_file = f'video/{id}.avi'
    filename = f'{id}'
    if not os.path.isdir(filename):
        os.mkdir(filename)
    cap = cv2.VideoCapture(video_file)
    fps = SAVING_FRAMES_PER_SECOND
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    count = 0
    save_count = 0
    i = 0
    while True:
        i += 1
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps
        closest_duration = saving_frames_durations[0]
        if frame_duration >= closest_duration:
            saveframe_name = os.path.join(filename, f"frame{i}.jpg")
            cv2.imwrite(saveframe_name, frame)
            save_count += 1
            saving_frames_durations.pop(0)
        count += 1


def frame(files):
    for x in files:
        foo = Image.open(x)
        w, h = foo.size
        crop = foo.crop((w / 2.75, h / 3, w / 1.85, h / 2))
        crop.save(f'{x}', optimize=True, quality=95)


class imarray(object):
    def __lconvert(self):
        self.__image = [[y[0] * 299 / 1000 + y[1] * 587 / 1000 + y[2] * 114 / 1000 for y in x] for x in self.__image]

    def __init__(self, path=None, mode='L'):
        if path == None:
            return
        try:
            self.__image = imageio.imread(path)  # mode=mode
            # self.__image = Image.fromarray(np.asarray(Image.open(path)))
            if mode == 'L':
                self.__lconvert()

        except:
            print("Error! Could not read the image from the path specified: %s" % path)
            return
        try:
            self.__image = np.asarray(self.__image)
            self.__dimension = self.__image.shape
            self.__type = path.split(".")[-1]
        except:
            print("Internal Error! Image file not supported")

    def __repr__(self):
        return repr(self.__image)

    #def __cmp__(self, img):
    #    return cmp(self, img)

    def __getitem__(self, coordinates):
        return self.__image[coordinates]

    def load(self, image):
        image = np.asarray(image, dtype=np.uint8)
        if len(image.shape) == 2:
            self.__image = image
            try:
                self.__dimension = self.__image.shape
            except:
                print("Internal Error! Image file not supported")
        else:
            print("Assignment Error. Given input is not an image")

    def getShape(self):
        return self.__dimension

    shape = property(getShape)

    def getExtension(self):
        return self.__type

    ext = property(getExtension)

    def displayImage(self, mode='Greys_r'):
        try:
            plt.imshow(self.__image, cmap=mode)
        except:
            print("Image could not be displayed")
            return
        plt.show()

    disp = property(displayImage)

    def save(self, name):
        plt.imsave(name, self.__image, cmap='Greys_r')

    def convolve(self, mask):
        mask = np.asarray(mask, dtype=np.float32)
        (m, n) = mask.shape
        padY = int(np.floor(m / 2))
        padX = int(np.floor(n / 2))
        (M, N) = self.__dimension
        padImg = np.ones((M + padY * 2, N + padX * 2)) * 128
        fImage = np.zeros((M + padY * 2, N + padX * 2))
        padImg[padY:-padY, padX:-padX] = self.__image

        for yInd in range(padY, M + padY):
            for xInd in range(padX, N + padX):
                fImage[yInd, xInd] = sum(
                    sum(padImg[yInd - padY:yInd + m - padY, xInd - padX:xInd + n - padX] * mask))

        return fImage[padY:-padY, padX:-padX]




def smoothen(img):
    gaussian = np.array(
        [[1 / 16., 1 / 8., 1 / 16.], [1 / 8., 1 / 4., 1 / 8.], [1 / 16., 1 / 8., 1 / 16.]])
    img.load(img.convolve(gaussian))
    return img


def edge(img, threshold):
    laplacian = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    # sobel = np.array([[3, 0, -3], [10, 0, -10], [3, 0, -3]])
    sobel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    G_x = img.convolve(sobel)
    G_y = img.convolve(np.fliplr(sobel).transpose())
    G = pow((G_x * G_x + G_y * G_y), 0.5)
    G[G < threshold] = 0
    L = img.convolve(laplacian)
    if L is None:
        return
    (M, N) = L.shape

    temp = np.zeros((M + 2, N + 2))
    temp[1:-1, 1:-1] = L
    result = np.zeros((M, N))
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if temp[i, j] < 0:
                for x, y in (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1):
                    if temp[i + x, j + y] > 0:
                        result[i - 1, j - 1] = 1
    img.load(np.array(np.logical_and(result, G), dtype=np.uint8))
    return img


def detectCircles(img, threshold, region, radius=None):
    (M, N) = img.shape
    if radius == None:
        R_max = np.max((M, N))
        R_min = 3
    else:
        [R_max, R_min] = radius

    R = R_max - R_min
    A = np.zeros((R_max, M + 2 * R_max, N + 2 * R_max))
    B = np.zeros((R_max, M + 2 * R_max, N + 2 * R_max))
    theta = np.arange(0, 360) * np.pi / 180
    edges = np.argwhere(img[:, :])
    for val in range(R):
        r = R_min + val
        bprint = np.zeros((2 * (r + 1), 2 * (r + 1)))
        (m, n) = (r + 1, r + 1)
        for angle in theta:
            x = int(np.round(r * np.cos(angle)))
            y = int(np.round(r * np.sin(angle)))
            bprint[m + x, n + y] = 1
        constant = np.argwhere(bprint).shape[0]
        for x, y in edges:
            X = [x - m + R_max, x + m + R_max]
            Y = [y - n + R_max, y + n + R_max]
            A[r, X[0]:X[1], Y[0]:Y[1]] += bprint
        A[r][A[r] < threshold * constant / r] = 0

    for r, x, y in np.argwhere(A):
        temp = A[r - region:r + region, x - region:x + region, y - region:y + region]
        try:
            p, a, b = np.unravel_index(np.argmax(temp), temp.shape)
        except:
            continue
        B[r + (p - region), x + (a - region), y + (b - region)] = 1

    return B[:, R_max:-R_max, R_max:-R_max]


def proc(id):
    pic(id)
    files = glob.glob(f'{id}/*.jpg')
    frame(files)
    xMass = []
    yMass = []
    xxMass = []
    files = glob.glob(f'{id}/*.jpg')
    i = 0
    for ffile in files:
        i += 1
        file_path = ffile
        img = imarray(file_path)
        res = smoothen(img)
        res = edge(res, 33)
        res = detectCircles(res, 4.3, 19, radius=[10, 9])
        circleCoordinates = np.argwhere(res)  # Extracting the circle information
        # circle = []
        # img2 = imageio.imread(file_path)
        # fig, ax = plt.subplots(1)
        # ax.imshow(img2)
        for r, x, y in circleCoordinates:
            #print(y, x)
            if 44 < x < 48:
                yMass.append(x)
                xxMass.append(y)
            # circle.append(plt.Circle((y, x), r, color=(1, 0, 0), fill=False))
            # fig.add_subplot(111).add_artist(circle[-1])
            # ax.add_patch(circle[-1])
        # plt.savefig(f'./{id}/{i}')
        #plt.show()
    for i in range(len(yMass)):
        xMass.append(i)
    plt.clf()
    plt.plot(xMass, yMass, color='b', linewidth=1)
    mn = min(xxMass)
    mx = max(xxMass)
    #print(mn, mx)
    for i in range(len(yMass)):
        if xxMass[i] == mx or xxMass[i] == mn or xxMass[i] == mx - 1:
            plt.vlines(i, 45, 47, color='red')
    plt.savefig(f'results/{id}.jpg')
    #plt.show()
# file_path = 'frame1.jpg'
# img = imarray(file_path)
# res = smoothen(img)
# res = edge(res, 30)
#
# res = detectCircles(res, 4.3, 19, radius=[10, 9])
# # res = detectCircles(res, 11.0, 60, radius=[34, 30])
#
# circleCoordinates = np.argwhere(res)  # Extracting the circle information
# circle = []
# img2 = imageio.imread(file_path)
# fig, ax = plt.subplots(1)
# ax.imshow(img2)
# for r, x, y in circleCoordinates:
#     print("circle!", y, x, r)
#     circle.append(plt.Circle((y, x), r, color=(1, 0, 0), fill=False))
#     # fig.add_subplot(111).add_artist(circle[-1])
#     ax.add_patch(circle[-1])
# plt.savefig('tt.jpg')
# plt.show()
