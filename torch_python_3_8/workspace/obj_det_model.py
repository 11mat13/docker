import sys
sys.path.append('./object-detection-with-spiking-neural-networks')
from object_detection_module import DetectionLitModule
import argparse
import cupy

from neurobench.models import SNNTorchModel
from neurobench.benchmarks import Benchmark
from neurobench.postprocessing.postprocessor import aggregate,choose_max_count


def main():
    parser = argparse.ArgumentParser(description='Classify event dataset')
    # Dataset
    parser.add_argument('-dataset', default='gen1', type=str, help='dataset used {GEN1}')
    parser.add_argument('-path', default='PropheseeGEN1', type=str, help='path to dataset location')
    parser.add_argument('-num_classes', default=2, type=int, help='number of classes')

    # Data
    parser.add_argument('-b', default=64, type=int, help='batch size')
    parser.add_argument('-sample_size', default=100000, type=int, help='duration of a sample in µs')
    parser.add_argument('-T', default=5, type=int, help='simulating time-steps')
    parser.add_argument('-tbin', default=2, type=int, help='number of micro time bins')
    parser.add_argument('-image_shape', default=(240,304), type=tuple, help='spatial resolution of events')

    # Training
    parser.add_argument('-epochs', default=50, type=int, help='number of total epochs to run')
    parser.add_argument('-lr', default=1e-3, type=float, help='learning rate used')
    parser.add_argument('-wd', default=1e-4, type=float, help='weight decay used')
    parser.add_argument('-num_workers', default=4, type=int, help='number of workers for dataloaders')
    parser.add_argument('-no_train', action='store_false', help='whether to train the model', dest='train')
    parser.add_argument('-test', action='store_true', help='whether to test the model')
    parser.add_argument('-device', default=0, type=int, help='device')
    parser.add_argument('-precision', default=16, type=int, help='whether to use AMP {16, 32, 64}')
    parser.add_argument('-save_ckpt', action='store_true', help='saves checkpoints')
    parser.add_argument('-comet_api', default=None, type=str, help='api key for Comet Logger')

    # Backbone
    parser.add_argument('-backbone', default='vgg-11', type=str, help='model used {squeezenet-v, vgg-v, mobilenet-v, densenet-v}', dest='model')
    parser.add_argument('-no_bn', action='store_false', help='don\'t use BatchNorm2d', dest='bn')
    parser.add_argument('-pretrained_backbone', default=None, type=str, help='path to pretrained backbone model')
    parser.add_argument('-pretrained', default=None, type=str, help='path to pretrained model')
    parser.add_argument('-extras', type=int, default=[640, 320, 320], nargs=4, help='number of channels for extra layers after the backbone')


    # Priors
    parser.add_argument('-min_ratio', default=0.05, type=float, help='min ratio for priors\' box generation')
    parser.add_argument('-max_ratio', default=0.80, type=float, help='max ratio for priors\' box generation')
    parser.add_argument('-aspect_ratios', default=[[2], [2, 3], [2, 3], [2, 3], [2], [2]], type=int, help='aspect ratios for priors\' box generation')

    # Loss parameters
    parser.add_argument('-box_coder_weights', default=[10.0, 10.0, 5.0, 5.0], type=float, nargs=4, help='weights for the BoxCoder class')
    parser.add_argument('-iou_threshold', default=0.50, type=float, help='intersection over union threshold for the SSDMatcher class')
    parser.add_argument('-score_thresh', default=0.01, type=float, help='score threshold used for postprocessing the detections')
    parser.add_argument('-nms_thresh', default=0.45, type=float, help='NMS threshold used for postprocessing the detections')
    parser.add_argument('-topk_candidates', default=200, type=int, help='number of best detections to keep before NMS')
    parser.add_argument('-detections_per_img', default=100, type=int, help='number of best detections to keep after NMS')

    args = parser.parse_args()

    module = DetectionLitModule(args)

    model = SNNTorchModel(module)

    # postprocessors
    # postprocessors = [choose_max_count]

    # static_metrics = ["footprint", "connection_sparsity"]
    # workload_metrics = ["synaptic_operations", "activation_sparsity", "classification_accuracy"]

    # benchmark = Benchmark(model, test_set_loader, [], postprocessors, [static_metrics, workload_metrics])
    # results = benchmark.run()
    # print(results)


if __name__ == '__main__':
    main()