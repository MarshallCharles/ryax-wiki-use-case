import json

import wikipediaapi


class NoWikiPageWithNameException(Exception):
    pass


def write_json(obj: dict, where: str) -> None:
    with open(where, "w") as f:
        json.dump(obj, f)


def handle(inputs: dict) -> dict:
    pagename = inputs["pagename"]
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(pagename)
    if not page.exists():
        print(f"No wikipedia with the pagename {pagename} exists.")
        raise NoWikiPageWithNameException

    save_loc = f"/tmp/{page.title}.json"
    write_json({"summary": page.summary, "links": list(page.links.keys())},save_loc)
    return {"pageinfo": save_loc}
