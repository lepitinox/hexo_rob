from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped
from std_msgs.msg import Int32
INIT = [[0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]]
TO_POSITION_CLASS = {
0: [[0.0],[0.0, 1.57, 1.57, 1.57],[0.0, 1.57, 1.57, 1.57],[0.0, 1.57, 1.57, 1.57],[0.0, 1.57, 1.57, 1.57],[0.0, 0.0, 1.57, 1.57]],
1: [[0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 1.57, 1.57]],
2: [[0.0],[0.0, 0.57, 0.57, 0.57],[0.0, 0.57, 0.57, 0.57],[0.0, 0.57, 0.57, 0.57],[0.0, 0.57, 0.57, 0.57],[0.5, 0.57, 0.57, 0.57],[0.0, 0.57, 0.57, 0.57]],
}

class UpdateHand:
    """
    config = {
        "finger1_joint1": 0.0,
        "finger1_joint2": 0.0,
        "finger1_joint3": 0.0,
        "finger1_joint4": 0.0,
        "finger2_joint1": 0.0,
        ...
    """
    def __init__(self, publisher) -> None:
        self._publisher = publisher
        self._joint_state = JointState()


    def move_to_class(self, class_nb,now):
        try:
            self.move_to(TO_POSITION_CLASS[int(class_nb)],now)
        except Exception as e:
            pass
    
    def move_to(self, config,now):
        self._joint_state = JointState()
        self._joint_state.header.stamp = now.to_msg()
        self._joint_state.name = [
            "handle_joint",
            "finger1_joint1",
            "finger1_joint2",
            "finger1_joint3",
            "finger1_joint4",
            "finger2_joint1",
            "finger2_joint2",
            "finger2_joint3",
            "finger2_joint4",
            "finger3_joint1",
            "finger3_joint2",
            "finger3_joint3",
            "finger3_joint4",
            "finger4_joint1",
            "finger4_joint2",
            "finger4_joint3",
            "finger4_joint4",
            "finger5_joint1",
            "finger5_joint2",
            "finger5_joint3",
            "finger5_joint4"
        ]
        oklol = []
        for i in config:
            oklol+=i
        self._joint_state.position = oklol
        self._publisher.publish(self._joint_state)


class StatePublisher(Node):

    def __init__(self):

        super().__init__('state_publisher')
        qos_profile = QoSProfile(depth=200)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))
        self.sub = self.create_subscription(Int32, 'hand_class', self.joint_callback, qos_profile)
        self.oklol = UpdateHand(self.joint_pub)
        now = self.get_clock().now()
        self.oklol.move_to(INIT, now)

    def joint_callback(self, msg):
        now = self.get_clock().now()
        class_nb = msg.data
        self.oklol.move_to_class(class_nb, now)


def main():
    rclpy.init()
    node = StatePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()