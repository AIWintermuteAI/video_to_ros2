import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class VideoPublisher(Node):
    def __init__(self):
        super().__init__(node_name="video_publisher")
        # TODO - change parameters
        self.declare_parameter("publish_topic", "/camera/image_raw")
        self.publish_topic = self.get_parameter("publish_topic").value
        self.declare_parameter("loop", True)
        self.loop = self.get_parameter("loop").value
        self.get_logger().info(f"Publishing video to topic {self.publish_topic}, loop={self.loop}")

        self.cv_bridge = CvBridge()

        self.frame_publisher = self.create_publisher(
            Image,
            self.publish_topic,
            0
        )

        self.declare_parameter("video_file", "videos/video.mp4")
        self.video_file = self.get_parameter("video_file").value

        picture_format_tuples = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")

        if self.video_file.endswith(picture_format_tuples):
            self.load_image()
        else:
            self.load_video()

    def publish_frames(self, opencv_img):
        img_msg: Image = self.cv_bridge.cv2_to_imgmsg(opencv_img, encoding="passthrough")

        self.frame_publisher.publish(img_msg)


    def load_image(self):
        img = cv2.imread(self.video_file)

        sleep_time = (1.0/60.0)

        while True:
            self.publish_frames(img)
            time.sleep(sleep_time)


    def load_video(self):
        capture = cv2.VideoCapture(self.video_file)

        if not capture.isOpened():
            self.get_logger().error("Failed to open video file...")
            return

        video_fps = capture.get(cv2.CAP_PROP_FPS)

        video_frame_time = (1.0 / video_fps) * 1000.0
        self.get_logger().info(f"Using video fps {video_fps}, frametime {video_frame_time}")

        while capture.isOpened():

            next_frame = time.time() + video_frame_time

            ret, frame = capture.read()
            if not ret:
                if self.loop:
                    self.get_logger().info("Video finished, rewinding...")
                    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    self.get_logger().info("Video finished.")
                    break

            self.publish_frames(frame)

            curr_time = time.time()

            # Wait if still not time for next frame
            if curr_time < next_frame:
                wait_time = next_frame - curr_time
                # self.get_logger().info(f"Loading took less time than expected. Waiting {wait_time} ms")
                time.sleep(1.0/wait_time)

        capture.release()


def main(args=None):
    rclpy.init(args=args)
    reciever = VideoPublisher()
    rclpy.spin(reciever)
    reciever.destroy_node()
    rclpy.shutdown()
