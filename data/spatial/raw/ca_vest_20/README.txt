2020 California precinct and election results shapefile.

## RDH Date retrieval
09/29/2021

## Sources
Election results primarily from the California Statewide Database (https://statewidedatabase.org/d10/g20.html). Precinct results that were combined by the Statewide Database were separated according to the 2020 Statement of the Vote from the registrars of the following counties: Glenn, El Dorado, Imperial, Inyo, Madera, Mendocino, San Joaquin, San Luis Obispo, Shasta, Sierra, Siskiyou, Sutter, Tuolumne.
Precinct shapefiles were obtained directly from nearly all counties. The precinct shapefiles for Modoc County and Sierra County were obtained from the Los Angeles Times Data Desk GitHub. For Trinity County the precinct shapefile was generated using the parcel precinct assignments in the General Plan shapefile. California counties routinely consolidate precincts based on polling place assignments and ballot styles for a given election. The majority of the county shapefiles featured regular precincts rather than consolidated precincts. Wherever necessary the registration precincts were consolidated to match the election results using the November 2020 consolidation reports from the respective counties.

## Fields metadata

Vote Column Label Format
------------------------
Columns reporting votes follow a standard label pattern. One example is:
G16PREDCli
The first character is G for a general election, P for a primary, C for a caucus, R for a runoff, S for a special.
Characters 2 and 3 are the year of the election.
Characters 4-6 represent the office type (see list below).
Character 7 represents the party of the candidate.
Characters 8-10 are the first three letters of the candidate's last name.

Office Codes
AGR - Agriculture Commissioner
ATG - Attorney General
AUD - Auditor
COC - Corporation Commissioner
COU - City Council Member
DEL - Delegate to the U.S. House
GOV - Governor
H## - U.S. House, where ## is the district number. AL: at large.
INS - Insurance Commissioner
LAB - Labor Commissioner
LAN - Commissioner of Public Lands
LTG - Lieutenant Governor
PRE - President
PSC - Public Service Commissioner
RRC - Railroad Commissioner
SAC - State Appeals Court (in AL: Civil Appeals)
SCC - State Court of Criminal Appeals
SOS - Secretary of State
SSC - State Supreme Court
SPI - Superintendent of Public Instruction
TRE - Treasurer
USS - U.S. Senate

Party Codes
D and R will always represent Democrat and Republican, respectively.
See the state-specific notes for the remaining codes used in a particular file; note that third-party candidates may appear on the ballot under different party labels in different states.


## Fields
G20PREDBID - Joseph R. Biden (Democratic Party)
G20PRERTRU - Donald J. Trump (Republican Party)
G20PRELJOR - Jo Jorgensen (Libertarian Party)
G20PREGHAW - Howie Hawkins (Green Party)
G20PREAFUE - Roque "Rocky" De La Fuente Guerra (American Independent Party)
G20PREPLAR - Gloria La Riva (Peace and Freedom Party)

## Processing Steps
Butte County amended its precinct results after the state certification deadline. The amended results are higher than the certified results as follows: Biden (D) +389, Trump (R) +89, Jorgensen (L) + 15, Hawkins (G) + 3, De La Fuente (A) + 2, La Riva (S) +1. The precinct results for Sutter County add 1 Biden vote and 2 Trump votes more than the certified totals. 
In Los Angeles County a scattering of ballots were reported by canvassing batch rather than by precinct. These add up to 54 Biden votes and 23 Trump votes. In San Diego County a scattering of ballots were reported from VBM "pseudo" precincts that are not assigned to a polling location. These add up to 93 Biden votes, 69 Trump votes, and 3 Jorgensen votes. 

In Sierra County, Precinct 23 (Sierra City 4) was added according to the 2018 PDF map provided by the county clerk. In Imperial County, Siskiyou County, and Sutter County regular precincts were split using water districts, fire districts, and school districts, respectively, consistent with the November 2020 district reports. In Siskiyou County, Weed 1 and Weed 2 were split using the voter assignment street list and the parcel shapefile.
A scattering of precincts in Los Angeles County do not feature a district assignment for either California State Senate or for Board of Equalization. In these instances the consolidated precincts cross district boundaries in areas where the relevant districts were not on the ballot for the November 2020 general election.