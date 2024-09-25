# Vertex Supervisor Mode

# Value  of any supervisor mode can be 'MODE_NONE' is 
uint8 NONE = 0

#Main mode of the supervisor
uint8 SUPERVISOR_INIT           = 1     # Flight Controller initializing
uint8 SUPERVISOR_BOOT_OK        = 2     # Flight Controller booted up succesfully
uint8 SUPERVISOR_CALIBRATING    = 3     # Flight Controller calibrating sensors
uint8 SUPERVISOR_READY          = 4     # Flight Controller ready 
uint8 SUPERVISOR_E_STOP         = 5     # Flight Controller in emergency stop state, reboot required

uint8   mode_supervisor  

# Supervisor flight mode
# Supervisor mode inside the main 'READY' mode  otherwise value is 'MODE_N0NE'

uint8   PRE_FLIGHT_CHECK    = 1     # Basic sensor and RC checks
uint8   MODE_DISARMED       = 2     # Flight Controller ready, motors disarmed
uint8   MODE_ARMED          = 3     # Flight Controller ready, motors armed
uint8   EMERGENCY_STOP      = 4     # Flight Controller in emergency stop mode, motors stopped

uint8   mode_of_flight

# Armed mode of the supervisor 
# Supervisor mode inside the flight mode 'ARMED' otherwise value is 'MODE_N0NE'

uint8   ARMED_MODE_TAKE_OFF     = 1     # Flight Controller in take-off mode
uint8   ARMED_MODE_IN_FLIGHT    = 2     # Take-off completed, in flight
uint8   ARMED_MODE_LANDING      = 4     # Flight Controller in landing mode 
uint8   ARMED_MODE_EMCY_LAND    = 5     # Flight Controller in emergency landing

uint8   mode_armed 

# Supervisor mode of operation
# Mode of operation when main mode is 'READY' otherwise value is 'MODE_N0NE'

uint8   ATTITUDE_MODE_MANUAL    = 1     # Manual RC control over attitude angles, altitude velocity and yaw velocity
uint8   POSITION_MODE_MANUAL    = 2     # Manual RC control over horizontal velocity in body frame, altitude velocity and yaw velocity
uint8   POSITION_MODE_EXTERNAL  = 3     # External control while following waypoints or commands.

uint8   mode_of_operation

