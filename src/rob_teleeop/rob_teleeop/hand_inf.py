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


class HandInf(Node):
    share_path = Path(get_package_share_directory('rob_teleeop'))

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')
        self.model = keras.models.load_model(self.share_path/'hand_sign_model.h5')
        # subscribe to the hand image topic
        self.hand_sub = self.create_subscription(Image, 'hand_image', self.hand_callback, 10)

        rclpy.spin(self)

    
    def hand_callback(self, msg):
        # convert the image to a numpy array
        img = np.array(msg.data)
        # log the shape of the image
        self.get_logger().info(f"Image shape: {img.shape}")
        # crop the image
        img = img.reshape(480, 640, 3)
        img = img[0:480, 80:560]
        # resize the image to 28x28x1
        img = tf.image.resize(img, [28, 28])
        self.get_logger().info(f"Image shape2: {img.shape}")
        # convert the image to grayscale
        img = tf.image.rgb_to_grayscale(img)
        # log the shape of the image
        self.get_logger().info(f"Image shape3: {img.shape}")
        # do the prediction
        pred = self.model.predict(img)
        # get the predicted class
        pred_class = np.argmax(pred)
        # print the predicted class
        print(pred_class)

def main():
    node = HandInf()

if __name__ == '__main__':
    main()