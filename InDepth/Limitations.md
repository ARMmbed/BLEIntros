#What Can't you Do?

Technology always has limitations. For mbed BLE, the most important ones are:

1. **The BLE device can talk only to phones, tablets etc.** It doesn't yet support direct communication between BLE devices. This is not a restriction of the protocol, since one common form of device-to-device communication (via meshing) would only require peripherals to scan for advertisements from neighbouring devices, and that feature is already a part of the standard - so this limitation should be removed shortly.

2. **The BLE device doesn't have independent access to the internet.** It requires either additional hardware or constant access to a BLE-enabled device with its own internet access, such as a mobile phone. Bluetooth IP support is  part of the latest standard, and it will be supported in mbed BLE before the end of 2015.

3. **For BLE to truly be low-energy, it has to work as little as possible.** That means, for example, limiting the frequency of its broadcasts, letting it sleep whenever there is no new data to handle, etc. We'll look at these parameters in other sections, such as the [discussion about connection parameters](/InDepth/ConnectionParameters/) and some of our coding samples.

4. **Bluetooth signals have a limited range, with Class 2 devices limited to about ten meters (33 feet)**; this can be extended with an antenna. Signals can be blocked by concrete and metal, so they don't always travel through walls. 

5. **Bluetooth 4 doesn't work on older mobile phones**, but as phones are upgraded quite often, in a year or two you can expect the majority of phones in the west to be able to communicate with our devices.

