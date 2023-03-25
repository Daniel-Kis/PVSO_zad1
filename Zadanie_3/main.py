import cv2 as cv
import numpy as np


def laplaceEdgeDetection(img):

    # convert to gray
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # img2 = gray
    # blur the image to remove noise
    img2 = cv.GaussianBlur(gray, (3, 3), 0)

    # img2 = cv.GaussianBlur(img, (3, 3), 0)
    # img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # various kernels for convolution with the picture
    # kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], np.float32)
    # kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], np.float32)  # <- good
    # kernel = np.array([[-1, 2, -1], [2, -4, 2], [-1, 2, -1]], np.float32)
    kernel = np.array([[1, 4, 1], [4, -20, 4], [1, 4, 1]], np.float32)  # <- best, from:
    # https://www.youtube.com/watch?v=uNP6ZwQ3r6A&ab_channel=FirstPrinciplesofComputerVision


    # apply the convolution
    hi, wi = img2.shape
    hk, wk = kernel.shape
    image_padded = np.zeros(shape=(hi + hk - 1, wi + wk - 1))
    image_padded[hk // 3:-hk // 3, wk // 3:-wk // 3] = img2
    out = np.zeros(shape=img2.shape)
    for row in range(hi):
        for col in range(wi):
            for i in range(hk):
                for j in range(wk):
                    out[row, col] += image_padded[row + i, col + j] * kernel[i, j]

    # out = np.clip(out * 255, 0, 255)  # proper [0..255] range
    # cv.imwrite("temp.png", cv.filter2D(img2, -1, kernel))
    out = np.array(out, dtype=float)/float(255)  # safe conversion
    # cv.imshow("Detected Edges", out)
    # cv.waitKey()
    # cv.destroyWindow("Detected Edges")

    return out


def main():
    # [variables]
    # Declare the variables we are going to use
    ddepth = cv.CV_16S
    kernel_size = 3
    window_name = "Laplace Demo"
    # [variables]
    # [load]
    imageName = 'img5.jpg'
    src = cv.imread(cv.samples.findFile(imageName), cv.IMREAD_COLOR)  # Load an image
    # Check if image is loaded fine
    if src is None:
        print('Error opening image')
        return -1

    # edge detection with created algorithm
    laplace_edged_picture = laplaceEdgeDetection(src)
    cv.imshow("output", laplace_edged_picture)
    cv.waitKey()
    cv.imwrite("detected_edges.png", np.clip(laplace_edged_picture * 255, 0, 255))

    # edge detection with opencv
    # [load]
    # [reduce_noise]
    # Remove noise by blurring with a Gaussian filter
    src = cv.GaussianBlur(src, (3, 3), 0)
    # [reduce_noise]
    # [convert_to_gray]
    # Convert the image to grayscale
    src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # [convert_to_gray]
    # Create Window
    cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
    # [laplacian]
    # Apply Laplace function
    dst = cv.Laplacian(src_gray, ddepth, ksize=kernel_size)
    # [laplacian]
    # [convert]
    # converting back to uint8
    abs_dst = cv.convertScaleAbs(dst)
    # [convert]
    # [display]
    cv.imshow(window_name, abs_dst)
    cv.waitKey(0)

    cv.imwrite("baseLaplacianOpencv.png", abs_dst)

    # [display]
    return 0

if __name__ == '__main__':
    main()

