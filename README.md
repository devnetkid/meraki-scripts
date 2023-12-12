# meraki-scripts

These meraki scripts are a collection of custom made scripts. They were
written to solve problems or needs, specific to my organization's use
cases. While they were designed with that in mind, you may be
able to adapt a portion of them for your purposes.

Keep in mind that while each script will stand alone, there were some 
functions that were used over and over. To clean things up a bit I 
moved them over to the universal folder. So if you are going to use 
just one you may need to copy over some of the functions found there.

## Scripts available thus far

  - **addresses** When you run this the dashboard returns all found
                  addresses as defined in the Address field on an
                  MX or MZ device.
  - **networks** This script will pull all network ID and names found
                 then write them in a comma separated format.