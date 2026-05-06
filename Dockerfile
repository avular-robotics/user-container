FROM ros:humble

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qq -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libssl-dev \
    libusb-1.0-0-dev \
    pkg-config \
    libgtk-3-dev \
    libglfw3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    curl \
    wget \
    unzip \
    nano iproute2 vim htop \
    net-tools \
    python3 \
    python3-dev \
    python3-pip \
    ca-certificates \
    software-properties-common \
    python3-rosdep \
    ros-${ROS_DISTRO}-rviz2 \
    ros-${ROS_DISTRO}-rmw-cyclonedds-cpp \
    ros-${ROS_DISTRO}-nav-msgs \
    ros-${ROS_DISTRO}-nav2-msgs \
    bash-completion \
    # Creos dependencies
    nlohmann-json3-dev \
    && rm -rf /etc/apt/apt.conf.d/docker-clean \
    # Setup Rosdep
    && rm /etc/ros/rosdep/sources.list.d/20-default.list \
    && rosdep init \
    && rm -rf /var/lib/apt/lists/*


# Add user user and switch to home directory
RUN useradd --create-home --shell /bin/bash --groups sudo user \
    # Enable passwordless sudo
    && echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/90-user \
    # Show the container name in the terminal
    && echo 'export PS1="\[\033[01;32m\]\u@\h\[\033[01;33m\][user]\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$ "' >> /home/user/.bashrc 
USER user

# Setup ros
RUN source /opt/ros/${ROS_DISTRO}/setup.sh \
    && rosdep update \
    && echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

USER root

# Setup entrypoint
COPY entrypoint.sh /
RUN sudo chmod 0755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Install Creos
RUN wget https://avular.blob.core.windows.net/creos/creos_sdk_0.7.1_jammy_arm64.zip \
    && unzip creos_sdk_0.7.1_jammy_arm64.zip \
    && apt update \
    && cd creos_sdk_client_package_Release_jammy_arm64 \
    && dpkg -i creos-*_*_arm64.deb \
    && cd .. \
    && rm -rf creos_sdk_client_package_Release_jammy_arm64 \
    && rm creos_sdk_*.*.*_jammy_arm64.zip

WORKDIR /home/user/ws

# Install extra dependencies
# RUN sudo apt update && sudo apt install -y \
#     <package you want to install>

USER user
WORKDIR /home/user/ws
CMD ["/bin/bash"]
