#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

# Function to generate random temperature and update chart
def draw_temperature_chart(epd, temperatures, max_data_points=20):
    try:
        # Create a blank imag
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)

        # Draw text for the current temperature
        current_temp = temperatures[-1]
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        draw.text((10, 10), f"Current Temperature: {current_temp}  C", font=font24, fill=0)

        # Draw a chart axis
        chart_x_start = 50
        chart_y_start = 60
        chart_width = 400
        chart_height = 200
        draw.rectangle((chart_x_start, chart_y_start, chart_x_start + chart_width, chart_y_start + chart_height), outline=0)
        
        # Plot temperature data as a line chart
        if len(temperatures) > 1:
            step_x = chart_width // (max_data_points - 1)
            min_temp, max_temp = -5, 40
            scale_y = chart_height / (max_temp - min_temp)
            
            # Map temperature to chart coordinates
            def map_temp_to_y(temp):
                return chart_y_start + chart_height - int((temp - min_temp) * scale_y)
            
            points = [
                (chart_x_start + i * step_x, map_temp_to_y(temp))
                for i, temp in enumerate(temperatures[-max_data_points:])
            ]
            
            for i in range(1, len(points)):
                draw.line((points[i - 1], points[i]), fill=0, width=2)

        # Update the display
        epd.display(epd.getbuffer(Himage))
    except Exception as e:
        logging.error("Error in drawing temperature chart: " + str(e))


# Main script
try:
    logging.info("epd7in5 Temperature Chart Demo")
    
    epd = epd7in5.EPD()
    logging.info("Initialize and Clear")
    epd.init()
    epd.Clear()

    temperatures = []  # Store temperature readings
    max_data_points = 20  # Maximum data points to display on the chart

    while True:
        # Generate a random temperature value
        temp = random.randint(-5, 40)
        temperatures.append(temp)

        # Keep only the last `max_data_points` temperatures
        if len(temperatures) > max_data_points:
            temperatures.pop(0)

        # Draw the chart with the updated temperature
        draw_temperature_chart(epd, temperatures, max_data_points)

        # Wait for 15 seconds before updating again
        time.sleep(15)
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit(cleanup=True)
    exit()

