from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from skimage import io,img_as_float
import pprint as pp


class Args: pass 
args_ = Args()

def list_folder(p):
    f_list = []
    f_list = list(p.glob('*us_*'))
    f_list.sort()
    return f_list

def list_files(p):
    f_list = []
    f_list=list(p.glob('**/*tiff'))
    return f_list

def pic_av(f_pic):
    f = str(f_pic)
    image = io.imread(f)
    image = img_as_float(image)
    img_av = np.mean(image)
    return img_av

def stack_av(folder_path):
    sub_dir_img = Path(folder_path).glob('*.tiff')
    sub_dir_av = []
    for img in sub_dir_img:
        sub_dir_av.append(pic_av(img))
    return sub_dir_av

def main(**kwargs):
    p = Path(kwargs['folder_path'])
    outdir = p/'results'
    outdir.mkdir(exist_ok=True, parents=True)
    print(p)
    out_file = str(outdir)+'/box_plot.png'
    folder_list = list_folder(p)
    dir_av = {}
    for sub_dir in folder_list:
        dir_av[str(sub_dir.name)] = stack_av(sub_dir)
        pp.pprint(dir_av)
    fig, ax = plt.subplots()
    plt.boxplot(dir_av.values())
    ax.set_xticklabels(dir_av.keys())
    plt.show()
    fig.savefig(out_file)

    print(folder_list)
#    pic_list = list_files(p)
##    print(pic_list)
#    pic_px_av = []
#    for pic in pic_list:
#        pic_av_ = pic_av(pic)
#        pic_px_av.append(pic_av_)
##    print(pic_px_av)
#    pic_one = np.ones(len(pic_px_av))
#    plt.boxplot(pic_px_av)
##    plt.plot(pic_px_av)
##    plt.ylim(ymin=0)
##    plt.violinplot(pic_px_av)
##    plt.show()
##    out_file = str(outdir)+"/plot_violin.png"
##    out_file = str(outdir)+"/plot_line.png"
#    out_file = str(outdir)+"/plot_box.png"
#    plt.savefig(out_file)
if __name__  == '__main__':
    import argparse
    # Argument parser.
    description = '''Analysis script for abf files.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--folder-path', '-f'
                        , required = False,
                        default ='./', type=str
                        , help = 'path of folder with  abf files '
                       )
    parser.parse_args(namespace=args_)
    main(**vars(args_)) 
