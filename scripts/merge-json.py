
import sys
import collections
import jprops
import json
import logging
import os

from pprint import pprint

logging.basicConfig(format='%(asctime)s %(levelname)s check_semasiodata.py: %(message)s', level=logging.INFO)


def removeLicense(monsters):
    logging.info("Removing license object from {}".format(monstersSourceFile))
    for idx in range(len(monsters)):
        monster = monsters[idx]
        if 'license' in monster:
            monsters.pop(idx)
    return monsters


def mergeMetadata(monsters, environments, outFile):
    for monster in monsters:
        try:
            logging.info(monster['name'])
            envListToAdd = []
            for env in environments:
                for monsterInEnv in env['monsters']:
                    if monster['name'] in monsterInEnv['name']:
                        envListToAdd.append(env['name'])
                        break
            # append the env list to the monster
            monster['environments'] = envListToAdd
        except KeyError:
            logging.warning("Encountered entity with no name.")

    # create the output file
    with open(outFile, 'w') as outfile:
        json.dump(monsters, outfile)
    
    logging.info("Completed merge.");


# call main
if __name__ == '__main__':

    # load configuration properties
    propertyfile = sys.argv[1]
    
    if os.path.isfile(propertyfile) == False:
        raise Exception('Configuration File %s  does not exist.', propertyfile)
    
    with open(propertyfile) as F:
        props = jprops.load_properties(F, collections.OrderedDict)
        
        monstersSourceFile = props['monsters.file.path']
        envMappingSourceFile = props['monsters.by.environment.file.path']
        mergedOutputFile = props['merged.output.file.path']

    # load and massage the monsters file
    monsters = json.load(open(monstersSourceFile))
    monsters = removeLicense(monsters)

    # load the environments mapping file
    environments = json.load(open(envMappingSourceFile))
 
    mergeMetadata(monsters, environments, mergedOutputFile)
