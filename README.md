# HistoricalLogGen

### How to use:
 - Please read section 6.1, deployment requirements and limitations
The agent support

The agent can be started directly on a client using CLI arguments
 
 - --start dd/mm/yyyy
 - --stop dd/mm/yyyy
 - --schedule normal/247
 - --speed 10/20/30

An API interface is partly imlemented. It can be started with the 
--api flag (none ofthe above options are required if API is activated)

### Data:
Data (PCAP and converted flows) found in the thesis can be downloaded on:
https://ntnu.box.com/s/l9bfl718n5sg0c3irldypdnve5eb8m6a

### Future work:
- Create a manager for starting the generator on all clients
in a network. 
- More testing
- More modules for user-emulation
- Try various methods for generating the background traffic

### Issues:
I have a suspicion that SkyHigh MIGHT have some sort of 
hypervisor clock synchronization as I briefely discussed in 
the thesis itself under the Depolyment section. I had 
some cases where the guest systems on skyhigh synced its 
clock when NTP was completely disabled (and its NTP severs
removed from registry). I didnt test, but its possible that
disabling the W32Time service completely negates that problem. 

The REST interface implemented for remote starting is just PoC, 
and should be improved before implementation in production. Currently
it is utilizing a simple Flask POST interface. 
