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
  <dt>uplinkstats</dt>
  <dd>Use this script to pull loss, latency, and jitter for a specified
  network.</dd>
  <dt>sort</dt>
  <dd>Use this script to sort data based on a regex string</dd>
</dl>


Testing
