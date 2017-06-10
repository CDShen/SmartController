


b = []
b.append({'score':-1.0, 'name':'default'})
b.append({'score':5.0, 'name':'default'})
b.append({'score':2.0, 'name':'default'})
b.append({'score':-5.0, 'name':'default'})


# for i in range(len(b)-1):
#     bOK = True
#     for j in range(0, len(b)-1-i):
#         item = b[j]
#         itemNext = b[j+1]
#         if item.get('score') < itemNext.get('score'):
#             itemTmp = itemNext
#             b[j+1] = item
#             b[j] = itemTmp
#             bOK = False
#     if bOK:
#         break


print (b)

