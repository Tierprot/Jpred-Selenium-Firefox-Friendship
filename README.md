# Jpred+Selenium+Firefox=Friendship
### Jpred submitting utility

The idea behind the tool was to check how does mutations influence secondary structure predictions if one would mutate whole protein in all possible ways. Program access Jpred server through Selenium webdriver for Firefox. I used dirty "parallelization" through multiprocessing to divide one thread into 5 to speed up predictions a bit. Script is usable but requires some additional tweaking.

All the Selenium <---> Jpred interaction stuff is described in single_query class, so if u need just that - go on.

**Requirements:**
- Python 3.4
- Selenium 2.53.2

