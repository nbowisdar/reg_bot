from src.database.tables import Trigger, Template, db
import json
import multiprocessing as ml

path_to_file = str


def generate_json_schema() -> path_to_file:
    file_name = "last.json"
    resp = []
    for temp in Template.select():
        resp.append(
            {
                "name": temp.name,
                "text": temp.text,
                "triggers": [trig.phrase for trig in temp.triggers]
            }
        )
    with open(file_name, mode='w', encoding="utf-8") as file:
        json.dump(resp, file, indent=4)
    return file_name


def _update_db_from_dict(data: dict):
    with db.atomic():
        Template.delete().execute()
        Trigger.delete().execute()
        for i in data:
            template = Template.create(
                name=i['name'],
                text=i['text']
            )
            Trigger.insert_many(
                [
                    {"phrase": tr.casefold(), "template": template}
                    for tr in i['triggers']
                ]
            ).execute()
            
            
def update_db_from_dict_in_other_proc(data: dict):
    proc = ml.Process(target=_update_db_from_dict, args=(data,))
    proc.start()
    from loguru import logger
    logger.info("database updated!")
            
            