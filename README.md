# drone_scripts
Scripts for Pterosoar drone

mavlogparse.py: a script to convert the drone tlogs to .csv files. See mavlogparse_readme for usage instructions.

quickplot.py: script to plot a csv-converted tlog file. Can plot any number of input parameters vs time, plots are vertically stacked.

    usage: python quickplot.py -i <inputfile> -p <parameters>
  
    <inputfile> is a csv-converted tlog file.
    
    <parameters> is a list of parameters (must be in quotes) to plot vs time, available parameters are in my_fields_new.json
    
    filepath of the input file is hardcoded to ease commandline use but is simple to edit, could change that too.
    
    example: python quickplot.py -i 2_June.csv -p 'VFR_HUD.heading ALTITUDE.altitude_amsl ALTITUDE.altitude_local'

my_fields_new.json: available fields in our tlogs. 

There are also a tlogs and those tlogs converted to csv's flights on: June 2 2022; May 24 2022. 

Note: these csv-converted tlogs use tabs for delimiters to avoid issues with commas in some of the warning messages and issues with lists (ex: battery cell voltages). To view/manipulate in MS Excel, use Data -> Get Data -> From Text/CSV, and ensure tab delimiter is selected. It's preferred/better to use the python csv module to manipulate data in these files. But, if doing something in Excel, to save the file: save as type "text (tab delimited)" and the resulting .txt file can then be renamed to .csv.

For the python csv module, ensure to use 
~~~
delimiter='\t'
~~~
where applicable.
