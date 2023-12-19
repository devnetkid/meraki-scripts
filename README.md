# meraki-scripts

These meraki scripts are a collection of custom made scripts. They were
written to solve problems or needs, specific to my organization's use
cases. While they were designed with that in mind, you may be
able to adapt a portion of them for your purposes.

Keep in mind that while each script will stand alone, there were some 
functions that were used over and over. To clean things up a bit I 
moved them over to the universal folder. So if you are going to use 
just one you may need to copy over some of the functions found there.

## Instructions

1. Clone the code for meraki-scripts
2. In the root folder create two folders called input and output
3. In the output folder create another folder called logs

### Example of settings.toml file

Take the following and paste it into a file called settings.toml
Make sure to put this file in the input folder. Now let's say
that you want to get all addresses for your organization. You
could modify the output_file in the [addresses] section or just
leave it as is. The same goes for all the rest of the functions
available.

```
# settings.toml

title = "Your Company Name, Meraki Operations"

# addresses
[addresses]
output_file = "output/addresses.txt"

# cellular
[cellular]
filter_list = ""
output_file = "output/cellular.csv"

# updategp
[updategp]
network_list = "input/networks.txt"
new_group_policy = "input/new_policy.json"
existing_name = 'my_group_policy'

# uplinkstats
[uplinkstats]
uplink_interface = "wan1"
destination_ip = "8.8.8.8"
output_file = "output/uplink-stats.csv"

# Script level logging
[logging]
file_log_level = 'info'
file_log_path = 'output/logs/'

# Meraki library settings
[meraki]
api_key = false
api_key_environment_variable = 'MERAKI_DASHBOARD_API_KEY'
suppress_logging = true
print_to_console = false
output_log = false
log_file_prefix = 'meraki_api_'
log_path = 'output/logs'
```

## Scripts available thus far

<dl>
  <dt>addresses</dt>
  <dd>When you run this the dashboard returns all found addresses as 
    defined in the Address field on an MX or MZ device.</dd>
  <dt>networks</dt>
  <dd>This script will pull all network ID and names found then write 
    them in a comma separated format.</dd>
  <dt>cellular</dt>
  <dd>Use this script to pull cellular data. Includes: Site, Model,
    Status, Connection Type, Signal Type, APN, ICCID, RSRP, RSRQ</dd>
  <dt>updategp</dt>
  <dd>Use this script to modify a group policy for a specified list
  of networks.</dd>
  <dt>uplinkstats</dt>
  <dd>Use this script to pull loss, latency, and jitter for a specified
  network.</dd>
  <dt>sort</dt>
  <dd>Use this script to sort data based on a regex string</dd>
</dl>