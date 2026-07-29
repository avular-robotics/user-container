# User container for the Vertex realsense add-on

The realsense add-on user container is an example container that can be used to develop with the realsense add-on on the Vertex. It comes pre-installed with the Avular SDK and the necessary dependencies to develop for the Vertex.

This guide will walk you through how to use the realsense container to develop on the Vertex.

> [!NOTE]
> This repository provides two containers: **this one** (`realsense-add-on`) for general ROS 2 / GStreamer development and raw video access, and the nested **[`realsense/` container](realsense/README.md)** (`realsense_ros`) for the RealSense ROS 2 API (`rs-enumerate-devices`, camera topics, etc.). See [Using the RealSense ROS2 API](#using-the-realsense-ros2-api) below.

## Setting up the realsense container

The realsense container is by default not available on the Vertex. If you want to use the realsense user container, or restore the container to its default state, you can follow the following steps:

1. SSH into the Vertex
2. Remove the current realsense user container files

> [!WARNING]
> This will remove all files in the realsense user container directory. Make sure to back up any files you want to keep.

```bash
rm -rf /data/user/add-on/realsense
```

3. Clone the realsense container files to the Vertex

```bash
git clone --branch add-on/realsense https://github.com/avular-robotics/user-container.git /data/user/add-on/realsense
```

4. Building the realsense container

```bash
cd /data/user/add-on/realsense
docker compose build
```

## Using the realsense user container for development

We suggest that you do all your development inside the realsense user container. This will ensure that your code runs on the Vertex as expected and will not be lost when the Vertex is updated.

First of all, you need to start the container. You can do this by running the following command:

```bash
cd /data/user/add-on/realsense
docker compose up -d
```

To enter the user container, you can run the following command:

```bash
docker exec -it realsense-add-on /bin/bash
```

You can now start developing on the Vertex. In the container, we have a user named `user`.
This user has sudo rights, so you can install packages and run commands as root. When entering
the container, you will be in the `/home/user/ws` directory. This is the workspace directory
where you can start developing your code. This workspace directory is also mounted from the host OS,
this is done so that you can easily `down` and `up` the container without losing your code.

> [!NOTE]
> This workspace is bind-mounted from `/data/user/add-on/realsense/ws` on the host (shipped in this repo), so your changes persist across `down`/`up` and can be edited directly from the host.

> [!WARNING]
> Be aware that recreating the container will remove all files outside the workspace directory.

### Installing packages

You probably want to install some packages to develop your code. To test out if the package works you
can just install it in the container. If you are happy with the package you can add it to the `Dockerfile`.
After adding the package to the `Dockerfile` you need to rebuild the container. You can do this by running
the following command from the `/data/user/add-on/realsense` directory:

```bash
docker compose up -d --build
```

## Using the container to create a livestream

The realsense container can be used to livestream the rgb camera of the realsense, for example as an fpv camera. All the right dependecies are already pre-installed and it is already configured to have access to the linux `video` group. This enables you to setup the livestream without needing sudo rights.

> [!NOTE]
> **Prerequisites on the host.** If the pipeline fails with `no element "nvv4l2h265enc"` or `no element "nvvidconv"`, the host is missing the NVIDIA L4T GStreamer plugins. Install them on the **host** (not the container) via SSH:
> ```bash
> sudo apt install nvidia-l4t-gstreamer
> ```
>
> **RTSP server.** `rtspclientsink` pushes the stream to an RTSP server rather than hosting one itself — on the Vertex this is the `mediamtx` system container. If port 8554 isn't reachable, confirm `mediamtx` is running on the host.

#### Manually setting up the livestream
By default, the container is configured to do "nothing". This means you can enter the container and start the livestream manually. This can be done with the following command:

```bash
gst-launch-1.0 v4l2src device=/dev/video-rs-rgb ! videoconvert ! video/x-raw,format=BGRx ! nvvidconv ! nvv4l2h265enc control-rate=0 bitrate=1000000 peak-bitrate=2000000 preset-level=1 ! h265parse ! rtspclientsink location=rtsp://0.0.0.0:8554/realsense
```

> [!NOTE]
> Device name depends on your Vertex software version: `/dev/video-rs-rgb` or `/dev/video_rs_rgb`. Run `ls /dev | grep video-rs` (or `video_rs`) on the host to check which one applies.

By default, it is configured for minimal latency and with variable bitrate control of 1 Mbps and a peak bitrate of 2 Mbps. This should be enough for a high quality stream which you can view on your remote or on a different device.

#### Viewing the livestream
For this part, we assume the IP addres of the Vertex through the Herelink remote hotspot. This is `192.168.144.50`. You can replace this IP with a different IP depending on the connection type between your device and the Vertex.

##### QGroundControl
For viewing the livestream through QGroundControl (or a different application), use the following address:
```bash
rtsp://192.168.144.50:8554/realsense
```

##### Terminal
For viewing the livestream through the terminal, use the following address:
```bash
ffplay -fflags nobuffer -flags low_delay -probesize 32 -analyzeduration 1 -strict experimental -framedrop -vf "rotate=0:bilinear=0,format=yuv420p,setpts=0" rtsp://192.168.144.50:8554/realsense
```
You will need `ffmpeg` to be installed before you can use ffplay.

##### VLC
You can use VLC to view the livestream. You will need the same link as is described for QGroundControl. It is important to know that VLC has a standard buffer time of ± 2 seconds; therefore, we don't recommend using VLC.


#### Automatically starting up the livestream
You can also setup the container to automatically start the livestream. this can be done by commenting out the default startup command (add a # in front of `command: sleep infinity`) in the docker-compose file and uncommenting the livestream command (remove the # in front of the sentence). 

```bash
command: gst-launch-1.0 v4l2src device=/dev/video-rs-rgb ! videoconvert ! video/x-raw,format=BGRx ! nvvidconv ! nvv4l2h265enc control-rate=0 bitrate=1000000 peak-bitrate=2000000 preset-level=1 ! h265parse ! rtspclientsink location=rtsp://0.0.0.0:8554/realsense
#command: sleep infinity
```
Make sure the right amount of tabs/spaces are in front of the line.

To apply this change, run `docker compose up -d --build` again. Once done, the livestream should automatically start. You can verify if everything is working well with `docker logs realsense-add-on`.

#### Troubleshooting


##### NvRmMemInitNvmap failed with Permission denied
When you get the following error: `NvRmMemInitNvmap failed with Permission denied`, it means you don't have access to the `video` group. By default we add access to the dockerfile, but it is possible the the group ID inside the container is not the same as outside of the container. You can verify this by comparing the ID of `video` both inside and outside of the container with the following command: `cat /etc/group`. 
If this indeed is not the same, replace the `- video` in the docker-compose file to, for example, `- 44` when the ID is indeed 44.

##### no element "nvv4l2h265enc" / "nvvidconv"
This means the host is missing the NVIDIA L4T GStreamer plugins the pipeline needs. SSH into the Vertex (not the container) and run:
```bash
sudo apt install nvidia-l4t-gstreamer
```
then restart the container (`docker compose up -d --build`) and try again.

##### Caught SIGSEGV / InitNVENC: Host1x handle open failed
This means the container's user can't access the hardware encoder. On current CreOS/L4T kernels, NVENC is reached through the DRM render node (`/dev/dri/renderD*`), which is owned by the `render` group — not through the legacy `/dev/nvhost-ctrl` device, which doesn't exist on these kernels at all. If the container's user isn't in the `render` group, NVIDIA's plugin fails to open it and crashes instead of returning a clean error.

Make sure the container process is in both the `video` and the host's `render` group. The `render` GID defaults to `104`; if `getent group render` on the host reports a different number, set `RENDER_GID` (e.g. in a `.env` file next to [docker-compose.yml](docker-compose.yml)) before recreating the container (`docker compose up -d --build`).

Separately, `NVIDIA_VISIBLE_DEVICES`/`NVIDIA_DRIVER_CAPABILITIES` under `environment:` are needed to avoid `EGL failed to initialize`/`Connecting to nvargus-daemon failed` — a different, earlier failure than the NVENC crash, but easy to hit at the same time.

##### rs-enumerate-devices: command not found
This container doesn't include librealsense — use the `realsense_ros` container instead, see [Using the RealSense ROS2 API](#using-the-realsense-ros2-api) below.

## Using the RealSense ROS2 API

This container does not ship librealsense or the RealSense ROS 2 wrapper. For the full RealSense ROS 2 API (camera/depth/pointcloud topics, `rs-enumerate-devices`, etc.), use the nested container in [`realsense/`](realsense/README.md).
