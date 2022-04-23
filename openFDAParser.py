import json
import csv
from os import listdir

def parseDrug(drugData):
    '''
    Parses input JSON data of an individual drug given by {drugData}
    and returns a condensed JSON representation.

        Parameters:
            drugData (JSON object)
                    dictionary holding drug information from openFDA

        Returns:
            A JSON representation of drug name mapping data with formatting
              * brand_name (string)
              * generic_name (string)

        Requires:
            {drugData} formatting is consistent with openFDA formatting

        Ensures:
            {parseDrug} = [a JSON representation of a subset of the data contained
            in {drugData}, with the formatting described in {Returns}]. If {drugData}
            is not consistent with openFDA formatting, an error is thrown and
            program execution stops
    '''
    # Obtain brand_name attribute from {drugData}
    try:
        drugBrandName = drugData["openfda"]["brand_name"][0]
    except KeyError:
        print("Error: brand_name is not an attribute of the following data:\n" + str(drugData["openfda"]))
        exit()

    # Obtain generic_name attribute from {drugData}
    try:
        drugGenericName = drugData["openfda"]["generic_name"][0]
    except KeyError:
        print("Error: generic_name is not an attribute of the following data:\n" + str(drugData["openfda"]))
        exit()
    
    # Create and populate condensed JSON representation of drug
    drugDataRep = {}
    drugDataRep["brand_name"] = drugBrandName.lower()
    drugDataRep["generic_name"] = drugGenericName.lower()

    return drugDataRep

def parseFile(inputFile, out):
    '''
    Parses input JSON data given by {inputFile} and appends drug name mapping data 
    for all properly formatted drugs in {inputFile} to {out}.

        Parameters:
            inputFile (string)
                    file path of openFDA input file
            out (DictWriter)
                    output stream to csv file

        Updates:
            out

        Requires:
            {inputFile} is a valid file path to a readable JSON file in proper openFDA format,
            {out} is open,
            {out} contains a valid csv header with two features

        Ensures:
            The content of {out} is updated to contain all drug name mappings contained in
            {inputFile}. If the input file cannot be opened or read, an error is thrown and 
            program execution stops
    '''
    # Open and read in data from {inputFile}
    try:
        with open(inputFile, "r") as input:
            try:
                rawData = input.read()
            except UnicodeDecodeError:
                print("Error: there is something wrong with input formatting in " + inputFile)
                exit()
    except OSError:
        print("Error: could not open file " + inputFile);
        exit()

    data = json.loads(rawData)
    drugsInFile = len(data["results"])

    # Parse and print data of each drug in {inputFile}
    for drugNum in range(drugsInFile):
        drug = data["results"][drugNum]
        # Ignore drugs that do not have openfda attribute
        if not drug["openfda"] == {}:
            out.writerow(parseDrug(drug))

def main():
    '''
    Main method for openFDAParser.
    Outputs a csv file with mappings between drug brand names and drug generic names.
    All input text is converted to lowercase. Otherwise, output mappings are as
    exactly as they appear in input.

    Data is read in from directory with relative path {DATA_DIRECTORY}.
    Output file is named {OUTPUT_FILE_PATH} and follows formatting {FIELD_NAMES}.
    If output file already exists, all data will be overridden.
    '''
    # Configuration constants
    DATA_DIRECTORY = "rawData"
    OUTPUT_FILE_PATH = "drugMapping.csv"
    FIELD_NAMES = ["brand_name", "generic_name"]

    # Open output stream and initialize with csv header
    outputFile = open(OUTPUT_FILE_PATH, "w")
    writer = csv.DictWriter(outputFile, fieldnames=FIELD_NAMES)
    writer.writeheader()

    # Parse and print data from each input file
    for file in listdir(DATA_DIRECTORY):
        # Excluse .DS_Store files (MacOS)
        if not file == ".DS_Store":
            parseFile("rawData/" + file, writer)

if __name__ == "__main__":
    main()
