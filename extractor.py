import bz2
import json
import pydash

def wikidata(filename):
    with bz2.open(filename, 'rt') as f:
        f.read(2)
        for line in f:
            try:
                yield json.loads(line.rstrip(',\n'))
            except json.decoder.JSONDecodeError:
                continue

if __name__=="__main__":
    filename = 'latest-all.json.bz2'

    count = 0
    for record in wikidata(filename):
        if pydash.has(record, 'claims.P31'):
            match = False
            for snak in pydash.get(record, 'claims.P31'):
                if (pydash.get(snak, 'mainsnak.datavalue.value.id') == "Q5"):
                    match = True
            if match:
                count += 1
                qid = pydash.get(record, 'id')
                label = pydash.get(record, 'labels.en.value')
                desc = pydash.get(record, 'descriptions.en.value')
                print(qid, label)
                print("\t", desc)
        if count > 100:
            break            

