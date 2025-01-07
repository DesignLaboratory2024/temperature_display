#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import random
from datetime import datetime

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

# Function to map temperatures to Y-axis values
def map_temp_to_y(temp, chart_y_start, chart_height, min_temp, max_temp):
    scale_y = chart_height / (max_temp - min_temp)
    return chart_y_start + chart_height - int((temp - min_temp) * scale_y)

# Function to draw temperature chart
def draw_temperature_chart(epd, lab_temperatures, other_temperatures, timestamps, max_data_points=5):
    try:
        # Create a blank image
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)

        # Font setup
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        # Chart configurations
        chart_width = 300
        chart_height = 200
        chart_y_start = 60
        chart_gap = 20
        min_temp, max_temp = 5, 40
        temp_step = 5

        # Lab Temperature Chart
        lab_chart_x_start = 30
        draw.text((lab_chart_x_start, 10), f"Lab Temperature: {lab_temperatures[-1]}°C", font=font24, fill=0)
        draw.rectangle(
            (lab_chart_x_start, chart_y_start, lab_chart_x_start + chart_width, chart_y_start + chart_height),
            outline=0,
        )

        # Gridlines and Y-axis values
        for temp in range(min_temp, max_temp + 1, temp_step):
            y = map_temp_to_y(temp, chart_y_start, chart_height, min_temp, max_temp)
            draw.line((lab_chart_x_start, y, lab_chart_x_start + chart_width, y), fill=128, width=1)
            draw.text((lab_chart_x_start - 30, y - 10), f"{temp}°C", font=font18, fill=0)

        # X-axis timestamps and vertical gridlines
        step_x = chart_width // max_data_points
        for i, timestamp in enumerate(timestamps[-max_data_points:]):
            x = lab_chart_x_start + i * step_x
            draw.line((x, chart_y_start, x, chart_y_start + chart_height), fill=128, width=1)
            draw.text((x - 20, chart_y_start + chart_height + 10), timestamp, font=font18, fill=0)

        # Other Temperature Chart
        other_chart_x_start = lab_chart_x_start + chart_width + chart_gap
        draw.text((other_chart_x_start, 10), f"Other Temperature: {other_temperatures[-1]}°C", font=font24, fill=0)
        draw.rectangle(
            (other_chart_x_start, chart_y_start, other_chart_x_start + chart_width, chart_y_start + chart_height),
            outline=0,
        )

        # Gridlines and Y-axis values
        for temp in range(min_temp, max_temp + 1, temp_step):
            y = map_temp_to_y(temp, chart_y_start, chart_height, min_temp, max_temp)
            draw.line((other_chart_x_start, y, other_chart_x_start + chart_width, y), fill=128, width=1)
            draw.text((other_chart_x_start - 30, y - 10), f"{temp}°C", font=font18, fill=0)

        # X-axis timestamps and vertical gridlines
        for i, timestamp in enumerate(timestamps[-max_data_points:]):
            x = other_chart_x_start + i * step_x
            draw.line((x, chart_y_start, x, chart_y_start + chart_height), fill=128, width=1)
            draw.text((x - 20, chart_y_start + chart_height + 10), timestamp, font=font18, fill=0)

        # Plot temperatures for both charts
        def plot_chart(temperatures, chart_x_start):
            if len(temperatures) > 1:
                for i in range(1, len(temperatures)):
                    x1 = chart_x_start + (i - 1) * step_x
                    y1 = map_temp_to_y(temperatures[i - 1], chart_y_start, chart_height, min_temp, max_temp)
                    x2 = chart_x_start + i * step_x
                    y2 = map_temp_to_y(temperatures[i], chart_y_start, chart_height, min_temp, max_temp)

                    color = 0 if temperatures[i] <= 25 else 1  # Black if <= 25, Red otherwise
                    draw.line((x1, y1, x2, y2), fill=color, width=2)

        plot_chart(lab_temperatures, lab_chart_x_start)
        plot_chart(other_temperatures, other_chart_x_start)

        # Update display
        epd.display(epd.getbuffer(Himage))

    except Exception as e:
        logging.error("Error in drawing temperature chart: " + str(e))

# Main script
try:
    logging.info("epd7in5 Dual Temperature Chart Demo")
    
    epd = epd7in5.EPD()
    logging.info("Initialize and Clear")
    epd.init()
    epd.Clear()

    lab_temperatures = []  # Store lab temperature readings
    other_temperatures = []  # Store other temperature readings
    timestamps = []  # Store timestamps
    max_data_points = 5  # Maximum data points to display on the chart

    while True:
        # Generate random temperatures
        lab_temp = random.randint(5, 40)
        other_temp = random.randint(5, 40)
        current_time = datetime.now().strftime("%H:%M")

        lab_temperatures.append(lab_temp)
        other_temperatures.append(other_temp)
        timestamps.append(current_time)

        # Keep only the last `max_data_points` temperatures and timestamps
        if len(lab_temperatures) > max_data_points:
            lab_temperatures.pop(0)
        if len(other_temperatures) > max_data_points:
            other_temperatures.pop(0)
        if len(timestamps) > max_data_points:
            timestamps.pop(0)

        # Draw the charts with updated temperatures
        draw_temperature_chart(epd, lab_temperatures, other_temperatures, timestamps, max_data_points)

        # Wait for 15 seconds before updating again
        time.sleep(15)
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit(cleanup=True)
    exit()
