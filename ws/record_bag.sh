# 
name=$1

# Check if the name is empty
if [ -z "$name" ]
then
    echo "Please provide a name for the bag file: ./record_bag.sh <name>"
    exit 1
fi

ros2 bag record -s mcap -o $name --all
