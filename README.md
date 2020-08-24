# Python to led strip

<p align="left">
<a href="https://github.com/tfrere/python-to-led-strip#licence"><img src="https://img.shields.io/badge/licence-MIT-green" alt="Licence"></a>
<a href="https://github.com/tfrere/python-to-led-strip"><img src="https://img.shields.io/badge/platform-osx--64%20%7C%20linux--64%20%7C%20windows--64-lightgrey" alt="Platform support"></a>
<a href="https://github.com/tfrere/python-to-led-strip"><img src="https://img.shields.io/github/last-commit/tfrere/python-to-led-strip" alt="Last update"></a>
<a href="https://github.com/tfrere/python-to-led-strip"><img src="https://img.shields.io/github/v/tag/tfrere/python-to-led-strip" alt="Current version"></a>
</p>

This repository is a part from the [**music to led project**](https://github.com/tfrere/music-to-led).

It's a tool that allows you to **send led strip frames** to an **arduino device** using **python**.

![arduino-case](./images/arduino-case.png)

## 1. Electronic scheme

![electronic-scheme](./images/electronic-scheme.png)

### Component list

- 1x **Alim 5V 10A**
- 1x **Arduino nano or other**
- 1x **1000mu Capacitor** ( optional )
- 1x **Led strip female connector**

## 2. Arduino part

The code can be found [here](./arduino/serial-case/serial-case.ino).

To upload it, you will need the NeoPixelBus library. You can [download it here](https://github.com/Makuna/NeoPixelBus) or using library manager, search for "NeoPixelBus".

## 3. Python part

Visualization code is compatible with Python 2.7 or 3.5. It will also require a numpy installation.

On Windows machines, the use of [Anaconda](https://www.anaconda.com/distribution/) is **highly recommended**. Anaconda simplifies the installation of Python dependencies, which is sometimes difficult on Windows.

### Installing dependencies with Anaconda

Create a [conda virtual environment](http://conda.pydata.org/docs/using/envs.html) (this step is optional but recommended)

```
conda create --name visualization-env python=3.5
activate visualization-env
```

Install dependencies using pip and the conda package manager

```
conda install numpy
```

### Installing dependencies without Anaconda

The pip package manager can also be used to install the python dependencies.

```
pip install numpy
```

If `pip` is not found try using `python -m pip install` instead.

## 4. Test your device

Once the wiring is finished and your code uploaded, you can test it following these simple steps :

- Connect the arduino to your computer through usb cable
- run **python serial.py --list-devices** and find the corresponding usb name
- run **python serial.py --test-serial-device "YOUR CORRESPONDING USB NAME"**

## 5. Make the 3d printed case

All the 3d parts can be found in the 3d-parts folder.

### Slicer settings

- Supports **No**
- Resolution **0.2**
- Infill **30-100%**

## 6. The end

You're good to go !

## Misc

### Led number limitation

It depends on two factors :

- Your board maximum baud rate
- Your led alimentation

For now and using the nano case, please consider not using more than 254 leds.

### Calculating led power consumtion

Each individual NeoPixel draws up to 60 milliamps at maximum brightness white (red + green + blue).

- 60 NeoPixels × 60 mA ÷ 1,000 = 3.6 Amps minimum
- 135 NeoPixels × 60 mA ÷ 1,000 = 8.1 Amps minimum
- 135 NeoPixels × 60 mA ÷ 1,000 / 2 (for each led to 125,125,125) = 4.05 Amps minimum
- 300 NeoPixels × 60 mA ÷ 1,000 = 18 Amps minimum
- 300 NeoPixels × 60 mA ÷ 1,000 / 2 (for each led to 125,125,125) = 9 Amps minimum

### OSX

Sometimes, the arduino nano is no recognized by OSX natively and you will have to install specific usb drivers to make it work.

brew tap adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver
brew cask install wch-ch34x-usb-serial-driver

## Roadmap

- Update the protocol
- Upgrade maximum led number
- Make an error proof protocol
- Bluetooth case

## Licence

This project was developed by Thibaud FRERE on MIT Licence.

## Contribute

If you encounter any problems running program, please open a new issue. Also, please consider opening an issue if you have any questions or suggestions for improving the installation process.
