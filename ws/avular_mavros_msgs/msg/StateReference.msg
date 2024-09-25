# Battery information message
# For all field holds, if the field is unavailable the max value will be provided (i.e. UINT32_MAX)

std_msgs/Header header      

float32[3]      position        # m
float32[3]      velocity        # m/s 
float32[3]      acceleration    # m/s^2
float32         heading         # rad 