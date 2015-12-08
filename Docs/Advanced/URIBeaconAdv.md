#The URIBeacon’s advanced features

##Configuring the URIBeacon dynamically

For the first few seconds after being powered on a URIBeacon device doesn't act as a beacon. Instead, it advertises itself as connectable and configurable. This period times out after ``CONFIG_ADVERTISEMENT_TIMEOUT_SECONDS``, and the application switches to being a regular, immutable URIBeacon. During the configurable period, it is possible to connect to the ``URIBeaconConfigService`` from a client to update the beacon's configuration. 

The application code switches between the two states using a Ticker object called ``configAdvertisementTimeoutTicker`` that calls back into a function called ``timeout()``.

If this dynamic configurability is unnecessary, it can be bypassed by calling ``uriBeaconConfig->setupURIBeaconAdvertisements()`` from ``main()`` immediately after constructing the ``uriBeaconConfig`` object in ``main()``.

##Configuration persistence

An implementation of the URIBeacon that wants to be compliant with Google’s URIBeacon specification needs persistence of configuration parameters. This means being able to use configuration parameters stored on non-volatile storage. This storage is often internal to the microcontroller, so access to it requires hardware-specific APIs. This makes a URIBeacon application platform-specific and breaks the otherwise portable application development environment offered by mbed. mbed will soon offer a generic API to access persistent storage, to remedy this situation.

Currently, there are a couple of APIs defined in the URIBeacon demo to abstract access to storage: ``loadURIBeaconConfigParams()`` and ``storeURIBeaconConfigParams()`` (under ``nrfConfigParamsPersistence.cpp``). Porting this demo to another platform will require providing alternative implementations for these.
