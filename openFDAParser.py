import json

def parseDrug(drugData):
    '''
    Parses input JSON data of an individual drug given by {drugData}
    and returns a condensed JSON representation.

        Parameters:
            drugData (JSON object)
                    dictionary holding drug information from openFDA

        Returns:
            A JSON representation of drug name mapping data with formatting
              * brand_name
              * generic_name

        Requires:
            {drugData} formatting is consistent with openFDA formatting

        Ensures:
            {parseDrug} = [a JSON representation of a subset of the data contained
            in {drugData}, with the formatting described in {Returns}]
    '''
    try:
        drugBrandName = drugData["openfda"]["brand_name"][0]
    except KeyError:
        print("Error: brand_name is not an attribute of the following data:\n" + str(drugData["openfda"]))
        exit()

    try:
        drugGenericName = drugData["openfda"]["generic_name"][0]
    except KeyError:
        print("Error: generic_name is not an attribute of the following data:\n" + str(drugData["openfda"]))
        exit()
    

    drugDataRep = {}
    drugDataRep["brand_name"] = drugBrandName.lower()
    drugDataRep["generic_name"] = drugGenericName.lower()

    return drugDataRep


def parseFile(inputFile, drugMappings):
    '''
    Parses input JSON data given by {inputFile} and appends condensed JSON
    data representation containing drug name mapping data for all drugs in
    {inputFile} into {drugMappings}.

        Parameters:
            inputFile (string)
                    file path in openFDA input file
            drugMappings (JSON object)
                    dictionary to which to add drug name mapping data

        Updates:
            drugMappings

        Requires:
            {inputFile} is a valid file path to a readable JSON file in proper openFDA format

        Ensures:
            The content of {drugMappings} is updated to contain all drug name mappings contained in
            {inputFile}. If the input file cannot be opened, an error is thrown and program
            execution stops
    '''
    # Open and read in data from {inputFile}
    try:
        with open(inputFile, "r") as input:
            rawData = input.read()
    except OSError:
        print("Error: could not open file " + inputFile);
        exit()

    data = json.loads(rawData)
    drugsInFile = len(data["results"])

    for drugNum in range(drugsInFile):
        drug = data["results"][drugNum]
        if not drug["openfda"] == {}:
            drugMappings.update(parseDrug(drug))


def main():
    '''
    Main method for openFDAParser.
    Outputs a JSON file with mappings between drug brand names and drug generic names.
    All input text is converted to lowercase. Otherwise, output mappings are as
    exactly as they appear in input.
    '''
    FILE_NAMES_LIST = ["openFDAInput1.json"]
    OUTPUT_FILE_PATH = "drugMapping.json"

    #outputFile = open(OUTPUT_FILE_PATH)
    
    drugMappings = {}

    for file in FILE_NAMES_LIST:
        parseFile(file, drugMappings)

    print(drugMappings)

if __name__=="__main__":
    main()


