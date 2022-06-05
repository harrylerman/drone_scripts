# drone_scripts
Scripts for Pterosoar drone

mavlogparse.py: a script to convert the drone tlogs to .csv files. See mavlogparse_readme for usage instructions.

quickplot.py: script to plot a csv-converted tlog file. Can plot any number of input parameters vs time, plots are vertically stacked.

    usage: python quickplot.py -i <inputfile> -p <parameters>
  
    <inputfile> is a csv-converted tlog file.
    
    <parameters> is a list of parameters (must be in quotes) to plot vs time, available parameters are in my_fields_fixed.json
    
    filepath of the input file is hardcoded to ease commandline use but is simple to edit, could change that too.
    
    example: python quickplot.py -i 2_June.csv -p 'VFR_HUD.heading ALTITUDE.altitude_amsl ALTITUDE.altitude_local'

my_fields_new.json: available fields in our tlogs. 

There is also a tlog from a flight on June 2, 2022 and that tlog converted to a .csv.
