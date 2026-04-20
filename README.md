# User container for continuous testing of the Origin

The docker container "continuous driving test" is an example container that can be used to continuously test a driving Origin. It comes pre-installed with ROS and the necessary dependencies to develop for the Origin. Once build and started, the docker container will sent velocity commands to the Origin so that it will continously drive in a [equilateral triangle](https://en.wikipedia.org/wiki/Equilateral_triangle) with sides of 1 meter.

> [!WARNING]
> Since there is no feedback on the position of the robot, the Origin shall drift from its original path while drving one triangle, after onatoher and after another and so on. So place ensure there is enough space for the Origin to maneuvre.

> [!WARNING]
> Also, since immediate velocities are sent to the robot, the Origin will have NO OBSTACLE AVOIDANCE and will therefore bump into everything it encounters.


This guide will walk you through how to use the docker container to continuously drive the Origin for testing.

## Setting up the user container
The docker container is available on the Origin by default at `/data/user/containers`. If you want to update the user container files, or restore the user container to its default state, you can follow the following steps:

1. SSH into the Origin
> [!WARNING]
> The next step will remove all files in the user container directory. Make sure to back up any files you want to keep.

2. Remove the current user container files
   
    ```bash
    rm -rf /data/user/containers
    ```

3. Clone the user container files to the Origin
    ```bash
    git clone --branch origin_duration_tests https://github.com/avular-robotics/user-container.git /data/user/containers
    ```
4. Building the user containers
    ```bash
    cd /data/user/containers
    docker compose build
    ```

## Using the docker container for continuous testing
In order to start to continuous driving test of the Origin you should start an `ssh` session with the Origin, go the the location of the docker container by running `cd /data/user/containers` and then run the following command in the terminal:
```bash
cd /data/user/containers
docker compose up -d
```
> [!WARNING]
> the Origin shall immediately start driving the equilateral triangle. In case you need to stop the Origin, then press the e-stop and stop the controller by running the following command in any `ssh` session with the robot: `docker stop continuous_driving_test`.