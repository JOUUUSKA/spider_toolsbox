# 安装指南 

## 1、安装依赖
```python  
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python==4.3.0.38 
```
```python  
pip install spider_toolsbox  
```
要使用spider_toolsbox里面的验证码识别模块需要cv2依赖库，  
这个库安装有一些坑，  
但是只要复制执行上面的安装指令即可绕过。  

## 2、实例化
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()  
```
  
# 使用指南  

**声明**  
为方便Crawler发送请求，  
此库中所有和请求相关的API都已默认使用fakeUA库内置UserAgent，  
不需要在网页上或三方库内获取设置UA，  
各位如需自定义headers，按正常步骤设置即可。
 
## 一、识别验证码  

**1、识别英文＋数字验证码**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()   

spidertool.ocr_img(img_path)
```
返回给图片中显示的验证码  

**2、识别滑块验证码**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()  
  
spidertool.ocr_slide_with_hole(bgimg_path, fullpage_path)
```
返回图片中显示的滑块图缺口坐标  

**3、识别点选验证码**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.ocr_click_choose(test_img_path, result_img_path)
```
返回图片中显示的 点选验证码 所在坐标  

## 二、下载系列

**1、下载视频**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.download_video(url)
```
**2、下载图片**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.download_img(url)
```
**3、下载文本**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.download_character(url)
```

## 三、快捷操作

**1、快速打开JS文件**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.open_js(js_file)
```
**2、快速创建一个时间戳**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.create_timestamp(js)
```
**3、快速创建一个随机字符串**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.create_random_str()
```

**4、快速创建UA**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.create_headers()
```

**5、快速定位元素**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.re(res, str_1, str_2)
```

## 四、发送各类请求
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.get()
spidertool.post()
spidertool.head()
spidertool.options()
spidertool.put()
spidertool.patch()
spidertool.delete()
```

## 五、重构response
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.rebuidtext(res)
```

## 六、JSON系列
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.json_loads(data)
spidertool.json_load(data)
spidertool.json_dumps(data)
spidertool.json_dump(data)
```

## 七、美化控制台输出格式
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.info()
spidertool.debug()
spidertool.warning()
spidertool.error()
```

## 八、常用装饰器
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

@spidertool.catch_bug
def test1:...

@spidertool.test_time
def test2:...

@spidertool.retry(max_attempts: int, delay)
def test3:...
```  

# 解答  

若是对此项目中的**API存疑**，  
可**鼠标中键**点击进入项目内部**查看源码注释**，  
笔者已做好**详细的注释**供各位参考  
若还不清楚，可通过电子邮箱联系作者**1393827820@qq.com**    

# 制作初衷  

自己玩爬虫有一段时间了，<br>
在制作爬虫的过程中，<br>
发现很多好用的三方库，<br>
也发现很多繁琐，复杂的代码编写操作。<br>
为了方便爬虫er们，<br>
笔者在此对这些操作进行合并与精简，<br>
希望借此能为各位扫清一些前行道路上的障碍，<br>
故甘为献丑，分享这些微不足道的东西，<br>
请各位不吝赐教，笔者会尽全力修改issue，<br>
如各位能看得上，无妨点上一个star。<br>
提此，共勉！！！<br>



