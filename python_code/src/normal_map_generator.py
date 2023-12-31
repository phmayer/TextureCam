# Credits:
# This code is taken from: https://github.com/Mehdi-Antoine/NormalMapGenerator

import argparse
import math
import numpy as np
from scipy import ndimage
from matplotlib import pyplot
from PIL import Image, ImageOps
import os
import multiprocessing as mp


def smooth_gaussian(im:np.ndarray, sigma) -> np.ndarray:

    if sigma == 0:
        return im

    im_smooth = im.astype(float)
    kernel_x = np.arange(-3*sigma,3*sigma+1).astype(float)
    kernel_x = np.exp((-(kernel_x**2))/(2*(sigma**2)))

    im_smooth = ndimage.convolve(im_smooth, kernel_x[np.newaxis])

    im_smooth = ndimage.convolve(im_smooth, kernel_x[np.newaxis].T)

    return im_smooth


def gradient(im_smooth:np.ndarray):

    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.arange(-1,2).astype(float)
    kernel = - kernel / 2

    gradient_x = ndimage.convolve(gradient_x, kernel[np.newaxis])
    gradient_y = ndimage.convolve(gradient_y, kernel[np.newaxis].T)

    return gradient_x,gradient_y


def sobel(im_smooth):
    gradient_x = im_smooth.astype(float)
    gradient_y = im_smooth.astype(float)

    kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    gradient_x = ndimage.convolve(gradient_x, kernel)
    gradient_y = ndimage.convolve(gradient_y, kernel.T)

    return gradient_x,gradient_y


def compute_normal_map(gradient_x:np.ndarray, gradient_y:np.ndarray, intensity=1):

    width = gradient_x.shape[1]
    height = gradient_x.shape[0]
    max_x = np.max(gradient_x)
    max_y = np.max(gradient_y)

    max_value = max_x

    if max_y > max_x:
        max_value = max_y

    normal_map = np.zeros((height, width, 3), dtype=np.float32)

    intensity = 1 / intensity

    strength = max_value / (max_value * intensity)

    normal_map[..., 0] = gradient_x / max_value
    normal_map[..., 1] = gradient_y / max_value
    normal_map[..., 2] = 1 / strength

    norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))

    normal_map[..., 0] /= norm
    normal_map[..., 1] /= norm
    normal_map[..., 2] /= norm

    normal_map *= 0.5
    normal_map += 0.5

    return normal_map


def normalized(a) -> float: 
    factor = 1.0/math.sqrt(np.sum(a*a)) # normalize
    return a*factor


def my_gauss(im:np.ndarray):
    return ndimage.uniform_filter(im.astype(float),size=20)


def shadow(im:np.ndarray):
    
    shadowStrength = .5
    
    im1 = im.astype(float)
    im0 = im1.copy()
    im00 = im1.copy()
    im000 = im1.copy()

    for _ in range(0,2):
        im00 = my_gauss(im00)

    for _ in range(0,16):
        im0 = my_gauss(im0)

    for _ in range(0,32):
        im1 = my_gauss(im1)

    im000=normalized(im000)
    im00=normalized(im00)
    im0=normalized(im0)
    im1=normalized(im1)
    im00=normalized(im00)

    shadow=im00*2.0+im000-im1*2.0-im0 
    shadow=normalized(shadow)
    mean = np.mean(shadow)
    rmse = np.sqrt(np.mean((shadow-mean)**2))*(1/shadowStrength)
    shadow = np.clip(shadow, mean-rmse*2.0,mean+rmse*0.5)

    return shadow


def flipgreen_path(path:str):
    try:
        with Image.open(path) as img:
            red, green, blue, alpha= img.split()
            image = Image.merge("RGB",(red,ImageOps.invert(green),blue))
            image.save(path)
    except ValueError:
        with Image.open(path) as img:
            red, green, blue = img.split()
            image = Image.merge("RGB",(red,ImageOps.invert(green),blue))
            image.save(path)


def flipgreen(img):
    try:
        red, green, blue, alpha= img.split()
        image = Image.merge("RGB",(red,ImageOps.invert(green),blue))
        return image
    except ValueError:
        red, green, blue = img.split()
        image = Image.merge("RGB",(red,ImageOps.invert(green),blue))
        return image


def CleanupAO_path(path:str):
    '''
    Remove unnsesary channels.
    '''
    try:
        with Image.open(path) as img:
            red, green, blue, alpha= img.split()
            NewG = ImageOps.colorize(green,black=(100, 100, 100),white=(255,255,255),blackpoint=0,whitepoint=180)
            NewG.save(path)
    except ValueError:
        with Image.open(path) as img:
            red, green, blue = img.split()
            NewG = ImageOps.colorize(green,black=(100, 100, 100),white=(255,255,255),blackpoint=0,whitepoint=180)
            NewG.save(path)


def CleanupAO(img):
    '''
    Remove unnsesary channels.
    '''
    try:
        red, green, blue, alpha= img.split()
        NewG = ImageOps.colorize(green,black=(100, 100, 100),white=(255,255,255),blackpoint=0,whitepoint=180)
        return NewG
    except ValueError:
        red, green, blue = img.split()
        NewG = ImageOps.colorize(green,black=(100, 100, 100),white=(255,255,255),blackpoint=0,whitepoint=180)
        return NewG


def convert_normal_path(input_file_path,output_file_path,smoothness,intensity):

    im = np.array(Image.open(input_file_path))

    if im.ndim == 3:
        im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
        im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
        im = im_grey

    im_smooth = smooth_gaussian(im, smoothness)

    sobel_x, sobel_y = sobel(im_smooth)

    normal_map = compute_normal_map(sobel_x, sobel_y, intensity)

    pyplot.imsave(output_file_path,normal_map)

    flipgreen_path(output_file_path)


#def convert_normal(input_img, smoothness, intensity):
#
#    im = np.array(input_img)
#
#    if im.ndim == 3:
#        im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
#        im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
#        im = im_grey
#
#    im_smooth = smooth_gaussian(im, smoothness)
#
#    sobel_x, sobel_y = sobel(im_smooth)
#
#    normal_map = compute_normal_map(sobel_x, sobel_y, intensity)
#    normal_map_image = Image.fromarray(normal_map)
#    im_normal = flipgreen(normal_map_image)
#    return im_normal


def convert_ao_path(input_file_path,output_file_path):

    im = np.array(Image.open(input_file_path))

    if im.ndim == 3:
        im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
        im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
        im = im_grey

    im_shadow = shadow(im)

    pyplot.imsave(output_file_path,im_shadow)
    CleanupAO_path(output_file_path)


#def convert_ao(input_img):
#
#    im = np.array(input_img)
#
#    if im.ndim == 3:
#        im_grey = np.zeros((im.shape[0],im.shape[1])).astype(float)
#        im_grey = (im[...,0] * 0.3 + im[...,1] * 0.6 + im[...,2] * 0.1)
#        im = im_grey
#
#    im_shadow = shadow(im)
#    
#    #maybe improve this:
#    pyplot.imsave("./result_ao.png",im_shadow)
#    CleanupAO("./result.png")
#    #im_ao = Image.open("./temp_ao_img.jpg")
#    #return im_ao

