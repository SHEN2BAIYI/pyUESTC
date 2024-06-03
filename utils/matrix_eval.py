import torch
import numpy as np

"""
    PA, cPA, IoU, mIoU - Evaluation Parameters
"""


class SegmentationMatrix:
    def __init__(self, num_classes):
        self.num_classes = num_classes

        # Create empty confusion matrix (According to the num of class)
        self.confusion_matrix = np.zeros((self.num_classes, ) * 2)

    def gen_confusion_matrix(self, my_predict, my_label, ignore_labels):
        # To numpy
        img_predict = my_predict
        if my_predict.shape != my_label.shape:
            img_predict = torch.argmax(my_predict, dim=1)
        img_predict = img_predict if type(img_predict) == np.ndarray else img_predict.numpy()
        img_label = my_label if type(my_label) == np.ndarray or type(my_label) == np.memmap else my_label.numpy()

        # Remove classes from unlabeled pixels in gt and pre
        mask = (img_label >= 0) & (img_label < self.num_classes)
        for ignore_label in ignore_labels:
            mask &= (img_label != ignore_label)

        # Count for confusion matrix: nx0+0, nx0+1, ..., nx0+n-1, ..., nx(n-1)+n-1
        label = (self.num_classes * (img_label[mask]) + img_predict[mask]).astype(np.int64)
        count = np.bincount(label, minlength=self.num_classes**2)
        confusion_matrix = np.reshape(count, [self.num_classes, self.num_classes])
        return confusion_matrix

    def add_batch(self, img_predict, img_label, ignore_labels):
        self.confusion_matrix += self.gen_confusion_matrix(img_predict, img_label, ignore_labels)

        return self.confusion_matrix

    def reset(self):
        self.confusion_matrix = np.zeros((self.num_classes, ) * 2)

    def pixel_accuracy(self):
        """
            Return all class overall pixel accuracy.
            PA = acc = (TP + TN) / (TP + TN + FP + FN)
        """
        acc = np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum()
        return acc

    def class_pixel_accuracy(self):
        """
            Return each category pixel accuracy.
            acc = TP / (TP + FP)
        """
        class_acc = np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=1)
        return class_acc

    def inter_over_union(self):
        """
            Compute the intersection over union.
            IoU = TP / (TP + FP + FN)
        """
        intersection = np.diag(self.confusion_matrix)
        union = np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) - intersection
        IoU = intersection / union
        return IoU

    def mean_inter_over_union(self):
        IoU = self.inter_over_union()
        mIoU = IoU[IoU < float('inf')].mean()
        return mIoU

    def dice_coefficient(self):
        """
            Compute the Dice Coefficient.
            Dice = 2TP / (2TP + FP + FN)
        """
        intersection = 2 * np.diag(self.confusion_matrix)

        # axis=1: TP + FP   axis=0: TP + FN
        tp_fn = np.sum(self.confusion_matrix, axis=0)
        tp_fp = np.sum(self.confusion_matrix, axis=1)
        union = tp_fp + tp_fn
        # union = np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0)

        dice = intersection / union

        # remove the value when TP + FP = 0 (This batch didn't contain this class)
        mask = (tp_fp == 0)
        dice[mask] = -1

        return dice

    def mean_dice(self):
        dice = self.dice_coefficient()
        mDice = dice[(dice < float('inf')) & (dice != -1)].mean()
        return mDice

    def acc(self):
        diag = np.sum(np.diag(self.confusion_matrix))
        total = np.sum(self.confusion_matrix)
        return diag / total





