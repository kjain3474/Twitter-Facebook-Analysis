import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import webbrowser


nodename=""
places=["goa","karnataka","matheran"]
labeldict = {}
count_list_post={}
count_list_postby={}
post=''
G=nx.Graph()
recommend = []
count=0
pos=nx.shell_layout(G)
#G.add_node("goa")
#G.add_node("karnataka")
#G.add_node("matheran")
labeldict["goa"] = "goa"
labeldict["matheran"] = "Matheran"
labeldict["karnataka"] = "Karnataka"

map_value={'goa':1.0,'karnataka':1.0,'matheran':1.0}
edge_list=[]

d_post={'goa':[],'karnataka':[],'matheran':[]}
#d_postedby={'goa':[],'karnataka':[],'matheran':[]}

df = pd.read_csv('post.csv')

for i in range(20):
    s=df.msg[i].lower()
    for j in places:
        if s.find(j)!=-1:
            x=d_post.get(j)
            x.append([df.pid[i],df.name[i]])
            d_post[j]=x
            labeldict[df.name[i]]=df.name[i]
            #G.add_node(df.name[i])
            map_value.setdefault(df.name[i],0.2)
            edge_list.append((j,df.name[i]))
            #nx.draw_networkx_nodes(G,pos,node_list=places,node_color='b')
            #print(d_post)
df_1=pd.read_csv('like.csv')
d_likedby={}
l=[l for l in d_post.keys()]
print l
print('posted by')
print(d_post)

#print(l)

#like section
for i in range(1):
    for d in l:
        list_post=d_post[d]
        
        for j in range(len(list_post)):
            _list=list_post[j][0]
            print _list
            if d_likedby.has_key(_list) == 0:
               d_likedby.setdefault(_list,[d])
            else:
                x=d_likedby.get(_list)
                x.append(d)
                d_likedby[_list]=x

d_likedbyListkeys=[i for i in d_likedby.keys()]


for x in range(20):
    pid_like=df_1.pid[x]
    for j in d_likedbyListkeys:
        if pid_like==j:
            #print(df_1.name[x])
            y=d_likedby.get(j)
            y.append(df_1.name[x])
            d_likedby[j]=y
            nodename = d_post.get(d_likedby.get(j)[0])[0][1]
            labeldict[df_1.name[x]]=df_1.name[x]
            map_value.setdefault(df_1.name[x],0.5)
            edge_list.append((nodename,df_1.name[x]))
            #G.add_node(df_1.name[x])
            #G.add_edge(nodename,df_1.name[x])
                     
print("Liked by")
print(d_likedby)
#comment section
#print(sum(len(v) for v in d_likedby.itervalues()))
df_2=pd.read_csv('comment.csv')
d_commentby={}
l1=[l1 for l1 in d_post.keys()]
#print(l)

for i in range(1):
    for d in l1:
        list_post=d_post[d]
        for j in range(len(list_post)):
            _list=list_post[j][0]
            if d_commentby.has_key(_list) == 0:
               d_commentby.setdefault(_list,[d])
            else:
                x=d_commentby.get(_list)
                x.append(d)
                d_commentby[_list]=x

d_commentbyListkeys=[i for i in d_commentby.keys()]

for x in range(20):
    pid_like=df_2.pid[x]
    for j in d_commentbyListkeys:
        if pid_like==j:
            y=d_commentby.get(j)
            y.append(df_2.name[x])
            d_commentby[j]=y
            nodename = d_post.get(d_commentby.get(j)[0])[0][1]
            labeldict[df_2.name[x]]=df_2.name[x]
            map_value.setdefault(df_2.name[x],0.7)
            edge_list.append((nodename,df_2.name[x]))

print("Commented by")
print(d_commentby)
print("labeldict")
print(labeldict)

G.add_edges_from(edge_list)
#creating liked by nodes
#print(nodename)
#nx.draw(G,pos=None,node_color=range(24),node_size=800,cmap=plt.cm.Blues,with_labels = True)
#nx.draw_networkx_nodes(G,pos=None,node_list=['sgsg'],font_size=16,font_color='red')
values = [map_value.get(node, 0.25) for node in G.nodes()]
nx.draw(G, cmap=plt.get_cmap('jet'), node_color=values, with_labels = True)

plt.savefig('facebook.jpg')

plt.show()
#retriving graph nodes for results
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


print placelengths
#sum1 = sum([len(v) for v in count_list_post.values()])

#print sum1

for i,j in zip(places,placelengths):
    #print i,j
    post = post+i+' = '+str(j)+'<br>'
#print post

#count = placelengths.count


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
print (count_list_postby)

postlengths = [len(v) for v in count_list_postby.values()]

#print postlengths
postby=''
for i,j in zip(count_list_postby.keys(),postlengths):
    #print i,j
    postby = postby+i+' = '+str(j)+'<br>'
    if j > 5:
        list1 = count_list_postby[i]
        for a in range(j):
            if list1[a] in places:
                print(list1[a])
            elif list1[a]==i:
                print(list1[a])
            else:
                recommend.append(list1[a])

print recommend
'''

for k in nx.all_neighbors(G,'Rob Zwerling'):
    print k'''
          
            
        
        
        
        
    


#html code
f = open('helloworld.html','w')

message = """<html>
<head></head>
<body><center><h1>Facebook Analysis Report</h1></center>
<br>
<table border=1>
<tr>
<th>
<center>
FACEBOOK
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
<img src="facebook.jpg">
</td>
<td>Number of Post for the following places:<br>""" + post 

xyz="""<br>Number of likes and comments to a user <br>""" +postby 
abc= """
</td>

""" 
pqr =  """
</td>
</tr>
""" 
#print abc
message = message + xyz
messsage = message+abc 

lmn = """<td><br>Recommend following people <br>""" 
for i in recommend:
    lmn = lmn + i + '<br>'
    
message = message +lmn
message = message +pqr
#print message 
f.write(message)
f.close()

#webbrowser.open_new_tab('helloworld.html')

#webbrowser.open_new_tab('helloworld.html')




'''import networkx as nx
import matplotlib.pyplot as plt
labeldict = {}
G=nx.Graph()

G.add_node("Goa")
G.add_node("Karnataka")
G.add_node("Matheran")


G.add_node(d_post.get('goa')[0][1])
labeldict[d_post.get('goa')[0][1]]=d_post.get('goa')[0][1]

#G.add_nodes_from()
labeldict["Goa"] = "goa"
labeldict["Matheran"] = "matheran"
labeldict["Karnataka"] = "Karnataka"

nx.draw(G,labels=labeldict, with_labels = True)
plt.show()
'''