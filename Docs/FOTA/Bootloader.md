#Internals of the Nordic DFU Boot Loader

The Device Firmware Update (DFU) service, when added to a BLE application, enables Firmware Over the Air (FOTA). As we’re working with Nordic’s nRF51822 Bluetooth system, we require a Nordic-specific DFU boot loader.

To update or modify the boot loader, you’ll need to understand how it works. We’ll start with reviewing the components, then the sources the boot loader requires, and finally see how to set up the boot loader and combine it with an initial application.

##Overview of Components

FOTA requires the following components:

* **SoftDevice**: Nordic’s encapsulation of the Bluetooth stack.

* The user’s **BLE application**.

* **DFU boot loader**. This, along with the BLE application and the SoftDevice, is built as the initial firmware for users to put on their devices. 

* Boot loader **settings page**: tells the boot loader about forwarding control to the application.

* **UICR**: a register defined by nRF MCU, which tells the SoftDevice where to forward control: the boot loader or the application.

## Overview of the System Startup Process

Here’s a summary of the boot process. We present it early on in this document to prepare the reader for the concepts that follow. Many of the details will be presented later on.

The system starts up with the SoftDevice gaining control by virtue of its vector table being placed at the start of the internal flash. After some basic initialization, it forwards control to the address taken from the UICR register (described below). If the UICR contains any value other than the default of ``0xFFFFFFFF``, this is taken to be the start of the receiving vector table. We program the UICR to contain the start of the bootloader. As a result, the bootloader gains control following the initialization of the soft-device.

The bootloader checks the GPREGRET register to determine if it has received control from the softdevice or an application which has triggered FOTA.

If the bootloader receives control from the softdevice, it refers to the values in its settings page to determine what it needs to do next. We’ve programmed the settings to forward control to any user application if one is found to exist. The application is expected to begin at the end of the softdevice, which is known to have a fixed size. The bootloader can inspect the flash memory following the tail end of the soft-device to determine a valid application header. If a seemingly valid header is discovered, control forwards to the application. If no useful application exists, then the bootloader enters the FOTA process where it awaits a new firmware over BLE.

If the bootloader receives control from an app which has triggered FOTA, it awaits a new firmware over BLE. Once new firmware has arrived over BLE, it is verified and forwarded control rightaway.

###Updating Firmware with USB

When working with the Nordic mKIT, or any mbed Nordic platform, drag-n-drop of the firmware over USB results in a mass-erase followed by programming. We have two possible builds for that firmware: 

1. The default IDE builds, which are non-FOTA. They include the SoftDevice and the application. As these are non-FOTA, they’re not relevant for this article.

