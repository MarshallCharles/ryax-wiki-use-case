import json
import wikipediaapi


class WikiPageDoesNotExistException(Exception):
    pass

def write_json(obj:dict, where: str)->None:
    with open(where, "w") as f:
        json.dump(obj, f)

def handle(inputs: dict)->dict:
    pagename = inputs["pagename"]
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(pagename)
    print(page.summary)
    if not page.exists():
        print(f"Page with name {pagename} does not exist!")
        raise WikiPageDoesNotExistException
    
    save_loc = f"/tmp/{page.title}.json"
    obj_to_dump = { "summary": page.summary, "links": list(page.links.keys())}
    write_json(obj_to_dump, save_loc)
    return {"pageinfo": save_loc}

if __name__=="__main__":
    handle({"pagename": str(input("Input a pagename\n>>>"))})
