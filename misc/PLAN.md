Initial plan/prompt input ... this was changes/refined during session

Create a utility to maintain a textual file for daily/weekly/monthly working
location.  We will have the following designations for a given day:
 - WFH (work from home)
 - WFL (work from lab)
 - WTR (work travel)
 - WkE (weekend)
 - VAC (vacation)
 - HOL (holiday)
 - OTH (other)

Guidelines
 - The tool should be written in Python.
 - The tool should maintain the data in a text file that is easy to read/modify directly.
 - The tool should run from the command-line with either a one-shot update
   or with an interactive mode.
 - In interactive mode, display a textual calendar (similar to cal output)
   showing the current month with the current day highlighted.
 - In interactive mode, allow editing the designation for any given date
   when prompted.
 - The tool will separate date tracking into months with a given week
   ending on Sunday, and new week starting on Monday.
 - The files should include the week number for the record.
 - Each day in the week will have one of the enumerated designations, and
   can only have one of those values.
 - The Default for Mon and Fri should be WFH.
 - The default for Tue, Wed, Thu should be WFL.
 - The default for Sat and Sun should be WkE.
 - The tool should provide the ability to give statistics/reporting on the
   breakdown of the designated times for a given month (30-day), 90-day and
   365 day period.
 - The tools should support doing a basic data validation.
 - The tool will roll over to a new backing data file each new year.
 - The dir structure should be roughly
     - src/  -- source code
     - data/ -- input/backing data files (e.g., YEAR.log)
     - conf/ -- any needed configurations go here
 - Ask me for any other details needed for remaining requirements.

