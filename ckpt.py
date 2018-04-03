import os
import argparse
import torch
from helper import config, load_ckpt, save_ckpt

camunet_mapping = {
    'c1.conv1.weight' : 'c1.block1.conv.weight',
    'c1.conv1.bias' : 'c1.block1.conv.bias',
    'c1.norm1.weight' : 'c1.block1.norm.weight',
    'c1.norm1.bias': 'c1.block1.norm.bias',
    'c1.norm1.running_mean' : 'c1.block1.norm.running_mean',
    'c1.norm1.running_var' : 'c1.block1.norm.running_var',
    'c1.conv2.weight' : 'c1.block2.conv.weight',
    'c1.conv2.bias' : 'c1.block2.conv.bias',
    'c1.norm2.weight' : 'c1.block2.norm.weight',
    'c1.norm2.bias' : 'c1.block2.norm.bias',
    'c1.norm2.running_mean' : 'c1.block2.norm.running_mean',
    'c1.norm2.running_var' : 'c1.block2.norm.running_var',
    'c2.conv1.weight' : 'c2.block1.conv.weight',
    'c2.conv1.bias' : 'c2.block1.conv.bias',
    'c2.norm1.weight' : 'c2.block1.norm.weight',
    'c2.norm1.bias': 'c2.block1.norm.bias',
    'c2.norm1.running_mean' : 'c2.block1.norm.running_mean',
    'c2.norm1.running_var' : 'c2.block1.norm.running_var',
    'c2.conv2.weight' : 'c2.block2.conv.weight',
    'c2.conv2.bias' : 'c2.block2.conv.bias',
    'c2.norm2.weight' : 'c2.block2.norm.weight',
    'c2.norm2.bias' : 'c2.block2.norm.bias',
    'c2.norm2.running_mean' : 'c2.block2.norm.running_mean',
    'c2.norm2.running_var' : 'c2.block2.norm.running_var',
    'c3.conv1.weight' : 'c3.block1.conv.weight',
    'c3.conv1.bias' : 'c3.block1.conv.bias',
    'c3.norm1.weight' : 'c3.block1.norm.weight',
    'c3.norm1.bias': 'c3.block1.norm.bias',
    'c3.norm1.running_mean' : 'c3.block1.norm.running_mean',
    'c3.norm1.running_var' : 'c3.block1.norm.running_var',
    'c3.conv2.weight' : 'c3.block2.conv.weight',
    'c3.conv2.bias' : 'c3.block2.conv.bias',
    'c3.norm2.weight' : 'c3.block2.norm.weight',
    'c3.norm2.bias' : 'c3.block2.norm.bias',
    'c3.norm2.running_mean' : 'c3.block2.norm.running_mean',
    'c3.norm2.running_var' : 'c3.block2.norm.running_var',
    'c4.conv1.weight' : 'c4.block1.conv.weight',
    'c4.conv1.bias' : 'c4.block1.conv.bias',
    'c4.norm1.weight' : 'c4.block1.norm.weight',
    'c4.norm1.bias': 'c4.block1.norm.bias',
    'c4.norm1.running_mean' : 'c4.block1.norm.running_mean',
    'c4.norm1.running_var' : 'c4.block1.norm.running_var',
    'c4.conv2.weight' : 'c4.block2.conv.weight',
    'c4.conv2.bias' : 'c4.block2.conv.bias',
    'c4.norm2.weight' : 'c4.block2.norm.weight',
    'c4.norm2.bias' : 'c4.block2.norm.bias',
    'c4.norm2.running_mean' : 'c4.block2.norm.running_mean',
    'c4.norm2.running_var' : 'c4.block2.norm.running_var',
    'cu.conv1.weight' : 'cu.block1.conv.weight',
    'cu.conv1.bias' : 'cu.block1.conv.bias',
    'cu.norm1.weight' : 'cu.block1.norm.weight',
    'cu.norm1.bias' : 'cu.block1.norm.bias',
    'cu.norm1.running_mean' : 'cu.block1.norm.running_mean',
    'cu.norm1.running_var' : 'cu.block1.norm.running_var',
    'cu.conv2.weight' : 'cu.block2.conv.weight',
    'cu.conv2.bias' : 'cu.block2.conv.bias',
    'cu.norm2.weight' : 'cu.block2.norm.weight',
    'cu.norm2.bias' : 'cu.block2.norm.bias',
    'cu.norm2.running_mean' : 'cu.block2.norm.running_mean',
    'cu.norm2.running_var' : 'cu.block2.norm.running_var',
    'u5s.up.weight' : 'u5s.up.weight',
    'u5s.up.bias' : 'u5s.up.bias',
    'u5s.conv1.weight' : 'u5s.block1.conv.weight',
    'u5s.conv1.bias' : 'u5s.block1.conv.bias',
    'u5s.norm1.weight' : 'u5s.block1.norm.weight',
    'u5s.norm1.bias' : 'u5s.block1.norm.bias',
    'u5s.norm1.running_mean' : 'u5s.block1.norm.running_mean',
    'u5s.norm1.running_var' : 'u5s.block1.norm.running_var',
    'u5s.conv2.weight' : 'u5s.block2.conv.weight',
    'u5s.conv2.bias' : 'u5s.block2.conv.bias',
    'u5s.norm2.weight' : 'u5s.block2.norm.weight',
    'u5s.norm2.bias' : 'u5s.block2.norm.bias',
    'u5s.norm2.running_mean' : 'u5s.block2.norm.running_mean',
    'u5s.norm2.running_var' : 'u5s.block2.norm.running_var',
    'u6s.up.weight' : 'u6s.up.weight',
    'u6s.up.bias' : 'u6s.up.bias',
    'u6s.conv1.weight' : 'u6s.block1.conv.weight',
    'u6s.conv1.bias' : 'u6s.block1.conv.bias',
    'u6s.norm1.weight' : 'u6s.block1.norm.weight',
    'u6s.norm1.bias' : 'u6s.block1.norm.bias',
    'u6s.norm1.running_mean' : 'u6s.block1.norm.running_mean',
    'u6s.norm1.running_var' : 'u6s.block1.norm.running_var',
    'u6s.conv2.weight' : 'u6s.block2.conv.weight',
    'u6s.conv2.bias' : 'u6s.block2.conv.bias',
    'u6s.norm2.weight' : 'u6s.block2.norm.weight',
    'u6s.norm2.bias' : 'u6s.block2.norm.bias',
    'u6s.norm2.running_mean' : 'u6s.block2.norm.running_mean',
    'u6s.norm2.running_var' : 'u6s.block2.norm.running_var',
    'u7s.up.weight' : 'u7s.up.weight',
    'u7s.up.bias' : 'u7s.up.bias',
    'u7s.conv1.weight' : 'u7s.block1.conv.weight',
    'u7s.conv1.bias' : 'u7s.block1.conv.bias',
    'u7s.norm1.weight' : 'u7s.block1.norm.weight',
    'u7s.norm1.bias' : 'u7s.block1.norm.bias',
    'u7s.norm1.running_mean' : 'u7s.block1.norm.running_mean',
    'u7s.norm1.running_var' : 'u7s.block1.norm.running_var',
    'u7s.conv2.weight' : 'u7s.block2.conv.weight',
    'u7s.conv2.bias' : 'u7s.block2.conv.bias',
    'u7s.norm2.weight' : 'u7s.block2.norm.weight',
    'u7s.norm2.bias' : 'u7s.block2.norm.bias',
    'u7s.norm2.running_mean' : 'u7s.block2.norm.running_mean',
    'u7s.norm2.running_var' : 'u7s.block2.norm.running_var',
    'u8s.up.weight' : 'u8s.up.weight',
    'u8s.up.bias' : 'u8s.up.bias',
    'u8s.conv1.weight' : 'u8s.block1.conv.weight',
    'u8s.conv1.bias' : 'u8s.block1.conv.bias',
    'u8s.norm1.weight' : 'u8s.block1.norm.weight',
    'u8s.norm1.bias' : 'u8s.block1.norm.bias',
    'u8s.norm1.running_mean' : 'u8s.block1.norm.running_mean',
    'u8s.norm1.running_var' : 'u8s.block1.norm.running_var',
    'u8s.conv2.weight' : 'u8s.block2.conv.weight',
    'u8s.conv2.bias' : 'u8s.block2.conv.bias',
    'u8s.norm2.weight' : 'u8s.block2.norm.weight',
    'u8s.norm2.bias' : 'u8s.block2.norm.bias',
    'u8s.norm2.running_mean' : 'u8s.block2.norm.running_mean',
    'u8s.norm2.running_var' : 'u8s.block2.norm.running_var',
    'ces.weight' : 'ces.weight',
    'ces.bias' : 'ces.bias',
    'u5c.up.weight' : 'u5c.up.weight',
    'u5c.up.bias' : 'u5c.up.bias',
    'u5c.conv1.weight' : 'u5c.block1.conv.weight',
    'u5c.conv1.bias' : 'u5c.block1.conv.bias',
    'u5c.norm1.weight' : 'u5c.block1.norm.weight',
    'u5c.norm1.bias' : 'u5c.block1.norm.bias',
    'u5c.norm1.running_mean' : 'u5c.block1.norm.running_mean',
    'u5c.norm1.running_var' : 'u5c.block1.norm.running_var',
    'u5c.conv2.weight' : 'u5c.block2.conv.weight',
    'u5c.conv2.bias' : 'u5c.block2.conv.bias',
    'u5c.norm2.weight' : 'u5c.block2.norm.weight',
    'u5c.norm2.bias' : 'u5c.block2.norm.bias',
    'u5c.norm2.running_mean' : 'u5c.block2.norm.running_mean',
    'u5c.norm2.running_var' : 'u5c.block2.norm.running_var',
    'u6c.up.weight' : 'u6c.up.weight',
    'u6c.up.bias' : 'u6c.up.bias',
    'u6c.conv1.weight' : 'u6c.block1.conv.weight',
    'u6c.conv1.bias' : 'u6c.block1.conv.bias',
    'u6c.norm1.weight' : 'u6c.block1.norm.weight',
    'u6c.norm1.bias' : 'u6c.block1.norm.bias',
    'u6c.norm1.running_mean' : 'u6c.block1.norm.running_mean',
    'u6c.norm1.running_var' : 'u6c.block1.norm.running_var',
    'u6c.conv2.weight' : 'u6c.block2.conv.weight',
    'u6c.conv2.bias' : 'u6c.block2.conv.bias',
    'u6c.norm2.weight' : 'u6c.block2.norm.weight',
    'u6c.norm2.bias' : 'u6c.block2.norm.bias',
    'u6c.norm2.running_mean' : 'u6c.block2.norm.running_mean',
    'u6c.norm2.running_var' : 'u6c.block2.norm.running_var',
    'u7c.up.weight' : 'u7c.up.weight',
    'u7c.up.bias' : 'u7c.up.bias',
    'u7c.conv1.weight' : 'u7c.block1.conv.weight',
    'u7c.conv1.bias' : 'u7c.block1.conv.bias',
    'u7c.norm1.weight' : 'u7c.block1.norm.weight',
    'u7c.norm1.bias' : 'u7c.block1.norm.bias',
    'u7c.norm1.running_mean' : 'u7c.block1.norm.running_mean',
    'u7c.norm1.running_var' : 'u7c.block1.norm.running_var',
    'u7c.conv2.weight' : 'u7c.block2.conv.weight',
    'u7c.conv2.bias' : 'u7c.block2.conv.bias',
    'u7c.norm2.weight' : 'u7c.block2.norm.weight',
    'u7c.norm2.bias' : 'u7c.block2.norm.bias',
    'u7c.norm2.running_mean' : 'u7c.block2.norm.running_mean',
    'u7c.norm2.running_var' : 'u7c.block2.norm.running_var',
    'u8c.up.weight' : 'u8c.up.weight',
    'u8c.up.bias' : 'u8c.up.bias',
    'u8c.conv1.weight' : 'u8c.block1.conv.weight',
    'u8c.conv1.bias' : 'u8c.block1.conv.bias',
    'u8c.norm1.weight' : 'u8c.block1.norm.weight',
    'u8c.norm1.bias' : 'u8c.block1.norm.bias',
    'u8c.norm1.running_mean' : 'u8c.block1.norm.running_mean',
    'u8c.norm1.running_var' : 'u8c.block1.norm.running_var',
    'u8c.conv2.weight' : 'u8c.block2.conv.weight',
    'u8c.conv2.bias' : 'u8c.block2.conv.bias',
    'u8c.norm2.weight' : 'u8c.block2.norm.weight',
    'u8c.norm2.bias' : 'u8c.block2.norm.bias',
    'u8c.norm2.running_mean' : 'u8c.block2.norm.running_mean',
    'u8c.norm2.running_var' : 'u8c.block2.norm.running_var',
    'cec.weight' : 'cec.weight',
    'cec.bias' : 'cec.bias',

    'u5m.up.weight' : 'u5m.up.weight',
    'u5m.up.bias' : 'u5m.up.bias',
    'u5m.conv1.weight' : 'u5m.block1.conv.weight',
    'u5m.conv1.bias' : 'u5m.block1.conv.bias',
    'u5m.norm1.weight' : 'u5m.block1.norm.weight',
    'u5m.norm1.bias' : 'u5m.block1.norm.bias',
    'u5m.norm1.running_mean' : 'u5m.block1.norm.running_mean',
    'u5m.norm1.running_var' : 'u5m.block1.norm.running_var',
    'u5m.conv2.weight' : 'u5m.block2.conv.weight',
    'u5m.conv2.bias' : 'u5m.block2.conv.bias',
    'u5m.norm2.weight' : 'u5m.block2.norm.weight',
    'u5m.norm2.bias' : 'u5m.block2.norm.bias',
    'u5m.norm2.running_mean' : 'u5m.block2.norm.running_mean',
    'u5m.norm2.running_var' : 'u5m.block2.norm.running_var',
    'u6m.up.weight' : 'u6m.up.weight',
    'u6m.up.bias' : 'u6m.up.bias',
    'u6m.conv1.weight' : 'u6m.block1.conv.weight',
    'u6m.conv1.bias' : 'u6m.block1.conv.bias',
    'u6m.norm1.weight' : 'u6m.block1.norm.weight',
    'u6m.norm1.bias' : 'u6m.block1.norm.bias',
    'u6m.norm1.running_mean' : 'u6m.block1.norm.running_mean',
    'u6m.norm1.running_var' : 'u6m.block1.norm.running_var',
    'u6m.conv2.weight' : 'u6m.block2.conv.weight',
    'u6m.conv2.bias' : 'u6m.block2.conv.bias',
    'u6m.norm2.weight' : 'u6m.block2.norm.weight',
    'u6m.norm2.bias' : 'u6m.block2.norm.bias',
    'u6m.norm2.running_mean' : 'u6m.block2.norm.running_mean',
    'u6m.norm2.running_var' : 'u6m.block2.norm.running_var',
    'u7m.up.weight' : 'u7m.up.weight',
    'u7m.up.bias' : 'u7m.up.bias',
    'u7m.conv1.weight' : 'u7m.block1.conv.weight',
    'u7m.conv1.bias' : 'u7m.block1.conv.bias',
    'u7m.norm1.weight' : 'u7m.block1.norm.weight',
    'u7m.norm1.bias' : 'u7m.block1.norm.bias',
    'u7m.norm1.running_mean' : 'u7m.block1.norm.running_mean',
    'u7m.norm1.running_var' : 'u7m.block1.norm.running_var',
    'u7m.conv2.weight' : 'u7m.block2.conv.weight',
    'u7m.conv2.bias' : 'u7m.block2.conv.bias',
    'u7m.norm2.weight' : 'u7m.block2.norm.weight',
    'u7m.norm2.bias' : 'u7m.block2.norm.bias',
    'u7m.norm2.running_mean' : 'u7m.block2.norm.running_mean',
    'u7m.norm2.running_var' : 'u7m.block2.norm.running_var',
    'u8m.up.weight' : 'u8m.up.weight',
    'u8m.up.bias' : 'u8m.up.bias',
    'u8m.conv1.weight' : 'u8m.block1.conv.weight',
    'u8m.conv1.bias' : 'u8m.block1.conv.bias',
    'u8m.norm1.weight' : 'u8m.block1.norm.weight',
    'u8m.norm1.bias' : 'u8m.block1.norm.bias',
    'u8m.norm1.running_mean' : 'u8m.block1.norm.running_mean',
    'u8m.norm1.running_var' : 'u8m.block1.norm.running_var',
    'u8m.conv2.weight' : 'u8m.block2.conv.weight',
    'u8m.conv2.bias' : 'u8m.block2.conv.bias',
    'u8m.norm2.weight' : 'u8m.block2.norm.weight',
    'u8m.norm2.bias' : 'u8m.block2.norm.bias',
    'u8m.norm2.running_mean' : 'u8m.block2.norm.running_mean',
    'u8m.norm2.running_var' : 'u8m.block2.norm.running_var',
    'cem.weight' : 'cem.weight',
    'cem.bias' : 'cem.bias',
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ckpt', nargs='*', help='checkpoint filepath')
    parser.add_argument('--model', help='model name of checkpoint')
    parser.add_argument('--migrate', action='store_true', help='migrate checkpoint format')
    args = parser.parse_args()

    if args.model:
        model_name = args.model.lower()
    else:
        model_name = config['param']['model']

    for fn in args.ckpt:
        # load ckpt
        if torch.cuda.is_available():
            # Load all tensors onto previous state
            checkpoint = torch.load(fn)
        else:
            # Load all tensors onto the CPU
            checkpoint = torch.load(fn, map_location=lambda storage, loc: storage)

        if model_name == 'camunet' and args.migrate is True:
            for old_name, new_name in camunet_mapping.items():
                if old_name != new_name:
                    checkpoint['model'][new_name] = checkpoint['model'][old_name]
                    del checkpoint['model'][old_name]

        if 'name' in checkpoint:
            print("Model name {} has existed in checkpoint".format(checkpoint['name'], fn))
            continue

        checkpoint['name'] = model_name
        torch.save(checkpoint, fn)
        print("Model name {} has insert into checkpoint {}".format(model_name, fn))