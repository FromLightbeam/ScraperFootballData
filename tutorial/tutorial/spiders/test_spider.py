import scrapy
import re
import json

# replace to helper
def pairwise(data):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    return zip(data[0::2], data[1::2]) 

class QuotesSpider(scrapy.Spider):
    name = "insta"
    start_urls = [
        'https://understat.com/league/La_liga',
        'https://understat.com/league/Serie_A'
    ]

    def parse(self, response): 
        page = response.url.split("/")[-1]
         
        variable = 'Data'

        # pattern = re.compile(r"var \w+%s = JSON.parse\(\'(.*)\'\)" % variable, re.MULTILINE | re.DOTALL)
        # data_pattern = re.compile(r"var \w+%s\s+=\s+JSON.parse\(\'(.*)\'\)" % variable, re.MULTILINE | re.DOTALL)
        pattern = re.compile(r"var (\w+)%s\s+=\s+JSON.parse\(\'(.*)\'\)" % variable, re.MULTILINE | re.DOTALL)
        # pattern = re.compile(r"var (\w+)%s" % variable, re.MULTILINE | re.DOTALL)

        data = response.xpath('//script[contains(., "var")]/text()').re(pattern)
        print('\n\n\n')
        # print(len(pairwise(data)))
        for item in pairwise(data):
            # print(item[0])
            # print(item[1][0:100])
            parsed = json.loads(item[1].encode().decode('unicode_escape'))
            pretty_parsed = json.dumps(parsed, indent=2, sort_keys=True)
        # print(type(pretty_parsed))
            print('\n\n\n')
        # locations = json.loads(locations)
            filename = 'under-{0}-{1}.json'.format(page, item[0])
            with open(filename, 'wb') as f:
                f.write(pretty_parsed.encode())
            self.log('Saved file %s' % filename)
