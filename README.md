# User container for the Vertex

The user container is an example container that can be used to develop on the Vertex. It comes pre-installed with ROS Humble, Avular [SDK](https://avular-robotics.github.io/vertex_one_user_documentation/sdk/latest/) and the necessary dependencies to develop for the Vertex.

The guide below will walk you through how to use the user container to develop on the Vertex.

The Vertex also has a example user container for working with the [Realsense Add-on](https://avular-robotics.github.io/vertex_one_user_documentation/latest/payloads/gen4/realsense_add-on/realsense_add-on_overview.html). This example can be found on the branch [`add-on/realsense`](https://github.com/avular-robotics/user-container/tree/add-on/realsense).

## Setting up the user container

The user container is available on the Vertex by default at `/data/user/containers`. If you want to update the user container files, or restore the user container to its default state, you can follow the following steps:

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

4. Building the user containers

    ```bash
    cd /data/user/containers
    docker compose build
    ```

## Using the user container for development

We suggest that you do all your development inside the user container or your own docker container. This will ensure that your code runs on the Vertex as expected and will not be lost when the Vertex is updated.

First of all, you need to start the user container. You can do this by running the following command:

```bash
cd /data/user/containers
docker compose up -d
```

To enter the user container, you can run the following command:

```bash
docker exec -it user /bin/bash
```

You can now start developing on the Vertex. In the container, we have an user named `user`.
This user has sudo rights, so you can install packages and run commands as root. When entering
the container, you will be in the `/home/user/ws` directory. This is the workspace directory
where you can start developing your code. This workspace directory is also mounted from the host OS,
this is done so that you can easily `down` and `up` the container without losing your code.

> [!WARNING]
> Be aware that recreating the container will remove all files outside the workspace directory.

### Installing packages

You probably want to install some packages to develop your code. To test out if the package works you
can just install it in the container. If you are happy with the package you can add it to the `Dockerfile`.
After adding the package to the `Dockerfile` you need to rebuild the container. You can do this by running
the following command from the `/data/user/containers` directory:

```bash
docker compose up -d --build
```

## SDK

The SDK packages are pre-installed in the user container. Which means that you can start developing your code right away. The [SDK Tools examples](https://avular-robotics.github.io/vertex_one_user_documentation/sdk/latest/example_tools.html) are also available.

To discover and test out the SDK try using the [CLI](https://avular-robotics.github.io/vertex_one_user_documentation/sdk/latest/cli.html) or the [ROS2 node](https://avular-robotics.github.io/vertex_one_user_documentation/sdk/latest/ros_wrapper.html).

You can use the user-container Dockerfile as a reference to see how the SDK is installed.

## ROS version

The user container comes pre-installed with ROS Humble but the SDK also supports ROS Jazzy. If you want to use ROS Jazzy, you can change the ROS version in the Dockerfile and change the SDK package download link from `jammy` to `noble`
