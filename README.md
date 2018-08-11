Some POC code to launch instance(s) on [MRC CLIMB](https://climb.ac.uk) using [CloudBridge](http://cloudbridge.cloudve.org/en/latest/). Lots of stuff pulled directly from the CloudBridge documentation.

Currently tested and working on [Cardiff](https://cardiff.climb.ac.uk).

# Endpoints
All internal services should resolve to https://cardiff.climb.ac.uk - edit your hostfile.

# Credentials
Credentials are parsed in the following order:
1. From the script directly
2. From $HOME/.cloudbridge
3. From /etc/cloudbridge.ini

# Process
1. Authenticate
2. List images containing the string "centos"
3. List flavours and select one based on vCPU/RAM characteristics

If _anything_ is provided as an argument:
4. Launch a small instance 
5. Check instance state and report external IP address



This is my first crack at Python, so please excuse terrible structure and quality.
