import csv

from unidecode import unidecode

from external_api.tasks.tmx.common import PROVIDER_ID

from airport.models import Airport


f = open('/code/airport/data.csv', 'r')
csv_reader = csv.reader(f, delimiter=',')

airports = []

for row in csv_reader:
    if row[3] == 'airport':
        airports.append(
            Airport(
                destination=None,
                provider_id=PROVIDER_ID,
                external_id=row[1],
                airport_name=row[2],
                search_name=unidecode(row[2]).lower().replace('-', '')
            )
        )

f.close()

Airport.objects.bulk_create(airports)
