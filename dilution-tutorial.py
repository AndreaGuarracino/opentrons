from opentrons import protocol_api

metadata = {
    "protocolName": "Serial Dilution Tutorial",
    "description": """This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.""",
    "author": "New API User"
    }

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", 7)
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", 8)
    plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 9)

    # Load pipette
    right_pipette = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tips])

    # Add diluent to all wells of the plate.
    # For every well on the plate, aspirate 100 µL of diluent from column 1
    # of the reservoir and dispense it in the well.
    right_pipette.transfer(100, reservoir['A1'], plate.wells())

    # Serial dilution across each row
    for i in range(8):  # For each row in the plate
        row = plate.rows()[i]

        # Transfer solution to the first well of the current row and mix (3 times with 50 µL of fluid each time)
        right_pipette.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

        # Serially transfer solution across the row, mixing after each transfer.
        # Since both row[:11] and row[1:] have 11 items, transfer() will step through
        # them in parallel (when the source is i-1, the destination is i).
        right_pipette.transfer(100, row[:11], row[1:], mix_after=(3, 50)) # Mix 3 times with 50 µL of fluid each time

    # In this way, all wells in the plate will have the volume of solution.
    # Transfer 100 µL from the last column to A3 of the reservoir
    right_pipette.transfer(100, plate.columns()[-1], reservoir['A3'])
    # last_column_wells = plate.columns()[-1]
    # for well in last_column_wells:
    #     right_pipette.transfer(100, well, reservoir['A3'])
