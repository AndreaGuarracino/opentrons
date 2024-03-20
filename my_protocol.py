from opentrons import protocol_api

# Metadata (read by the server and returned to client applications)
metadata = {
    'protocolName': 'My protocol',
    'author': 'Andrea Guarracino',
    'description': 'Protocol description',
    'apiLevel': '2.15' # Only required field
}

# This function must be named exacly "run" with exactly one argument
# which represents the robot and its capabilities. This context:
# - remembers, tracks, and checks the robot's state
# - exposes the functions that make the robot execute actions
def run(protocol: protocol_api.ProtocolContext):
    # Labware refers to places, reservoirs, tiptracks, tuberacks,
    # and any other static products used in liquid handling on the deck.

    # load_labware takes:
    # - a "loadname" that points to information about the physical dimensions of the labware and its comprising wells
    # - a "slot" (1-11) that points to the labware's physical locations on the deck
    # - (optional) a display name
    # https://labware.opentrons.com/corning_96_wellplate_360ul_flat/
    plate = protocol.load_labware(
        load_name='corning_96_wellplate_360ul_flat',
        location='2',
        label='Name-of-the-plate'
    )  # Load Corning 96 Well Plate on Deck Position 2
    
    # Groups of wells
    all_wells = plate.wells()
    all_rows = plate.rows()
    all_cols = plate.columns()

    print(len(all_rows))
    print(len(all_cols))
    print(len(all_wells))

    # for well in all_wells:
    #     print(well)
    # for row in all_rows:
    #     print(row)
    #     print('\n')
    
    # Individual wells
    well_H3 = plate.wells_by_name()['H3']
    wells_10_thru_12 = plate.wells()[9:12]
    row_A= plate.rows()[0]
    column_5 = plate.columns_by_name()['5']

    print(well_H3)
    print(wells_10_thru_12)
    print(row_A)
    print(column_5)
    
    # Pipette refers to the Opentrons fleet of the elettronic pipette.
    # The OT-2 granty houses 2 pipette mounts (left and right)
    # load_instrument takes:
    # - a "model" pointing to the range and type (single- or multi-channnel) of the pipette
    # - a "mount" (left or right)
    # - (optional) tiètracks (an istance of labware) to automatically iterate over tip pickups
    p300 = protocol.load_instrument(
        instrument_name='p300_single',
        mount='left'
    )# some protocols require more tips, so you can assign them to a pipette all at once, like tip_racks=[tips1, tips2]
    # CONVENTION: [p|m]volume (single-channel 300 uL -> p300)

    # Simple commands
    # p300.pick_up_tip() # pick up the first available tip
    # p300.flow_rate.aspirate = 300 # flow_rate change in uL/s
    # p300.flow_rate.dispense = 300 # flow_rate change in uL/s
    # p300.mix(repetitions=10, volume=200, location=source)
    # p300.aspirate(200, source)
    # p300.dispense(200, destination)
    # p300.blow_out(destination)
    # p300.drop_tip() # drop the tip in the default waste bin

    # Complex commands
    #transfer() from 1 well to 1 well
    #distribute() 1 to many
    #consolidate() many to 1

    # # Protocol steps
    # p300.pick_up_tip()
    # p300.transfer(200, plate['A1'], plate['H12'], new_tip='never')
    # p300.drop_tip()


    # Non-liquid handling commands
    protocol.comment('This is a comment. Robot function will continue.')
    protocol.delay(minutes=1, seconds=30, msg= 'Delaying for 90 seconds.')
    protocol.pause('Pausing until user input.')

# Uncomment the line below for local simulation/testing
#run(protocol_api.ProtocolContext())
