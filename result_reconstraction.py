import json, cv2, os, glob
import numpy as np
import pandas as pd

def create_img_lr(img_lr, df):
    R = cv2.imread('saved_data/R.png')
    L = cv2.imread('saved_data/L.png')
    pnames = list(df['patch_name'])
    cx_list = list(df['cx'])
    cy_list = list(df['cy'])
    lr_list = list(df['label'])
    for i, (cx, cy, lr) in enumerate(zip(cx_list, cy_list, lr_list)):
        cv2.circle(img_lr, (cx, cy), 15, (255, 255, 255), thickness=-1)
        if int(lr) == 0:
            cv2.circle(img_lr, (cx, cy), 15, (0, 0, 255), thickness=2)
            img_lr[cy-10:cy+10, cx-10:cx+10] = R
        elif int(lr) == 1:
            cv2.circle(img_lr, (cx, cy), 15, (255, 0, 0), thickness=2)
            img_lr[cy-10:cy+10, cx-10:cx+10] = L
        else:
            print('type mismatching !!')
    return img_lr

def main(DIRNAME):
    pths_img = glob.glob(os.path.join(DIRNAME, '*.png'))
    pths_df = glob.glob(os.path.join(DIRNAME, '*.csv'))
    pths_json = glob.glob(os.path.join(DIRNAME, '*.json'))

    for pth_json, pth_img, pth_df in zip(pths_json, pths_img, pths_df):

        # load (fname, bb, contour, arrangement) from json 
        f = open(pth_json, 'r')
        dic = json.load(f)
        fname = dic['fname'].split('_')[0] + '.png' if '_' in dic['fname'] else dic['fname']
        bb = dic['bb']
        contour = dic['contour']
        arr = dic['arrangement']

        # load img, df 
        img = cv2.imread(pth_img)
        df_natural_patch = pd.read_csv(pth_df)

        img_bb = np.copy(img)
        cv2.rectangle(img_bb, (bb[0], bb[1]), (bb[2], bb[3]), (255, 255, 0), thickness=4)

        mask = cv2.drawContours(np.zeros(img.shape[:2], np.uint8), np.array(contour).reshape(1, -1, 2), 0, color=1, thickness=-1)
        img_fore = cv2.bitwise_and(img, img, mask=mask)

        img_corner = np.copy(img)
        for xy in zip(df_natural_patch.cx, df_natural_patch.cy):
            cv2.circle(img_corner, xy, 1, (255,255,0), 5)

        img_lr = np.copy(img)
        img_lr = create_img_lr(img_lr, df_natural_patch)
        for name, img in zip(['img_bb', 'mask', 'img_fore', 'img_corner', 'img_lr'], [img_bb, mask*255, img_fore, img_corner, img_lr]):
            cv2.imwrite(f'./{DIRNAME}/{name}.png', img)

if __name__ == "__main__":
    import sys

    args = sys.argv
    dir_path = args[1]
    main(dir_path)