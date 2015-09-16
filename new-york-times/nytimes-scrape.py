model_search = "http://api.nytimes.com/svc/search/v2/" + \
            "articlesearch.response-format?" + \
            "[q=search term&" + \
            "fq=filter-field:(filter-term)&additional-params=values]" + \
            "&api-key=9key"

"""http://api.nytimes.com/svc/search/v2/articlesearch.json?q=terrorism+OR+terrorist
&begin_date=19900102&end_date=19900103&sort=newest&api-key=
key"""

search = "http://api.nytimes.com/svc/search/v2/" + \
            "articlesearch.json?" + \
            "[q=terror]" + \
            "&api-key=key"
precise_search = "http://api.nytimes.com/svc/search/v2/" + \
                "articlesearch.json"
terms = "?q=terrorism+OR+terrorist"
api = "&api-key=key"
    
print(precise_search+terms+dates+api)    

"""
    aggressive for looping in order to overcome the ten article limit. instead search each key word PER JOUR, and then concat the jsons into a nice pandas dataframe, and then eventually a csv.
"""
months_list = ["%.2d" % i for i in range(1,2)]
days_list = ["%.2d" % i for i in range(1,32)]
json_files = []
print(months_list)
for x in months_list:
    month_s = x
    month_e = x
    for y in days_list:
        day_s = y
        day_e = str(int(y)+1).zfill(2)
        year_s = "1990"
        year_e = "1990"
        start = year_s + month_s + day_s
        end = year_e + month_e + day_e
        dates = "&begin_date="+start+"&end_date="+end+"&sort=newest"
        #print(start + "   "+end + "\n" +dates)
        r = requests.get(precise_search+terms+dates+api)
        original_json = json.loads(r.text)
        response_json = original_json['response']
        json_file = response_json['docs']
        json_files.append(json_file)
        
frames = []
for x in json_files:
    df = pd.DataFrame.from_dict(x)
    frames.append(df)
#print(frames)
result = pd.concat(frames)
result
