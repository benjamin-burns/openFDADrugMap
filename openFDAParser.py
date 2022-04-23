import json
import csv



with open("drug-label-0001-of-0010.json", "r") as input:
    rawData = input.read()

data = json.loads(rawData)

entriesInFile = len(data["results"])

for i in range(entriesInFile):
    pass


def parseDrug(drugData, out):
    '''
    Method that parses input json data of an individual drug given in {drugData}
    and writes output to {out}.
    '''
    # TODO
    pass


def parseFile(inputFile, out):
    '''
    Parses {inputFile} and outputs drug name mappings to an output file using {out}.

        Parameters:
            inputFile (string)
                    file path in openFDA input file
            out (Writer)
                    output stream to csv file

        Updates:
            out

        Requires:
            {inputFile} is a valid file path to a readable json file in proper openFDA format,
            {out} is open to a file to which the program can write, and
            {out} already contains an appropriate csv header

        Ensures:
            The content of {out} is updated to contain all drug name mappings contained in
                {inputFile}
    '''
    # Open and read in data from {inputFile}
    with open(inputFile, "r") as input:
        rawData = input.read()
    data = json.loads(rawData)
    drugsInFile = len(data["results"])

    for drugNum in drugsInFile:
        drug = data["results"][drugNum]
        parseDrug(drug, out)


def main():
    '''
    Main method for openFDAParser.
    Outputs a csv file with mappings between drug brand names and drug generic names.
    No reformatting is performed on the input (i.e. the values in the mapping are exactly 
        as they appear in the input)
    '''
    FILE_NAMES_LIST = ["openFDAInput1.json"]
    OUTPUT_FILE_PATH = "drugMapping.csv"

    outputFile = open(OUTPUT_FILE_PATH)
    outputWriter = csv.writer(outputFile)

    for file in FILE_NAMES_LIST:
        parseFile(file, outputWriter)
    


if __name__=="__main__":
    main()


