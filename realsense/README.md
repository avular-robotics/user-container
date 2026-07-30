# RealSense ROS 2 container for the Vertex

This is the `realsense_ros` container, nested inside the [realsense add-on user container](../README.md). It builds [librealsense](https://github.com/realsenseai/librealsense) and the [RealSense ROS 2 wrapper](https://github.com/realsenseai/realsense-ros) from source, providing the RealSense ROS 2 API (camera/depth/pointcloud topics, `rs-enumerate-devices`, etc.) that the outer container doesn't include.

## Setting up the realsense_ros container

This directory is part of the same checkout as the outer container. If `/data/user/add-on/realsense` is already set up (see the [main README](../README.md#setting-up-the-realsense-container)):

```bash
cd /data/user/add-on/realsense/realsense
```

### Building

```bash
docker compose build
```

## Using the realsense_ros container

By default the container runs `sleep infinity` and does not launch the camera. To launch it automatically on container start, uncomment the `command:` line in [docker-compose.yml](docker-compose.yml), then bring it up:

```bash
docker compose up -d realsense_ros
```

Alternatively, start the node manually inside the running container:

```bash
docker exec -it realsense_ros bash -lc "source /home/user/ws/install/setup.bash && ros2 launch realsense2_camera rs_launch.py config_file:=/pointcloud_params.yaml"
```

Once the node is running it publishes camera and pointcloud data.

### Verifying the RealSense ROS 2 API is working

```bash
docker exec -it realsense_ros bash
rs-enumerate-devices
```

This should list your RealSense device (e.g. `Intel RealSense D435I`). If not, see [Troubleshooting](#troubleshooting).

Check the ROS 2 topics are publishing:

```bash
ros2 topic list | grep camera
ros2 topic hz /camera/camera/color/image_raw
```

See the [RealSense ROS 2 wrapper](https://github.com/realsenseai/realsense-ros) docs for more.

## Troubleshooting

### rs-enumerate-devices: No device detected. Is it plugged in?
Confirm the camera is visible to the host: `lsusb | grep -i intel`. If that's empty, it's a hardware/connection issue, not this container. (Older librealsense versions refused to report a D435i at all without a working motion module — fixed by the v2.56.3 pin already in this Dockerfile.)

### Gyro/accel (IMU) topics don't appear
Expected on this Vertex — the kernel is missing `CONFIG_HID_SENSOR_ACCEL_3D`/`CONFIG_HID_SENSOR_GYRO_3D`, so `/dev/iio:device*` never appears. Video/depth/pointcloud are unaffected. Needs a base OS update from Avular; nothing in this container can work around a missing kernel module.

### Pointcloud has no color, depth-to-color alignment isn't published
Both off by default: `stream_filter` (texture source) is `0` not `2`, and `align_depth.enable` is `false`. Change either in [pointcloud_params.yaml](pointcloud_params.yaml).

Pointcloud settings go through `pointcloud_params.yaml`, not a `pointcloud.*` launch arg — on this ARM64/NEON build librealsense names the filter's parameter `pointcloud__neon_.*`, not `pointcloud.*`, so `rs_launch.py`'s own `pointcloud.enable` argument silently does nothing.

### Build fails while building `ros_base`
Verify the `ros_base` service's build context in [docker-compose.yml](docker-compose.yml) is `context: ..` — it needs `entrypoint.sh`, which lives one level up.
