import numpy as np
from skimage import io
import tifffile
import os, sys, shutil
import json

########### DEBUG MODE ###########
import matplotlib.pyplot as plt
##################################

def check_and_get_system_args():
    if len(sys.argv) == 4:
        return sys.argv[1:]
    print("Usage: python run.py <settings_file.json> <mode> <clean=0|1>")
    sys.exit(1)

def clean_image(im, thresh=0.0005):
    total = im.sum()
    for i in range(im.shape[0]):
        if im[i,:].sum()/total > thresh:
            break
    for j in reversed(range(im.shape[0])):
        if im[j,:].sum()/total > thresh:
            break
    for k in range(im.shape[1]):
        if im[:,k].sum()/total > thresh:
            break
    for l in reversed(range(im.shape[1])):
        if im[:,l].sum()/total > thresh:
            break
    return im[i:j,k:l]

def get_image_sum(path, clean, thresh=0.8):
    img = tifffile.imread(path)
    im = np.sum(img.astype(np.float32), axis=0)
    im = (im - np.min(im)) / (thresh * (np.max(im) - np.min(im)))
    im = np.clip(im, 0, 1)
    if clean == 1:
        im = clean_image(im, 0.0005)
    return im

def get_image_max(path, clean, thresh=0.8):
    img = tifffile.imread(path)
    im = np.max(img.astype(np.float32), axis=0)
    im = (im - np.min(im)) / (thresh * (np.max(im) - np.min(im)))
    im = np.clip(im, 0, 1)
    if clean == 1:
        im = clean_image(im, 0.001)
    return im

def main(args):
    json_file_name = args[0]
    mode = args[1]
    clean = int(args[2])
    with open(json_file_name,) as json_file:
        ctx = json.load(json_file)
    home = ctx["raw_data_path"]
    outdir = ctx["images_path"]
    if 'data' in os.listdir('./'):
        shutil.rmtree('data/')
    os.mkdir('data')
    # t1 = "1. Fragmented"
    # t2 = '190801-HEK293-mOr_dmso-2h50m.nd2 - 190801-HEK293-mOr_dmso-2h50m.nd2 (series 03)-1.tif'
    # if mode == "max":
    #     im = get_image_max(os.path.join(home, t1, t2), clean)
    # elif mode == "sum":
    #     im = get_image_sum(os.path.join(home, t1, t2), clean)
    # plt.imshow(im, cmap="gray")
    # plt.show()
    i = 0
    for category in os.listdir(home):
        os.mkdir('data/'+category)
        for image in os.listdir(os.path.join(home, category)):
            i += 1
            if mode == "max":
                im = get_image_max(os.path.join(home, category, image), clean)
            elif mode == "sum":
                im = get_image_sum(os.path.join(home, category, image), clean)
            io.imsave(outdir+"/"+category+"/"+str(i)+".bmp", im)

if __name__ == "__main__":
    main(check_and_get_system_args())
    sys.exit(0)
