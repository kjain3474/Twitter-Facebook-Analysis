import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import re
import webbrowser

df = pd.read_csv('tweet.csv')
places=["goa","karnataka","matheran"]

val_map={'goa':1.0,'karnataka':1.0,'matheran':1.0}
edge_list=[]
df_post={'goa':[],'karnataka':[],'matheran':[]}
screen_name={}
labeldict = {}
G=nx.Graph()
count_list_post={}
count_list_postby={}

pos=nx.spring_layout(G)

#G.add_node("goa")
#G.add_node("karnataka")
#G.add_node("matheran")
labeldict["goa"] = "goa"
labeldict["matheran"] = "Matheran"
labeldict["karnataka"] = "Karnataka"
'''matchobj =re.match(r'RT\s@(\w*)',df.text[5])

print(matchobj.group(1))'''

for i in range(20):
    s=df.text[i].lower()
    s1=df.text[i]
    p=re.compile(r'RT\s@(\w*)')
    matchobj=re.match(p,s1)
    
    if matchobj:
        print matchobj
        print('pass')
        pass
    else:
        print('accept')
        print matchobj
        for j in places:
            if s.find(j)!=-1:
                x=df_post.get(j)
                x.append([df.screenname[i],df.text[i]])
                df_post[j]=x
                labeldict[df.screenname[i]]=df.screenname[i]
                
                val_map.setdefault(df.screenname[i],0.2)
                edge_list.append((j,df.screenname[i]))
                #edge_list.append()

print(df_post)

#like section
for y in range(20):
    s1=df.text[y]
    p=re.compile(r'RT\s@(\w*)')
    matchobj=re.match(p,s1)
    if matchobj:
        
        if screen_name.has_key(matchobj.group(1)):
             print matchobj.group(1)
             x=screen_name.get(matchobj.group(1))
             x.append(df.screenname[y])
             screen_name[matchobj.group(1)]=x
             labeldict[df.screenname[y]]=df.screenname[y]
                
             val_map.setdefault(df.screenname[y],0.7)
             edge_list.append((matchobj.group(1),df.screenname[y]))
        else:
            screen_name.setdefault(matchobj.group(1),[df.screenname[y]])
            labeldict[df.screenname[y]]=df.screenname[y]
                
            val_map.setdefault(df.screenname[y],0.7)
            edge_list.append((matchobj.group(1),df.screenname[y]))

print(screen_name)
#nx.draw(G,pos=None,node_color=range(24),node_size=800,cmap=plt.cm.Blues,with_labels = True)
#nx.draw_networkx_nodes(G,pos=None,node_list=['sgsg'],font_size=16,font_color='red')
G.add_edges_from(edge_list)
values = [val_map.get(node, 0.25) for node in G.nodes()]
nx.draw(G, cmap=plt.get_cmap('jet'), node_color=values, with_labels = True)

plt.savefig('twitter.jpg')

plt.show()

f = open('helloworld.html','a')
for q in places:  
    
    for i in nx.all_neighbors(G,q):
        #print i
        if count_list_post.has_key(q) == 0:
               count_list_post.setdefault(q,[i])
        else:
            #print('else')
            x=count_list_post.get(q)
            x.append(i)
            count_list_post[q]=x
        
placelengths = [len(v) for v in count_list_post.values()]
post=''

print placelengths
for i,j in zip(places,placelengths):
    #print i,j
    post = post+i+' = '+str(j)+'<br>'
    
print post

for j in places:
    nodename =  count_list_post.get(j)
    for i in range(len(nodename)):
        for k in nx.all_neighbors(G,nodename[i]):
        
            if count_list_postby.has_key(nodename[i]) == 0:
               count_list_postby.setdefault(nodename[i],[k])
            else:
            #print('else')
                x=count_list_postby.get(nodename[i])
                x.append(k)
                count_list_postby[nodename[i]]=x
                                 
#print count_list_postby.keys()


postlengths = [len(v) for v in count_list_postby.values()]

#print postlengths
recommend=[]
postby=''
for i,j in zip(count_list_postby.keys(),postlengths):
    #print i,j
    postby = postby+i+' = '+str(j)+'<br>'
    if j > 2:
        list1 = count_list_postby[i]
        for a in range(j):
            if list1[a] in places:
                print(list1[a])
            elif list1[a]==i:
                print(list1[a])
            else:
                recommend.append(list1[a])
        

print recommend

message = """
<tr>
<th>
<center>
TWITTER
</center>
</th>
<th>
<center>
OUTPUT
</center>
</th>
<th>
<center>
Recommendation
</center>
</th>
</tr>
<tr>
<td>
<img src="twitter.jpg">
</td><td>Number of Post for the following places:<br>""" + post 

abc="""
</tr>
</table>
""" 
xyz="""<br>Number of likes and comments to a user <br>""" +postby 
 
pqr =  """
</td>
</tr>
""" 
#print abc
message = message + xyz


lmn = """<td><br>Recommend following people <br>""" 
for i in recommend:
    lmn = lmn + i + '<br>'
    
message = message +lmn
message = message +pqr
messsage = message+abc 
f.write(message)
f.close()

webbrowser.open_new_tab('helloworld.html')
'''for x in range(20):
    s=df.text[i].lower()
    for j in d_likedbyListkeys:
        if pid_like==j:
            print(df_1.name[x])
            y=d_likedby.get(j)
            y.append(df_1.name[x])
            d_likedby[j]=y
            nodename = d_post.get(d_likedby.get(j)[0])[0][1]
            labeldict[df_1.name[x]]=df_1.name[x]
            G.add_node(df_1.name[x])
            G.add_edge(nodename,df_1.name[x])       '''