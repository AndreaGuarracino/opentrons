from opentrons import protocol_api

# Metadata (read by the server and returned to client applications)
metadata = {
    'protocolName': 'Transfer 200ul from A1 to H12',
    'author': 'Andrea Guarracino',
    'description': 'Simple transfer of 200ul from well A1 to H12 on a Corning 96 wellplate',
    'apiLevel': '2.15'  # Only required field
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
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')  # Load Corning 96 Well Plate on Deck Position 2
    
    # groups
    all_wells = plate.all_wells()
    all_rows = plate.rows()
    all_cols = plate.columns()

    for well in all_wells:
        print(well)

    # # Pipette
    # # Replace 'p300_single' with the pipette you're using, e.g., 'p20_single_gen2' if you're using a different pipette
    # pipette = protocol.load_instrument('p300_single', 'right')  

    # # Protocol steps
    # pipette.pick_up_tip()
    # pipette.transfer(200, plate['A1'], plate['H12'], new_tip='never')
    # pipette.drop_tip()

# Uncomment the line below for local simulation/testing
# run(protocol_api.ProtocolContext())
