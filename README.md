# Timegate

A 3D printed fiber optic RGB LED clock.

## Required Tools

- Basic soldering setup
- 3D printer with 140mm x 140mm usable print area minimum
- Hot glue gun

## Required Materials

- [Adafruit ESP32-S3 Feather with 4MB Flash 2MB PSRAM](https://www.adafruit.com/product/5477)
- [5v WS2813 RGB LED 30/m](https://www.amazon.com/WS2813-Individually-Addressable-WS2812B-Updated/dp/B09MKJLDX4)
- [2mm Side Glow Plastic Optical Fiber](https://www.amazon.com/Lind-Kitchen-2-0mm-Transparent-1-5mm/dp/B0D2HRQQCL)
- 3D printed part glue, such as [IPS Weld-On #16](https://www.amazon.com/Weld-Acrylic-Plastic-Cement-Tube/dp/B00R5NYM7M)
- Hot glue sticks
- Painters/masking tape
- Plastic primer and paint, original piece used Rustoleum Hammered Gray spray paint
- 24 AWG stranded hookup wire (~50mm each of 3 colors - red, black, yellow)
- USB-C data-capable cable for programming and power
- USB-C power adapter

For both the LEDs and optical fiber, you'll need less than 0.5m per clock.

## Assembly

1. Print all of the STL files in the `models` directory can be printed in any stiff filament. The original piece was printed using PETG on an Ender 5 Pro and sliced using Prusa Slicer.
2. Gently sand all parts so they fit and have a nice smooth surface
3. Cut sections of the optical fiber to fit between the inner and outer ring, press into place using a flathead screwdriver or similar. Alternate sides to maintain tension.
4. Trim the supports that connect the inner and outer rings and sand off remaining nubs of plastic.
5. Cut strip of LEDs to get a segment of 12 and tin and solder wires to the pads. Solder red to +, black to -, and yellow to data.
6. Thread the wires down through the stand of the outer ring and position the LEDs in the outer ring, going counter-clockwise.
7. Once the LEDs are positioned correctly, put a few dabs of hot glue into the outer ring to hold them there.
8. Glue the inner and outer ring covers into place, the face with the covers is the front of the clock.
9. Thread the wires through the base and glue the base to the outer ring using plastic glue/weld (NOT hot glue). Wait for it to cure.
10. Protect the wires and optical fiber with painters tape and then prime and paint the piece. Wait for it to dry.
11. Remove the painters tape and solder the wires to the microcontroller. Solder red to USB, black to GND, and yellow to pin 11.
12. Fit the microcontroller onto the plastic pins, then melt the tops of the pins to hold it down.
13. Connect the microcontroller to your computer, you may need to first flash it with CircuitPython 9.x (follow the instructions from Adafruit).
14. Copy the contents of the `src` folder to the microcontroller.
15. Edit the `settings.py` with the code editor of your choice and enter your wifi credentials and time zone information.
