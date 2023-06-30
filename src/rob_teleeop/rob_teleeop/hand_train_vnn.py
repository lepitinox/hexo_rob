import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
import rclpy




def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('hand_inf')
    rclpy.spin(node)
    share_path = Path(get_package_share_directory('rob_teleeop'))

    train_df = pd.read_csv(share_path/'sign_mnist_train.csv')
    test_df = pd.read_csv(share_path/'sign_mnist_test.csv')


    X_train = np.array(train_df.iloc[:, 1:]).reshape(-1, 28, 28, 1)
    y_train = np.array(train_df.iloc[:, 0])

    X_test = np.array(test_df.iloc[:, 1:]).reshape(-1, 28, 28, 1)
    y_test = np.array(test_df.iloc[:, 0])

    input_shape = (28, 28, 1)

    model = keras.Sequential()
    model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))

    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))

    early_stop = EarlyStopping(monitor='val_loss',patience=2)

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(x=X_train, y=y_train, validation_data=(X_test, y_test),epochs=25, callbacks=[early_stop])

    model.save(share_path/'hand_sign_model.h5')

    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
