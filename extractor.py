import bz2
import json
import pydash
import csv

def wikidata(filename):
    with bz2.open(filename, 'rt') as f:
        f.read(2)
        for line in f:
            try:
                yield json.loads(line.rstrip(',\n'))
            except json.decoder.JSONDecodeError:
                continue

if __name__=="__main__":
    filename = '/data/latest-all.json.bz2'

    header = ['id','label','desc',
                'birth_time','birth_precision','birth_place'
                'death_time','death_precision','death_place'
            ]
    with open('/data/people.csv','w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        count = 0
        for record in wikidata(filename):
            if pydash.has(record, 'claims.P31'):
                match = False
                for snak in pydash.get(record, 'claims.P31'):
                    if (pydash.get(snak, 'mainsnak.datavalue.value.id') == "Q5"):
                        match = True
                if match:
                    count += 1
                    if count % 1000 == 0:
                        print(count)
                    qid = pydash.get(record, 'id')
                    label = pydash.get(record, 'labels.en.value')
                    desc = pydash.get(record, 'descriptions.en.value')
                    birth = pydash.get(record, 'claims.P569[0].mainsnak.datavalue.value')
                    death = pydash.get(record, 'claims.P570[0].mainsnak.datavalue.value')
                    birth_place = pydash.get(record, 'claims.P19[0].mainsnak.datavalue.value.id')
                    birth_time = pydash.get(birth, 'time')
                    birth_prec = pydash.get(birth, 'precision')
                    death_place = pydash.get(record, 'claims.P19[0].mainsnak.datavalue.value.id')
                    death_time = pydash.get(death, 'time')
                    death_prec = pydash.get(death, 'precision')

                    row = [qid, label, desc, birth_time, birth_prec, birth_place, death_time, death_prec, death_place]
                    csv_writer.writerow(row)
                
#                    print(row)
#            if count > 10:
#                break            

