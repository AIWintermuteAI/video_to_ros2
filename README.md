# video_to_ros2
Allows publishing video files to ros2 nodes, as well as previewing sensor_msgs/Image nodes.
Contains two nodes, video_publisher and video_preview.
Works with ROS 2 Jazzy.

## Requirements
The node requires ROS2, OpenCV as well as cv_bridge installed.

## video_publisher
Lets you push a file as a camera feed to ROS2. Also works with images, outputting them with 60 fps.
Parameters:
- publish_topic - Name of topic node publishes to (string)
  - default: "/camera/image_raw"
- video_file - Path to video or image to publish
  - default: "videos/video.mp4"
- loop - Rewind and replay video when it reaches the end (bool)
  - default: True

```
ros2 run video_to_ros2 video_publisher --ros-args --param loop:=true --param video_file:=videos/short_video.mp4
```

## video_preview
Lets you preview video form a camera feed in ROS2.
Parameters:
- itopic_video - Name of topic node subscribes to (string)
  - default: "/video"
