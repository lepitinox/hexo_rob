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
        self.model = keras.models.load_model(self.share_path/'hand_sign_model.h5')
        # subscribe to the hand image topic
        self.hand_sub = self.create_subscription(Image, 'hand_image', self.hand_callback, 10)

    
    def hand_callback(self, msg):
        # convert the image to a numpy array
        img = np.array(msg.data)
        # reshape the image to the correct shape
        img = img.reshape(-1, 28, 28, 1)
        # do the prediction
        pred = self.model.predict(img)
        # get the predicted class
        pred_class = np.argmax(pred)
        # print the predicted class
        print(pred_class)

if __name__ == '__main__':
    # create the node
    rclpy.init()
    node = HandInf()
    # spin the node
    rclpy.spin()
    # destroy the node
    rclpy.shutdown()