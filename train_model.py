import argparse
import os.path as osp

import mmcv
from mmcv import Config
from mmdet.apis import train_detector
from mmdet.datasets import build_dataset
from mmdet.models import build_detector

from dataset.data_config import data_configs
from model.Faster_RCNN import get_faster_rcnn_config
from model.RetinaNet import get_retinanet_config
from model.RetinaNet_EfficientNet import get_retinanet_efficientnet_config
from model.RetinaNet_EfficientNet_Data_Augmentation import get_retinanet_efficientnet_data_augmentation_config
from model.RetinaNet_Swin import get_retinanet_swin_config
from model.RetinaNet_Swin_Data_Augmentation import get_retinanet_swin_data_augmentation_config
from model.SSD import get_ssd_config
from model.VFNet import get_vfnet_config


def get_train_config(opt):
    data_cfg = data_configs[str(opt.num_classes)][str(opt.img_size)]

    if opt.method == "Faster_RCNN":
        return get_faster_rcnn_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=opt.pretrained
        )
    if opt.method == "RetinaNet":
        return get_retinanet_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=opt.pretrained
        )
    if opt.method == "VFNet":
        return get_vfnet_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=opt.pretrained
        )
    if opt.method == "RetinaNet_Swin":
        return get_retinanet_swin_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=False
        )
    if opt.method == "RetinaNet_EfficientNet":
        return get_retinanet_efficientnet_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=False
        )
    if opt.method == "RetinaNet_Swin_Data_Aug":
        return get_retinanet_swin_data_augmentation_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=False
        )
    if opt.method == "RetinaNet_EfficientNet_Data_Aug":
        return get_retinanet_efficientnet_data_augmentation_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=False
        )
    if opt.method == "SSD":
        return get_ssd_config(
            data_config=data_cfg,
            num_classes=opt.num_classes,
            img_size=opt.img_size,
            max_epochs=opt.epochs,
            lr=opt.lr,
            pretrained=False
        )


def train_model(opt):
    cfg = get_train_config(opt)

    # Build dataset
    datasets = [build_dataset(cfg.data.train)]

    # Build the detector
    model = build_detector(cfg.model)
    # Add an attribute for visualization convenience
    model.CLASSES = datasets[0].CLASSES
    if opt.pretrained is False or opt.method == 'RetinaNet_Swin':
        model.init_weights()

    # Create work_dir
    mmcv.mkdir_or_exist(osp.abspath(cfg.work_dir))
    cfg.dump(osp.join(cfg.work_dir, opt.method + '.py'))

    train_detector(model, datasets, cfg, distributed=False, validate=True)


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', required=True, type=str, default='Faster_RCNN', help='Method to train model')
    parser.add_argument('--img_size', required=True, type=int, default=640, help='train, val image size (pixels)')
    parser.add_argument('--num_classes', required=True, type=int, default=2, help='number of classes: 2 or 3')
    parser.add_argument('--epochs', type=int, default=12, help='number of epochs training')
    parser.add_argument('--lr', type=float, default=0.0025, help='initial learning rate')
    parser.add_argument('--pretrained', action="store_true", help='Use pretrained model')

    return parser.parse_known_args()[0] if known else parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    train_model(opt)
