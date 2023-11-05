# Story

NMIoT (Next Metro IoT) is a device that provides users with essential information and convenient features in a single package. It offers real-time information about the date and time, weather forecasts for the week, and metro (m1 in Lausanne) departure times. Furthermore, it supports iOS device screen casting through Airplay. This project represents the convergence of diverse functionalities into one IoT device, making it a valuable addition to any environment.

# What

NMIoT is a multi-functional device that offers the following features:

Date and Time Display: NMIoT provides real-time information about the current date and time.
Weather Forecasts: Users can access weekly weather forecasts, allowing them to plan their activities accordingly.
Metro Departure Times: The device displays live departure times for the Lausanne metro (m1), enhancing commuters' convenience.
iOS Screen Casting: NMIoT supports Airplay for casting iOS device screens onto its display.
# How

App Development: NMIoT's functionality is achieved through a Python3-based application, which consists of five threads. Each thread is responsible for a specific feature, including the main application and the four functionalities mentioned above.
# Challenges

Metro Departure Times: Initially, acquiring metro departure times posed a challenge as the main operator of public transportation in Lausanne, TL, did not provide a public API with documentation. To overcome this, web scraping was initially employed. Subsequently, the official REST API used by TL for their mobile and web app was discovered through browser dev tools. With some experimentation, the required requests to obtain the necessary information were determined.

Airplay: NMIoT's Airplay support was implemented using RPiPlay, an open-source AirPlay mirroring server designed for the Raspberry Pi.

# Result

NMIoT was built using a Raspberry Pi Zero W as the main computing platform, a recycled laptop monitor for display, and an LCD driver board to connect the Raspberry Pi's HDMI output to the laptop screen. Power was supplied using a 220V AC to 12V DC (36W) adapter for the driver board and screen and a car adapter (12V DC to 5V DC) for the Raspberry Pi. Heatsinks were added to the driver board to manage heat dissipation.

The project successfully created a functional NMIoT device, capable of delivering a variety of useful information in real-time. The device was housed within a custom-made plywood enclosure. This project, initiated in 2019, underwent a temporary hiatus due to a lack of tools and hardware but remains open to future feature enhancements.