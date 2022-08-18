import argparse

from sahi.slicing import slice_coco
from pathlib import Path
from path_config import PathConfig

pathConfig = PathConfig()


def slice_data(parser) -> None:
    num_classes = parser.num_classes
    image_size = parser.image_size

    if num_classes == 2:
        data_root = pathConfig.data_2_classes
        train_input_annotation_path = pathConfig.train_annotation_2_classes_path
        val_input_annotation_path = pathConfig.val_annotation_2_classes_path
    if num_classes == 3:
        data_root = pathConfig.data_3_classes
        train_input_annotation_path = pathConfig.train_annotation_3_classes_path
        val_input_annotation_path = pathConfig.val_annotation_3_classes_path

    if image_size == 256:
        output_image_path = data_root / pathConfig.size_256_image_path
        output_annotation_path = data_root / pathConfig.size_256_annotation_path

    if image_size == 512:
        output_image_path = data_root / pathConfig.size_512_image_path
        output_annotation_path = data_root / pathConfig.size_512_annotation_path

    if image_size == 640:
        output_image_path = data_root / pathConfig.size_640_image_path
        output_annotation_path = data_root / pathConfig.size_640_annotation_path

    if image_size == 1024:
        output_image_path = data_root / pathConfig.size_1024_image_path
        output_annotation_path = data_root / pathConfig.size_1024_annotation_path

    Path(output_annotation_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_image_path / "train_images").parent.mkdir(parents=True, exist_ok=True)
    Path(output_image_path / "val_images").parent.mkdir(parents=True, exist_ok=True)

    # slice train dataset
    coco_dict, coco_path = slice_coco(
        coco_annotation_file_path=train_input_annotation_path,
        image_dir=pathConfig.train_image_path,
        output_coco_annotation_file_name=str(output_annotation_path / "train_annotations"),
        ignore_negative_samples=True,
        output_dir=output_image_path / "train_images",
        slice_height=image_size,
        slice_width=image_size,
        overlap_height_ratio=0.2,
        overlap_width_ratio=0.2,
        min_area_ratio=0.9,
    )

    # slice val dataset
    coco_dict, coco_path = slice_coco(
        coco_annotation_file_path=val_input_annotation_path,
        image_dir=pathConfig.val_image_path,
        output_coco_annotation_file_name=str(output_annotation_path / "val_annotations"),
        ignore_negative_samples=True,
        output_dir=output_image_path / "val_images",
        slice_height=image_size,
        slice_width=image_size,
        overlap_height_ratio=0.2,
        overlap_width_ratio=0.2,
        min_area_ratio=0.9,
    )


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_size', required=True, type=int, default=640, help='train, val image size (pixels)')
    parser.add_argument('--num_classes', required=True, type=int, default=2, help='number of classes: 2 or 3')

    return parser.parse_known_args()[0] if known else parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    slice_data(opt)