FROM ros-humble-base

USER root

# Fix permissions
RUN chown -R user:user /home/user

# Install system deps and librealsense2 from source
RUN apt-get update && apt-get install --no-install-recommends -y \
    libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev \
    libgl1-mesa-dev libglu1-mesa-dev cmake git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/librealsense

RUN git clone --depth 1 --branch v2.56.3 https://github.com/realsenseai/librealsense.git librealsense

WORKDIR /tmp/librealsense/librealsense/build

RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=OFF && \
    make -j"$(nproc)" && make install && ldconfig

# Install ROS 2 deps for the wrapper
RUN apt-get update --allow-insecure-repositories && apt-get install --no-install-recommends -y \
    ros-humble-diagnostic-updater \
    ros-humble-image-transport \
    ros-humble-tf2-ros \
    ros-humble-pcl-conversions \
    ros-humble-pcl-ros \
    ros-humble-cv-bridge \
    ros-humble-rclcpp-action \
    ros-humble-std-srvs && \
    rm -rf /var/lib/apt/lists/*

# Clone the ROS wrapper
# Note the Realsense wrapper version should be compatible with the librealsense version (ending to the same version nubmer)
WORKDIR /home/user/ws/src
RUN git clone https://github.com/realsenseai/realsense-ros.git -b 4.56.3

# Build
WORKDIR /home/user/ws
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build --symlink-install && \
    echo "source /home/user/ws/install/setup.bash" >> ~/.bashrc

COPY pointcloud_params.yaml /pointcloud_params.yaml

USER user
WORKDIR /home/user/ws
CMD ["/bin/bash"]
