model = dict(
    type='RetinaNet',
    backbone=dict(
        type='ResNeXt',
        depth=101,
        num_stages=4,
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(
            type='Pretrained', checkpoint='open-mmlab://resnext101_64x4d'),
        groups=64,
        base_width=4),
    neck=dict(
        type='FPN',
        in_channels=[256, 512, 1024, 2048],
        out_channels=256,
        start_level=1,
        add_extra_convs='on_input',
        num_outs=5),
    bbox_head=dict(
        type='RetinaHead',
        num_classes=2,
        in_channels=256,
        stacked_convs=4,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            octave_base_scale=4,
            scales_per_octave=3,
            ratios=[0.5, 1.0, 2.0],
            strides=[8, 16, 32, 64, 128]),
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[1.0, 1.0, 1.0, 1.0]),
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        loss_bbox=dict(type='L1Loss', loss_weight=1.0),
        train_cfg=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.5,
                neg_iou_thr=0.4,
                min_pos_iou=0,
                ignore_iof_thr=-1),
            allowed_border=-1,
            pos_weight=-1,
            debug=False),
        test_cfg=dict(
            nms_pre=1000,
            min_bbox_size=0,
            score_thr=0.05,
            nms=dict(type='nms', iou_threshold=0.5),
            max_per_img=100)),
    train_cfg=dict(
        assigner=dict(
            type='MaxIoUAssigner',
            pos_iou_thr=0.5,
            neg_iou_thr=0.4,
            min_pos_iou=0,
            ignore_iof_thr=-1),
        allowed_border=-1,
        pos_weight=-1,
        debug=False),
    test_cfg=dict(
        nms_pre=1000,
        min_bbox_size=0,
        score_thr=0.05,
        nms=dict(type='nms', iou_threshold=0.5),
        max_per_img=100))
dataset_type = 'CocoDataset'
data_root = '/content/drive/MyDrive/data_2_classes/size_256/images'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(256, 256), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(
        type='Normalize',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=True),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(256, 256),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img'])
        ])
]
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type='CocoDataset',
        ann_file=
        '/content/drive/MyDrive/data_2_classes/size_256/annotations/train_annotations_coco.json',
        img_prefix='train_images',
        pipeline=train_pipeline,
        data_root='/content/drive/MyDrive/data_2_classes/size_256/images',
        classes=('normal', 'cancer')),
    val=dict(
        type='CocoDataset',
        ann_file=
        '/content/drive/MyDrive/data_2_classes/size_256/annotations/val_annotations_coco.json',
        img_prefix='val_images',
        pipeline=test_pipeline,
        data_root='/content/drive/MyDrive/data_2_classes/size_256/images',
        classes=('normal', 'cancer')),
    test=dict(
        type='CocoDataset',
        ann_file=
        '/content/drive/MyDrive/data_2_classes/size_256/annotations/val_annotations_coco.json',
        img_prefix='val_images',
        pipeline=test_pipeline,
        data_root='/content/drive/MyDrive/data_2_classes/size_256/images',
        classes=('normal', 'cancer')))
evaluation = dict(interval=1, metric='bbox')
optimizer = dict(type='SGD', lr=0.0025, momentum=0.9, weight_decay=0.0001)
optimizer_config = dict(grad_clip=None)
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=1000,
    warmup_ratio=0.001,
    step=[8, 11])
runner = dict(type='EpochBasedRunner', max_epochs=10)
checkpoint_config = dict(interval=1)
log_config = dict(
    interval=200,
    hooks=[
        dict(type='TextLoggerHook'),
        dict(
            type='MMDetWandbHook',
            init_kwargs=dict(
                project='CancerDetection',
                entity='thesisltran',
                name='RetinaNet_2_256',
                id='RetinaNet_2_256',
                notes='retinanet_x101_64x4d_fpn_1x_coco',
                save_code=True,
            tags=["2", "256", "RetinaNet"]
            ),
            interval=10,
            log_checkpoint=True,
            log_checkpoint_metadata=True,
            num_eval_images=50)
    ])
custom_hooks = [dict(type='NumClassCheckHook')]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = '/content/drive/MyDrive/checkpoints/retinanet_x101_64x4d_fpn_1x_coco.pth'
resume_from = None
workflow = [('train', 1)]
opencv_num_threads = 0
mp_start_method = 'fork'
auto_scale_lr = dict(enable=False, base_batch_size=16)
classes = ('normal', 'cancer')
work_dir = './tutorial_exps'
seed = 0
gpu_ids = range(0, 1)
device = 'cuda'