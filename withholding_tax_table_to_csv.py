# Convert a file describing the tax tariffs for Swiss witholding tax/Quellensteuer/impôt à source
# to csv format suitable for importing to spreadsheet software (default import settings work in LibreOffice Calc)

# Supports only the tariff for regular employees (record type 06)

# See https://www.estv.admin.ch/estv/de/home/direkte-bundessteuer/quellensteuer/dienstleistungen/tarife-herunterladen.html

# Usage: "python witholding_tax_table_to_csv.py [input file_name] [output_file_name]"
# Example: witholding_tax_table_to_csv.py tar14zh.txt tar14zh.csv
usage = "python witholding_tax_table_to_csv.py [input file_name] [output_file_name]"
example = "python witholding_tax_table_to_csv.py tar14zh.txt tar14zh.csv"

import csv
import sys

def parse_vorlauf(line):
    # Returns canton abbreviation, create date (as string)
    canton = line[2:4]
    creation_date = line[19:27]
    return canton, creation_date

def parse_record(line):
    record_type = line[0:2]
    transaction_type = line[2:4]
    canton = line[4:6]
    qst_code = line[6:16]
    tariff_group = qst_code[0]
    with_church_tax = qst_code[2]
    valid_from_date = line[16:24]
    income_from = line[24:33]
    tariff_increment = line[33:42]
    num_children = line[43:45]
    tax_in_chf = line[45:54]
    tax_in_percent = line[54:59]
    return record_type, tariff_group, with_church_tax, income_from, \
           tariff_increment, num_children, tax_in_chf, tax_in_percent

def main():
    if(len(sys.argv))<=2:
        print("Please provide the input filename as the first argument and output filename as second argument")
        print("Usage:", usage)
        print("Example:", example)
        return
        

    input_fn = sys.argv[1]
    input_file = open(input_fn, 'r')
    output_fn = sys.argv[2]
    output_file = open(output_fn, 'w', newline='')
    #output_file.write("sep= \n")

    csvwriter = csv.writer(output_file, delimiter=' ')
    csvwriter.writerow(['Quellensteuer tariffs for employees'])

    canton, valid_from = parse_vorlauf(input_file.readline())
    csvwriter.writerow(['Canton:', canton, 'Valid from:', valid_from])
    
    csvwriter.writerow(['Tariff group', 'With church tax', 'From income', 'Income increment', 'Num. children', 'Tax in CHF', 'Tax in percent'])
    for line in input_file:
        if line[0:2]=='99':
            # This is the 'endrecord'
            break
        record_type, tariff_group, with_church_tax, income_from, \
                    income_increment, num_children, tax_in_chf, tax_in_percent = parse_record(line)
        
        # add a decimal point to the tax in percent
        tax_in_percent = tax_in_percent[0:3] + '.' + tax_in_percent[3:5]
        if record_type=='06':
            csvwriter.writerow( [tariff_group, with_church_tax, income_from, income_increment, num_children, tax_in_chf, tax_in_percent] )

    output_file.close()
    input_file.close()

if __name__ == "__main__":
    main()