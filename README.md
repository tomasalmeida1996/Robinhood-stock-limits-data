# Robinhood-stock-limits-data
Over the last few weeks there has been many discussions and controversies around Robinhood behavior after the WSB and GME stock trading events. Given the current state of events, and as I have many interests around this subject, I thought this work would be an interesting weekend project. So the final objetive was to get RH stock limiting data to later analyze it and compare it to the market behavior.

In order to get the data from RH website, I developed a web scrapping process with Selenium to extract the data from [RH website](https://robinhood.com/us/en/support/articles/changes-due-to-recent-market-volatility/), and stored that data in a MySQL database. Furthermore, everytime the data is extracted from the website, a screenshot of the whole page is taken to serve as a proof of realization.

Note: The resulting database only will be made available at the end of this when the dust settles :)
