#! /usr/bin/env python3

import argparse

from pydwf import DigilentWaveformLibrary, DwfEnumConfigInfo

def main():

    parser = argparse.ArgumentParser(description="Enumerate Digilent Waveform devices.")
    parser.add_argument('--no-obsolete-api', action='store_false',
                        help="for each device, suppress printing of analog-in parameters using obsolete FDwfEnumAnalogIn* API calls", dest='use_obsolete_api')
    parser.add_argument('--no-configurations', action='store_false',
                        help="for each device, suppress printing of configurations", dest='list_configurations')

    args = parser.parse_args()

    dwf = DigilentWaveformLibrary()

    num_devices = dwf.enum.count()

    if num_devices == 0:
        print("No Digilent Waveform devices found.")
        return

    for device_index in range(num_devices):

        devtype = dwf.enum.deviceType(device_index)
        is_open = dwf.enum.deviceIsOpened(device_index)
        username = dwf.enum.userName(device_index)
        devicename = dwf.enum.deviceName(device_index)
        serial = dwf.enum.serialNumber(device_index)

        header = "Device information for device #{} ({} of {} devices)".format(device_index, device_index+1, num_devices)

        print(header)
        print("=" * len(header))
        print()
        print("  device .......... : {}".format(devtype[0]))
        print("  version ......... : {}".format(devtype[1]))
        print("  open ............ : {}".format(is_open))
        print("  username ........ : {!r}".format(username))
        print("  devicename ...... : {!r}".format(devicename))
        print("  serial .......... : {!r}".format(serial))
        print()

        if args.use_obsolete_api:

            ai_channels = dwf.enum.analogInChannels(device_index)
            ai_bufsize = dwf.enum.analogInBufferSize(device_index)
            ai_bits = dwf.enum.analogInBits(device_index)
            ai_frequency = dwf.enum.analogInFrequency(device_index)

            print("Analog-in information (retrieved through obsolete API)")
            print("------------------------------------------------------")
            print()
            print("  number of channels ...... : {!r}".format(ai_channels))
            print("  buffer size ............. : {!r}".format(ai_bufsize))
            print("  bits .................... : {!r}".format(ai_bits))
            print("  frequency ............... : {!r}".format(ai_frequency))
            print()

        if args.list_configurations:

            configuration_data = {}

            num_config = dwf.enum.configCount(device_index)

            for configuration_index in range(num_config):
                for configuration_parameter in DwfEnumConfigInfo:
                    configuration_parameter_value = dwf.enum.configInfo(configuration_index, configuration_parameter)
                    configuration_data[(configuration_index, configuration_parameter)] = configuration_parameter_value

            header = "Supported configurations ({})".format(num_config)

            print(header)
            print("-" * len(header))
            print()
            print("  configuration_index:    {}".format("  ".join("{:8d}".format(configuration_index) for configuration_index in range(num_config))))
            print("  ----------------------  {}".format("  ".join("--------" for configuration_index in range(num_config))))
            for configuration_parameter in DwfEnumConfigInfo:
                print("  {:22}  {}".format(configuration_parameter.name, "  ".join("{:8d}".format(configuration_data[(configuration_index, configuration_parameter)]) for configuration_index in range(num_config))))
            print()


if __name__ == "__main__":
    main()