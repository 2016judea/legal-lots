"""Dump a Municode code node as text. usage: fetch_municode.py <jobId> <productId> <nodeId>
Minneapolis: productId 11490 (job 492538 = Supp. 73 Upd. 1). Saint Paul: productId 10061 (job 495421 = Supp. 133 Upd. 1).
Latest job: https://api.municode.com/Jobs/latest/<productId>"""
import sys,json,re,html,urllib.request
job,prod,node=sys.argv[1:4]
u=f"https://api.municode.com/CodesContent?jobId={job}&nodeId={node}&productId={prod}"
d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})))
for doc in d.get('Docs',[]):
    t=doc.get('Content') or ''
    t=re.sub(r'<(br|/p|/tr|/li|/div)[^>]*>','\n',t); t=re.sub(r'</t[dh]>',' | ',t)
    t=html.unescape(re.sub(r'<[^>]+>','',t)); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    print('#####',doc.get('Title'),doc.get('Id')); print(t)
