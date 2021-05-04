#firebase 
Basics:
Firebase is designed for speed and not complexity so
1. keep data as shellow as possible, no nested data. why? becose when you try to read any entry it reads complte data
under it! so if any dynamic data present then it will read that too so sperate dynamic and static data.
eg. users->AccountInfo (static data)
         ->Comments (dynamic Data grows over time)
Wrong Way, reading AccountInfo will read all comments tooo!
eg. users->AccountInfo (static data)->Comments (dynamic Data grows over time)

2: use db import export initally to create databse


