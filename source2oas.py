import re
import json
import sys
import os
import os.path
import collections
import ruamel.yaml as yaml
import urllib.parse
from ruamel.yaml.representer import Representer
yaml.add_representer(collections.defaultdict, Representer.represent_dict)


postutils_re = re.compile(r'(?s)(\n\s*)PostUtil.post\(([^,]*),(.*?)\1}')
urls_re = re.compile(r'(Urlsutil|Urlsutil.getInstance\(\)|new Urlsutil\(\))\.(\w+)(\(\))?\s*(\+ "[^"]*")*')
params_re = re.compile(r'(?s)(\n\s*)public void Params\((.*?)\1}')
map_re = re.compile(r'map.put\("([^"]*)", .*\);')

class Url:
    def __init__(self, name, url):
        self.name = name
        self.full_url = url
        path, params = strip_query(url)
        self.base_url = path
        self.get_params = params
        self.post_params = []
    
    def add_post_parameter(self, name):
        self.post_params.append(name)

class Urls:
    def __init__(self):
        self.urls = []

    def add(self, url):
        self.urls.append(url)

    def __getitem__(self, name):
        for u in self.urls:
            if u.name == name:
                return u
        return None
    
    def __contains__(self, name):
        for u in self.urls:
            if u.name == name:
                return True
        return False


def get_url_ref(code):
    m = urls_re.search(code)
    if not m:
        return None
    return m.group(2)


def get_postutil_params(content):
    result = {}

    m = postutils_re.findall(content)
    for _, url, body in m:
        url_name = get_url_ref(url)
        m = params_re.search(body)
        m = map_re.findall(m.group(2))
        result[url_name] = m
    return result

def get_urls(content):
    var_re = re.compile(r'public String (\w+) = \((.*) \+ "(.*)"\);')
    meth_re = re.compile(r'public static String (\w+)\(\) {\s*return (.*) \+ "(.*)";')

    matches = var_re.findall(content) + meth_re.findall(content)
    return matches

def read_file(fname):
    with open(fname) as fp:
        return fp.read()

def strip_query(path):
    try:
        base, query = path.split("?", 1)
    except ValueError:
        return path, None

    parts = urllib.parse.parse_qs(query)
    parameters = []
    for key, values in parts.items():
        parameters.append({
            "name": key,
            "in": "query",
            "schema": {
                "type": "string",
                "enum": values
            }
        })

    return base, parameters

def merge_paths(orig, new):
    if orig["summary"]:
        orig["summary"] = orig["summary"] + ", " + new["summary"]
    else:
        orig["summary"] = new["summary"]
    
    if orig["parameters"]:
        if new["parameters"]:
            params = {}
            for param in orig["parameters"] + new["parameters"]:
                name = param["name"]
                if name in params:
                    params[name]["schema"]["enum"] += param["schema"]["enum"]
                else:
                    params[name] = param
    else:
        orig["parameters"] = new["parameters"]
        




def add_posts(urls):
    for root, dirs, files in os.walk(source_dir):
        for fname in files:
            path = os.path.join(root, fname)
            content = read_file(path)
            posts = postutils_re.findall(content)
            for _, url, code in posts:
                url_name = get_url_ref(url)
                if url_name and url_name in urls:
                    paramcodes = params_re.findall(code)
                    for _, pcode in paramcodes:
                        maps = map_re.findall(pcode)
                        for name in maps:
                            urls[url_name].add_post_parameter(name)


def read_urls():
    result = Urls()
    urls_file = os.path.join(source_dir, "com/growatt/shinephone/util/Urlsutil.java")
    urls = get_urls(read_file(urls_file))
    for name, _, path in urls:
        result.add(Url(name, path))
    return result

if False:    
    source_dir = sys.argv[1]

    def create_dict():
        return collections.defaultdict(create_dict)
    paths = create_dict()

    urls_file = os.path.join(source_dir, "com/growatt/shinephone/util/Urlsutil.java")
    urls = get_urls(read_file(urls_file))
    for name, _, path in urls:
        path, params = strip_query(path)
        merge_paths(paths[path], {
            "summary": name,
            "parameters": params
        })
    
    print(yaml.dump(paths))

if __name__ == "__main__":
    source_dir = sys.argv[1]
    urls = read_urls()
    add_posts(urls)
    print(yaml.dump(urls))