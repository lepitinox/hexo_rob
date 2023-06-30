# class to do ther inferece using the hand model
# imports 

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from sensor_msgs.msg import Image
import rclpy
import cv2


class HandInf(Node):
    share_path = Path(get_package_share_directory('rob_teleeop'))

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')
        self.model = keras.models.load_model(self.share_path/'hand_sign_model.h5')
        # subscribe to the hand image topic
        self.hand_sub = self.create_subscription(Image, 'hand_image', self.hand_callback, 10)

        self.mat = None
        rclpy.spin(self)

    
    def hand_callback(self, msg):
        # convert the image to a numpy array
        img = np.array(msg.data)
        # log the shape of the image
        # crop the image
        img = img.reshape(480, 640, 3)
        img = img[0:480, 80:560]
        # resize the image to 28x28x1
        img = tf.image.resize(img, [28, 28])
        # convert the image to grayscale
        img = tf.image.rgb_to_grayscale(img)
        # log the shape of the image
        # convert the image to a numpy array
        img = np.array(img)
        # log the shape of the image
        # reshape the image to 1x28x28x1
        img = img.reshape(1, 28, 28, 1)
        # log the shape of the image

        # do the prediction
        pred = self.model.predict(img)
        # get the predicted class
        pred_class = np.argmax(pred)
        # print the predicted class
        print(pred_class)
        # log the predicted class
        self.get_logger().info(f'Predicted class: {pred_class}')
        sz = (msg.height, msg.width)
        # print(msg.header.stamp)
        if False:
            print('{encoding} {width} {height} {step} {data_size}'.format(
                encoding=msg.encoding, width=msg.width, height=msg.height,
                step=msg.step, data_size=len(msg.data)))
        if msg.step * msg.height != len(msg.data):
            print('bad step/height/data size')
            return

        if msg.encoding == 'rgb8':
            dirty = (self.mat is None or msg.width != self.mat.shape[1] or
                     msg.height != self.mat.shape[0] or len(self.mat.shape) < 2 or
                     self.mat.shape[2] != 3)
            if dirty:
                self.mat = np.zeros([msg.height, msg.width, 3], dtype=np.uint8)
            self.mat[:, :, 2] = np.array(msg.data[0::3]).reshape(sz)
            self.mat[:, :, 1] = np.array(msg.data[1::3]).reshape(sz)
            self.mat[:, :, 0] = np.array(msg.data[2::3]).reshape(sz)
        elif msg.encoding == 'mono8':
            self.mat = np.array(msg.data).reshape(sz)
        else:
            print('unsupported encoding {}'.format(msg.encoding))
            return
        if self.mat is not None:
            cv2.imshow('image', img/255.0)
            cv2.waitKey(5)



def main():
    node = HandInf()

if __name__ == '__main__':
    main()