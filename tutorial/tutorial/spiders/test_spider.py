import scrapy
import re
import json
import os.path
import itertools

# replace to helper
def pairwise(data):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    return zip(data[0::2], data[1::2]) 

class SeasonSpider(scrapy.Spider):
    name = "seasons"
    start_urls = [
        'https://understat.com/league/La_liga/2018',
        'https://understat.com/league/Serie_A/2018'
    ]

    def parse(self, response): 
        league = response.url.split("/")[-2]
        season = response.url.split("/")[-1]
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
            filename = 'under-{0}-{1}-{2}.json'.format(league, season, item[0])
            with open(filename, 'wb') as f:
                f.write(pretty_parsed.encode())
            self.log('Saved file %s' % filename)

class MatchSpider(scrapy.Spider):
    name = "match"
    start_urls = [ 'https://understat.com/match/{0}'.format(i) for i in range(81, 11000)]
    # start_urls = [ 'https://understat.com/match/{0}'.format(i) for i in range(81, 83)]

    def parse(self, response): 
        match_id = response.url.split("/")[-1]
        filename = 'matches.csv'
        shots_filename = 'shots.csv'
        # print('\n\n\n')
        # print(response.url)
        variable = 'Data'

        # pattern = re.compile(r"var \w+%s = JSON.parse\(\'(.*)\'\)" % variable, re.MULTILINE | re.DOTALL)
        data_pattern = re.compile(r"match_info\s+=\s+JSON.parse\(\'(.*)\'\)", re.MULTILINE | re.DOTALL)
        shots_pattern = re.compile(r"shotsData\s+=\s+JSON.parse\(\'(.*)\'\),", re.MULTILINE | re.DOTALL)

        # pattern = re.compile(r"var (\w+)%s\s+=\s+JSON.parse\(\'(.*)\'\)" % variable, re.MULTILINE | re.DOTALL)
        
        pattern = re.compile(r"var (\w+)", re.MULTILINE | re.DOTALL)

        data = response.xpath('//script[contains(., "var")]/text()').re(data_pattern)
        shots = response.xpath('//script[contains(., "var")]/text()').re(shots_pattern)
        # print('\n\n\n')
        # print(len(pairwise(data)))
        for item in data:
            parsed = json.loads(item.encode().decode('unicode_escape'))
        
        for item in shots:
            shots_parsed = json.loads(item.encode().decode('unicode_escape'))
            shots_parsed = list(itertools.chain.from_iterable(shots_parsed.values()))
        # print('\n\n\n')
            # filename = 'under-{0}-{1}-{2}.json'.format(league, season, item[0])
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write(','.join(parsed.keys()))
                f.write('\n')
        with open(filename, 'a') as f:
            f.write(','.join(parsed.values()))
            f.write('\n')
        if not os.path.isfile(shots_filename):
            with open(shots_filename, 'w') as f:
                f.write(','.join(shots_parsed[0].keys()))
                f.write('\n')
        with open(shots_filename, 'a') as f:
            for shot in shots_parsed: 
                shot = ['' if v is None else v for v in shot.values()] 
                f.write(','.join(shot))
                f.write('\n')
            # f.write(pretty_parsed.encode())
            # self.log('Saved file %s' % filename)
