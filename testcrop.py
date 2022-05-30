# import glob
#
# from PIL import Image
# #
# # foo = Image.open('frame1.jpg')
# # w, h = foo.size
# # crop = foo.crop((w/3, h/3, w/2, h/2))
# # crop.save('t.jpg', optimize=True, quality=95)
#
# # files = glob.glob('long/*.jpg')
# # i = 0
# # for filess in files:
# #     print(filess)
# #     i += 1
# #     im = Image.open(filess)
# #     s = im.resize((226, 160), Image.Resampling.LANCZOS)
# #     s.save(f'./scaled/{i}.jpg')
# #
# #
# #
# import datetime
# print(str(datetime.date.today()))
# def isaplha(str, alp=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')):
#     return not alp.isdisjoint(str)
#
# print(isaplha('ППППП'),
# isaplha('123'),
# isaplha('Прр1233'))
# questions = []
# file = open('STAI', 'r')
# for line in file:
#     questions.append(str(line))
#     for i in range(len(questions)):
#         questions[i].replace('\\n', '\n')
# print(questions)
# m = [3, 3, 2, 2, 3, 2, 2, 3, 2, 3, 3, 2, 2, 2, 3, 3, 2, 2, 3, 3]
# a1 = m[0] + m[1] +