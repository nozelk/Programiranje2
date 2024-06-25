import requests
import re
from collections import Counter

url = requests.get('https://www.gutenberg.org/files/11/11-h/11-h.htm')
besedilo=url.text
besedilo=re.sub('<[^<]+?>', '', besedilo)
besedilo_2 = re.sub('\"', '', besedilo)
beseda = re.sub('\s', ' ', besedilo_2)
imena = re.findall('[A-Z][a-z]*', beseda)

st_imen=Counter(imena)
prvih_15=st_imen.most_common(15)
for imena, stevilo in prvih_15:
    if len(imena)==1:
       continue
    else:
     print(f"{imena} ({stevilo}x)")





