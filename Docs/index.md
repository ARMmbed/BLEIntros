# mbed BLE

Welcome. We're here to help you build something awesome with an mbed-enabled BLE platform.

If you're totally new check out our [starters documentation](Introduction/BeginnersIntro.md), which will walk you through everything you need to know. If you have some BLE experience, check out the [short version](Introduction/DevIntro.md) and get your first project up and running. 

## mbed OS versions and the BLE API

mbed currently supports three generations of mbed OS:

* mbed OS 5.0 - we recommend you work with this version. From the point of view of a BLE-application developer, mbed OS 5.0 is nearly identical to mbed OS 2.0.
* mbed OS 3.0 - this version works with MINAR, and its sample code is therefore unique.

Despite the significant differences between mbed OS 2.0 and 5.0 and mbed OS 3.0, most of the information presented in this guide is valid for both generations. BLE is still BLE, and the concept of abstracting the hardware through the use of an API has not changed, either. 

However, to prevent confusion, we have divided the guide into sections:

1. [Introduction to BLE](Introduction/Overview.md): Explores BLE as a technology and as a protocol. While this section might occasionally refer to one version or another of mbed OS, it is largely valid for all versions.

1. [BLE on mbed OS 2.05 and 5.0](mbed_Classic/Overview.md): Details sample applications written for mbed OS 2.0, which will also work on 5.0. This section includes general BLE information and basic C++ concepts, so you might find it useful even if you are working with mbed OS 3.0.

1. [BLE on mbed OS 3.0](mbed_OS/Overview.md): Helps the transition from mbed 2.0 or 5.0 to mbed OS, with a focus on BLE.

1. [Advanced samples and features](Advanced/Overview.md): Reviews more advanced BLE features. These focus on mbed 2.0 and 5.0, but serve as good demonstrations of using the API, so mbed OS 3.0 users might find them interesting, too.

1. [Additional resources](Additional/Overview.md): Provides links to other sources, answers to frequently asked questions and a list of abbreviations.
 
## BLE documentation 

If you're looking for the API documentation, please see:

 *  [For mbed OS 5.0](https://docs.mbed.com/docs/mbed-os-api-reference/en/5.1/APIs/communication/ble/).
 *  [For mbed OS 3.0](https://docs.mbed.com/docs/ble-api/en/master/api/index.html).