2. A build that includes the initial application, which itself includes the SoftDevice, the initial firmware as described above, boot loader and the UICR (pointing to the boot loader). This is available for [download](https://developer.mbed.org/teams/Bluetooth-Low-Energy/wiki/Firmware-Over-the-Air-FOTA-Updates#default-bootloader).

###Updating Firmware with FOTA

When updating over FOTA, you’ll need to include only the application in the package you’re sending. Note, however:

1. You need an application that already supports FOTA (that is, if the application was not programmed to allow FOTA, no amount of configurations on the device or server can force it to accept FOTA). This includes the DFUService call and a boot loader. We have [instructions for adding FOTA support to your application](http://developer.mbed.org/forum/team-63-Bluetooth-Low-Energy-community/topic/5169/).

2. You need platforms matching FOTA. You can find these in the [Platforms page](http://developer.mbed.org/platforms/).
In other words, if you need FOTA you must first get the SoftDevice and boot loader, with initialized UICR, onto the device. You can use [srec_cat](http://srecord.sourceforge.net/) to combine things and initialize the UICR and boot loader settings.

##Sources and Build Instructions for the Boot Loader

The [sources](https://github.com/mbedmicro/dfu-bootloader) are available publicly on GitHub. They are derived from Nordic's SDK V6.1.0 with very minor modifications. The bootloader cannot yet be built using the online toolchain on mbed.org because unlike regular mbed applications it needs to be located at a non-standard starting address at the upper end of the internal flash. Bootloader builds can be accomplished using a separate offline build system based on CMake. 

###Building with CMake

The sources include a CMakeLists.txt file. This is a build configuration file that contains variables that point to some headers and resources (from mbed-SRC and the nRF51822 libraries) that the boot loader build depends on.

The following variables may need to be updated:

* ``MBED_SRC_PATH`` to point to the location of the folder called ‘mbed’ within your local clone of mbed-src repository.

* ``BLE_API_SRC_PATH`` to point to the local clone of the BLE_API repository.

* ``NRF51822_SRC_PATH`` to point to the local clone of the nRF51822 repository.

* ``CMAKE_CXX_COMPILER`` and ``CMAKE_C_COMPILER`` to point to your arm-none-eabi-g++ or gcc as appropriate.

* ``SIZE_COMMAND`` and ``OBJCOPY_COMMAND`` to point to arm-none-eabi-size and objcopy (as appropriate).Git Sources in CMakeLists.txt


You can build the boot loader with the following steps:

```cmake
/BLE_BootLoader$ mkdir Build
/BLE_BootLoader$ cd Build/
/BLE_BootLoader/Build$ cmake ..
/BLE_BootLoader/Build$ make -j all
```

###Size Limitations

Please note that we expect to fit the boot loader within 16K of internal flash (at the upper end of the code space); this includes nearly 1K of configuration space (for boot loader settings), so the actual available code size is a little less than 15K. 

Depending on your toolchain, it may be a challenge to fit the boot loader within these constraints. Doing this with ARM-CC requires the use of the linker feedback files, involving two rounds of compilation in which the first round generates the feedback file. Please refer to the command line compiler option called 'feedback' under [infocenter.arm.com](http://infocenter.arm.com/help/index.jsp) or search for "Minimizing code size by eliminating unused functions during compilation" in the context of ARM-CC.

If you are unable to fit the boot loader within 16K, then increase the value of the constant ``BOOTLOADER_REGION_START``; you'll then also need to make a corresponding change in the boot loader's linker script to place the vector table at the new START address.

##The UICR

The UICR is a collection of memory-mapped configuration registers starting from the address ``0x10000000``; they can be programmed like any other part of the internal flash, and determine who gets control when a device starts up: the application or the bootloader.

The following snippet within ``bootloader_settings_arm.c`` sets up the update for UICR by setting up the UICR.BOOTADDR to point to the boot loader’s vector table:

```cmake
uint32_t m_uicr_bootloader_start_address
__attribute__((at(NRF_UICR_BOOT_START_ADDRESS))) = BOOTLOADER_REGION_START;
```

You should be able to verify that the .hex file generated for the boot loader contains the update to UICR.BOOTADDR. The following lines at the end of the generated .hex file do the trick:

```cmake
:020000041000EA
:0410140000C0030015
```

They specify the programming of the 4-byte value ``0x0003C000`` at address ``0x10001014``, which is the address of UICR.BOOTADDR. Please [refer](http://en.wikipedia.org/wiki/Intel_HEX) to the format for Intel HEX files. 

Please also refer to the datasheet for the nRF51822 for the layout of registers within the UICR region.

##Receiving Control at Startup

At reset, the SoftDevice checks the UICR.BOOTADDR register. Two things can happen:

1. If the register is blank (meaning it is set to ``0xFFFFFFFF``), the SoftDevice assumes that no boot loader is present. It then forwards interrupts to the application and executes the application as usual. 

2. If the BOOTADDR register is set to an address different from ``0xFFFFFFFF``, the SoftDevice assumes that the boot loader vector table is located at this address. Interrupts are then forwarded to the boot loader at this address and execution will be started at the boot loader reset handler.

##Setup to Forward Control to the Application

After being handed control, the boot loader looks for an application at the end of the SoftDevice (if it fails to find one, it sets up the DFUService and waits for a new firmware).

In the normal case, where there is an application, you'd want the boot loader to forward control to it. You must update the boot loader’s settings to instruct it to look for a valid application; this can either be done statically or by manually writing to the 'settings' region . Settings reside within the page starting at the address ``0x003FC00``.

The following settings need to be installed (listed alongside the corresponding addresses):

```cmake
0x3FC00: 0x00000001
0x3FC04: 0x00000000
0x3FC08: 0x000000FE
0x3FC0C-0x3FC20: 0x00000000
```

The above can be accomplished by amending the command line options to ``srec_cat`` with the following sequence placed *after* ``${PROJECT_NAME}.hex -intel``:

```cmake
-exclude 0x3FC00 0x3FC20 -generate 0x3FC00 \
0x3FC04 -l-e-constant 0x01 4 -generate 0x3FC04 \
0x3FC08 -l-e-constant 0x00 4 -generate 0x3FC08 \
0x3FC0C -l-e-constant 0xFE 4 -generate 0x3FC0C \
0x3FC20 -constant 0x00
```

##Combining the SoftDevice and an Initial Application

The initial image to be programmed onto a device needs to contain the SoftDevice with the DFU-boot loader and (optionally) an initial application. If there is no initial application, the bootloader will wait for FOTA.

The following is a complete command to combine all the above components:

```cmake
srec_cat ${MBED_SRC_PATH}/targets/hal/TARGET_NORDIC \
TARGET_MCU_NRF51822/Lib/s110_nrf51822_7_0_0/ \
s110_nrf51822_7.0.0_softdevice.hex -intel BLE_Default_APP.hex -intel \
../../BLE_BootLoader/Build/BLE_BOOTLOADER.hex -intel -exclude 0x3FC00 \
0x3FC20 -generate 0x3FC00 0x3FC04 -l-e-constant 0x01 4 -generate \
0x3FC04 0x3FC08 -l-e-constant 0x00 4 -generate 0x3FC08 0x3FC0C \
-l-e-constant 0xFE 4 -generate 0x3FC0C 0x3FC20 -constant 0x00 -o \
combined.hex -intel
```

Et voila, the above produces a ``combined.hex`` that is ready to be flashed onto the target following a mass-erase; you've got your DFU boot loader all set up.

##Receiving Control from an Application when FOTA Is Triggered

The boot loader receives control in one of two possible cases: either from the SoftDevice during system startup (as we saw above), or from an application for which FOTA has been triggered. In the second case, the boot loader should always enter DFU mode and wait for a new firmware. It is important for the boot loader to be able to distinguish between the two possibilities. This is done through one of the registers in the power-domain - the GPREGRET - which is the general purpose retention register.

When DFU is triggered by writing into the control characteristic of the DFU service, a DFU- enabled application executes the following code, which sets GPREGRET that can then be read back by the boot loader:

```cmake	
sd_power_gpregret_set(BOOTLOADER_DFU_START);
```

``BOOTLOADER_DFU_START`` is a constant that the boot loader sees as indication that control flowed into it from an application (instead of the SoftDevice).

##Finally

You're free to modify and enhance the boot loader. In fact, you're encouraged to do so. You might want to have your particular flavour depend on certain buttons or other settings to do special boot-yoga.

We intend to rewrite the boot loader using mbed's BLE_API; we also want to abstract the platform agnostic parts of the boot loader to be able to produce a portable variety.

Happy Hacking. And may FOTA be fun for you.
