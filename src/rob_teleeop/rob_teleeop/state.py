from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped


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
    def __init__(self, config) -> None:
        pass


class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        degree = pi / 180.0
        loop_rate = self.create_rate(30)

        joint_state = JointState()
        a = 0

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                # update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['handle_joint']
                joint_state.position = [0.0]
                for i in range(1, 6):
                    for j in range(1, 5):
                        joint_state.name.append('finger{}_joint{}'.format(i, j))
                        joint_state.position.append(0.0)


                self.joint_pub.publish(joint_state)
                loop_rate.sleep()

        except KeyboardInterrupt:
            pass

def main():
    node = StatePublisher()

if __name__ == '__main__':
    main()