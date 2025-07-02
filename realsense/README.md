# User realsense_ros container for the Vertex

The user realsense_ros container is an example container that can be used to develop on the Vertex. It comes pre-installed with ROS, LibRealsense and the Realsense ROS wrapper. It can be used as a starting point for using the Vertex Realsense Add-on.

This guide will walk you through how to use the user container to develop on the Vertex.

## Setting up the realsense_ros container

The user container is available on the Vertex by default at `/data/user/containers`. If you want to update the user container files, or restore the user container to its default state, you can follow these steps:

1. SSH into the Vertex
2. Remove the current user container files

    > [!WARNING]
    > This will remove all files in the user container directory. Make sure to back up any files you want to keep.

    ```bash
    rm -rf /data/user/containers
    ```

3. Clone the user container files to the Vertex

    ```bash
    git clone --branch vertex https://github.com/avular-robotics/user-container.git /data/user/containers
    ```

4. Building the user realsense_ros container

    ```bash
    cd /data/user/containers/realsense
    docker compose build
    ```

## Using the realsense_ros container

The realsense_ros container is configured to start publishing camera and pointcloud data as soon as the Realsense is connected. If you swap Realsense devices, you may need to restart the container.

More information on the usage of the [Intel Realsense ROS wrapper](https://github.com/IntelRealSense/realsense-ros) can be found here.