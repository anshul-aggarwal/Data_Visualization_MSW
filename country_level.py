import csv

country_data_file = open('country_level_data_0.csv', newline='')
country_pop_file = open('API_SP.POP.TOTL_DS2_en_csv_v2_41106.csv', newline='')


country_data = csv.reader(country_data_file, delimiter=',')
pop_data = csv.reader(country_pop_file, delimiter=',')
country_data_csv_format = next(country_data)
#print("\n".join(csv_format))
pop_data_csv_format = next(pop_data)

country_name = 2
msw_tons_per_year = 26
iso3c_country_data = 0
iso3c_pop_data = 1
pop_2017 = 61

population_list = dict()
for row in pop_data:
    try:
        population_list[row[iso3c_pop_data]] = int(row[pop_2017])
    except ValueError:
        try:
            population_list[row[iso3c_pop_data]] = int(next(pop for pop in reversed(row) if not pop == ""))
            print("Population data for country missing - " + row[iso3c_pop_data] + " - Choosing older population value " + str(population_list[row[iso3c_pop_data]]))
        except ValueError:
            population_list[row[iso3c_pop_data]] = 0
            print("Population data for country missing - " + row[iso3c_pop_data] + " - Skipping")

country_names = dict()
msw_kg = dict()
for row in country_data:
    country_names[row[iso3c_country_data]] = row[country_name]
    try:
        msw_kg[row[iso3c_country_data]] = float(row[msw_tons_per_year])*907.185
    except ValueError:
        print("MSW data for country missing - " + row[iso3c_country_data])
        #msw_kg[row[iso3c_country_data]] = 0

outfile = open("msw_kg_per_capita.tsv", "w+")
outfile.write("Country\tMSW_kg_per_capita\n")
for country_iso3c in country_names:
    try:
        msw_per_capita = msw_kg[country_iso3c]/population_list[country_iso3c]
        outfile.write(country_names[country_iso3c] +"\t"+ str(msw_per_capita) + "\n")
    except ZeroDivisionError:
        msw_per_capita = 0
    except KeyError:
        print("Data for country missing - " + country_iso3c + " - Skipping")
    

outfile.close() 