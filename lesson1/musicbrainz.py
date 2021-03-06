# To experiment with this code freely you will have to run this code locally.
# Take a look at the main() function for an example of how to use the code.
# We have provided example json output in the other code editor tabs for you to
# look at, but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {"simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"},
                "area": {"inc": "area"}}


def query_site(url, params, uid="", fmt="json"):
    # This is the main function for making queries to the musicbrainz API.
    # A json document should be returned by the query.
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    # This adds an artist name to the query parameters before making
    # an API call to the function above.
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    # After we get our output, we can format it to be more readable
    # by using this function.
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    '''
    Modify the function calls and indexing below to answer the questions on
    the next quiz. HINT: Note how the output we get from the site is a
    multi-level JSON document, so try making print statements to step through
    the structure one level at a time or copy the output to a separate output
    file.
    '''
    # Find number of bands called "First Aid Kid"
    results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    #pretty_print(results)
    list_bands = [x["name"] for x in results["artists"] if x["name"]=='First Aid Kit']
    print "There are " + str(len(list_bands)) + " bands called First Aid Kid"

    # Find begin-area name for Queen
    results_queen = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    pretty_print("Begin area name for Queen: " + results_queen["artists"][0]["begin-area"]["name"])

    # Find spanish alias for the Beatles
    results_beatles = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    beatles_id = results_beatles["artists"][0]["id"]
    alias_data = query_site(ARTIST_URL, query_type["aliases"], beatles_id)
    aliases_beatles = alias_data["aliases"]
    #pretty_print(aliases_beatles)
    beatle = [x["name"] for x in aliases_beatles if x["locale"]=='es']
    print beatle[0]


    # Find disambiguation for Nirvana
    results_nirvana = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    pretty_print(results_nirvana["artists"][0]["disambiguation"])

    #Find When One Direction was formed
    results_oneD = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    pretty_print(results_oneD["artists"][0]["life-span"]["begin"])

if __name__ == '__main__':
    main()
