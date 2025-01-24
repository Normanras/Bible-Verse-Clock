# Bible Clock Project

As I was thinking about a gift for my partner, I saw an ad on Instagram a few weeks ago that was a simple box with a e-ink screen that simple displays a verse based on the time. So if it is 3:16, the screen would display the verse for a book in the Bible that contains a verse at chapter 3, verse 16. I thought that would be simple enough to build myself and give for her birthday.

The hardware is pretty easy to conceptualize (subject to change once I start putting wires to hardware):
* ESP powered device
* eInk display
* (optional) RTC sensor

Since Python is the language I'm the most comfortable with, I've been looking for a project to dip my feet into [Micropython](https://micropython.org/).

Current status:
* Logic for making an API call to [Crossway's ESV Endpoint](https://api.esv.org/)
* Parse returned JSON to make it more presentable (fixing special characters, closing open quotes, removing footnotes, etc)
* Add timeout decorator for times that are do not commonly have a verse/chapter association (i.e 11:58).
* Remove the 0 for any "xx:0x" timestamp as verses do not have 0s for numbers under 10.

To Do List:
- [ ] If timeout triggers, display generic verse on screen with the current time
- [ ] Check time every x seconds and run the functions if the time has changed from previous value.
- [ ] Setup micropython files & functions, including display libraries.

Longer term plans to make this "giftable":
- [ ] Create Wi-Fi SSID & Interface to connect to your own Wi-Fi network
- [ ] Web UI to remove/add specific books from being shown
