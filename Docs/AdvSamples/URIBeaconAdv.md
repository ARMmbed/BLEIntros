#The URI Beacon’s Advanced Features

##Configuring the URIBeacon Dynamically

For the first few seconds after being powered on, a URIBeacon device advertises itself as connectable and configurable - not yet acting as a beacon. This period times out after ``CONFIG_ADVERTISEMENT_TIMEOUT_SECONDS``, and the application switches to being a regular, immutable URIBeacon. Within this initial timeout period, it is possible to connect to the URIBeaconConfigService from a client to update the configuration. 

The application code switches between the two states using a Ticker object called ``configAdvertisementTimeoutTicker`` that calls back into a function called ``timeout()``.

If this dynamic configurability is unnecessary, it can be bypassed by calling ``uriBeaconConfig->setupURIBeaconAdvertisements()`` from ``main()`` immediately after constructing the ``uriBeaconConfig`` object in ``main()``.

##Configuration Persistence

An implementation of the URIBeacon that wants to be compliant with Google’s URIBeacon specification requires persistence of configuration parameters, which means being able to use configuration parameters stored on non-volatile storage. This storage is often internal to the microcontroller, so access to it requires hardware-specific APIs. This makes a URIBeacon application platform-specific and breaks the otherwise portable application development environment offered by mbed. Mbed will soon offer a generic API to access persistent storage, to remedy this situation.

Currently, there are a couple of APIs defined in the URIBeacon demo to abstract access to storage: ``loadURIBeaconConfigParams()`` and ``storeURIBeaconConfigParams()`` (under ``nrfConfigParamsPersistence.cpp``). Porting this demo to another platform will require providing alternative implementations for these.
