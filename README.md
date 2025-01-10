# Temperature Display Project
The main goal of this project is to fetch temperature data and display it on the e-paper screen in the form of a temperature chart. The chart will update, providing a visual representation of temperature fluctuations.

Hardware
* Raspberry Pi 3
* A Waveshare 7.5-inch e-paper display, used for the temperature chart.
* Waveshare E-Paper HAT, connecting the display to the Raspberry Pi.

Software
* Python 3.x
* Necessary Python libraries for interacting with the Waveshare e-paper display

At first, a hardware needed to be chosen. Display was already provided, so a microcontroller needed to be discussed. Big advantage of a Rapberry Pi was availability of libraries provided by a display producer (which cannot be said about STM32, Arduino or any other platform). Then, we decided to develop our software using Python, because of its possibilities in terms of drawing charts, which is a main purpose of our project. 
We chose to use display vertically, because that way we are able to fit 2 charts on a display at the same time. It might be useful to monitor not only the air temperature in a laboratory, but some hardware temperature, too.
Updating content of a display takes much time, so it does not make much sense to refresh it often. We plan to do it every hour and keep values from the last 5 hours on both charts.
