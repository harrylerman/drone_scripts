# drone_scripts
Scripts for Pterosoar drone

mavlogparse.py: a script to convert the drone tlogs to .csv files. See mavlogparse_readme for usage instructions.

quickplot.py: script to plot a csv-converted tlog file. Can plot any number of input parameters vs time, plots are vertically stacked.

    usage: python quickplot.py -i <inputfile> -p <parameters>
  
    <inputfile> is a csv-converted tlog file.
    
    <parameters> is a list of parameters (must be in quotes) to plot vs time, available parameters are in my_fields_new.json
    
    filepath of the input file is hardcoded to ease commandline use but is simple to edit, could change that too.
    
    example: python quickplot.py -i 2_June.csv -p 'VFR_HUD.heading ALTITUDE.altitude_amsl ALTITUDE.altitude_local'
    
plot_pos_data.py: script to plot drone position data, either from a csv-converted tlog or a csv-convert ulog. Can output either a static plot or will save an animated gif. Use mavlogparse in this repository to convert tlogs, pyulog (https://github.com/PX4/pyulog) to convert ulogs.

    usage: python plot_pos_data.py -i <inputfile.csv> -d <delimiter> -a <outputfile.gif for animated plot> -t <if a tlog csv> -u <if a ulog csv>
    
    for ulogs, use the 'vehicle_local_position' csv file. 
    
    filepath is hardcoded, should be the only thing needed to change to use the script. 
    
    for writing animated gif files, it uses the PillowWriter animation writer, I think this is included by default in matplotlib. 
    
    if the input file delimiter is a tab, then put 'tab' for the delimiter (delimiter must be in quotes). We seem to have settled on the '|' delimiter so this parameter may be deprecated in the future. Default is '|'. 
    
    examples: python plot_pos_data.py -i 2_June.csv -d 'tab' -t
              python plot_pos_data.py -i 2_June.csv -d 'tab' -a 2_June.gif -t
              python plot_pos_data.py -i 21_22_19_vehicle_local_position_0.csv -d '|' -u
              python plot_pos_data.py -i 21_22_19_vehicle_local_position_0.csv -d '|' -a 21_22_19.gif -u

my_fields_new.json: available fields in our tlogs. 

There are also tlogs and those tlogs converted to csv's from flights on: June 2 2022; May 24 2022 (csv is zipped). 

Note: these csv-converted tlogs use tabs for delimiters to avoid issues with commas in some of the warning messages and issues with lists (ex: battery cell voltages). To view/manipulate in MS Excel, use Data -> Get Data -> From Text/CSV, and ensure tab delimiter is selected. It's preferred/better to use the python csv module to manipulate data in these files. But, if doing something in Excel, to save the file: save as type "text (tab delimited)" and the resulting .txt file can then be renamed to .csv.

For the python csv module, ensure to use 
~~~
delimiter='\t'
~~~
where applicable.
