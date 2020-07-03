# DMcode
##编写初衷
改包是因为py3.8中没有合适的datamatrix码制作工具包从 hubarcode中改过来的,编码方式均为之前没动
主要是因为之前的只适配了2.x

#如何使用
将整个DMcode下载下来
```
from DMcode import DataMatrixEncoder as DME

dme = DME('你想编码的字符')
dme.get_img() #这是编码后返回的PIL.Image格式对象,可以show()展示或save()保存
new_img = dme.refresh('你想编码的字符') #使用refresh(text)函数可以重新编译新的字符返回的是PIL.Image对象

#dme.matrix 这个是编码后的矩阵模式数据 可以frombytes()成图片但是像素点只有1不方便使用
```
