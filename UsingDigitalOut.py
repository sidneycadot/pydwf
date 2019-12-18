#! /usr/bin/env python3

import argparse
import contextlib

from pydwf import DigilentWaveformLibrary

def demonstrate_usage(serial_number: str) -> None:

    # Version 3.12.1 of the DWF library has 46 'FDwfDigitalOut' functions, 1 of which (FDwfDigitalOutTriggerSourceInfo) is obsolete.
    #
    # [1] reset()
    # [1] configure(start: bool)
    # [1] status() -> DwfState
    #
    # [1] internalClock    float                  [Hz]   Info
    # [3] triggerSource    TRIGSRC                [-]    Info Set Get              // Info is deprecated!
    # [4] run              float                  [s]    Info Set Get Status
    # [3] wait             float                  [s]    Info Set Get
    # [4] repeat           int                    [-]    Info Set Get Status
    # [2] triggerSlope     DwfTriggerSlope        [-]         Set Get
    # [2] repeatTrigger    bool                   [-]         Set Get
    # [1] count()          int                    [-]                              // counts number of channels
    #
    # ====== Per channel:
    #
    # [2] enable           bool                   [-]         Set Get
    # [3] output           DwfDigitalOutOutput    [-]    Info Set Get
    # [3] type             DwfDigitalOutType      [-]    Info Set Get
    # [3] idle             DwfDigitalOutIdle      [-]    Info Set Get
    # [5] divider          int                    [-]    Info Set Get InitSet InitGet
    # [5] counter          int                    [-]    Info Set Get InitSet InitGet
    # [2] data             string                 [-]    Info Set

    dwf = DigilentWaveformLibrary()

    with contextlib.closing(dwf.device.openBySerialNumber(serial_number)) as device:

        digitalOut = device.digitalOut

        digitalOut.reset()

def main():

    parser = argparse.ArgumentParser(description="Demonstrate usage of the DigitalOut instrument.")
    parser.add_argument('serial_number', help="serial number of the Digilent device")

    args = parser.parse_args()

    demonstrate_usage(args.serial_number)

if __name__ == "__main__":
    main()