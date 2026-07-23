# RealSense ROS 2 container for the Vertex

This is the `realsense_ros` container, nested inside the [realsense add-on user container](../README.md). It builds [librealsense](https://github.com/realsenseai/librealsense) and the [RealSense ROS 2 wrapper](https://github.com/realsenseai/realsense-ros) from source, providing the RealSense ROS 2 API (camera/depth/pointcloud topics, `rs-enumerate-devices`, etc.) that the outer container doesn't include.

## Setting up the realsense_ros container

This directory is part of the same checkout as the outer container. If `/data/user/add-on/realsense` is already set up (see the [main README](../README.md#setting-up-the-realsense-container)):

```bash
cd /data/user/add-on/realsense/realsense
```

### Building

`ros_base` must be built before `realsense_ros` — `docker compose build` doesn't order dependency builds:

```bash
docker compose build ros_base
docker compose build realsense_ros
```

## Using the realsense_ros container

The realsense_ros container starts publishing camera and pointcloud data as soon as the Realsense is connected. If you swap Realsense devices, restart the container.

```bash
docker compose up -d realsense_ros
```

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
Confirm the camera is visible to the host (via SSH, not inside a container): `lsusb | grep -i intel` should show the RealSense. If not, it's a hardware/connection issue.

If the host sees it but the container doesn't: this build uses librealsense's V4L2 backend (the recommended default), which needs the host kernel to carry RealSense's V4L2 metadata patches. If those aren't present on this Vertex's kernel, camera detection can fail this way — check with Avular whether the kernel has them. [librealsense's RSUSB backend](https://github.com/realsenseai/librealsense/blob/master/doc/installation_jetson.md) is a documented fallback for this case, but comes with real limitations (e.g. multi-camera support) and isn't enabled here.

### Build fails while building `ros_base`
Build `ros_base` before `realsense_ros` (see [Building](#building)). Verify the `ros_base` service's build context in [docker-compose.yml](docker-compose.yml) is `context: ..` — it needs `entrypoint.sh`, which lives one level up.
