# 安装指南 

## 1、安装依赖
```python  
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python==4.3.0.38 
```
```python  
pip install git+https://github.com/JOUUUSKA/spider_toolsbox.git
```
要使用spider_toolsbox里面的验证码识别模块需要cv2依赖库，  
cv2这个库安装有一些坑，  
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
<br>-------------------------------------------------------------------------------------------------------------------------------------------------------<br>

**2、识别滑块验证码**  

一张图为带坑位的原图，如下图

![Test](https://cdn.wenanzhe.com/img/bg.jpg) 

一张图为原图，如下图 

![Test](https://cdn.wenanzhe.com/img/fullpage.jpg) 
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()  
  
spidertool.ocr_slide_with_hole(bgimg_path, fullpage_path)
```    
返回图片中显示的滑块图缺口坐标
<br>-------------------------------------------------------------------------------------------------------------------------------------------------------<br>
小滑块为单独的png图片，背景是透明图，如下图

![Test](https://cdn.wenanzhe.com/img/b.png) 

然后背景为带小滑块坑位的，如下图 

![Test](https://cdn.wenanzhe.com/img/a.png) <br>
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()  
  
spidertool.ocr_slide_with_clean(bgimg_path, fullpage_path)
```   
返回图片中显示的滑块图缺口坐标
<br>-------------------------------------------------------------------------------------------------------------------------------------------------------<br>

**3、识别点选验证码**  

![Test](https://cdn.wenanzhe.com/img/0446fe794381489f90719d5e0506f2da.jpg) 

![Test](https://cdn.wenanzhe.com/img/6175e944c1dc408a89aabe4f7fc07fca.jpg) 

![Test](https://cdn.wenanzhe.com/img/20211226135747.png) 

![Test](https://cdn.wenanzhe.com/img/f34390d4911c45ce9058dc2e7e9d847a.jpg) 
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

spidertool.download_character(txt)
```

## 三、快捷操作

**1、快速打开JS文件**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.open_js(js_file_path)
```
**2、快速创建一个时间戳**
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

spidertool.create_timestamp()
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
spidertool.success()
spidertool.critical()
```

## 八、常用装饰器
```python  
from spider_toolsbox.spidertools import SpiderTools
spidertool = SpiderTools()    

@spidertool.catch_bug
def test1:...

@spidertool.test_time
def test2:...

@spidertool.retry(max_attempts, delay)
def test3:...
```  

## 九、常用加密类型  
### **使用说明**:
加密模式的填充类型统一设定为**PKCS7**  
加密类型中只有 **SHA系列，HMAC。PBKDF2** 的输出格式只能为hex固定格式  
其他的加密类型都能 自行指定 输出格式为base64或者hex  

**加密函数的 形参 中**  
指定output_format='hex'则输出为hex返回值，  
指定output_format='base64'则输出为base64返回值  

**解密函数的 形参 中**  
指定input_format='hex'则输出为hex返回值  
指定input_format='base64'则输出为base64返回值
### **使用示例**
**1、AES系列**
```python  
from cryptools import Cryptor
cryptor = Cryptor()  

cryptor.encrypt_AESCBC(data, key, iv)
cryptor.decrypt_AESCBC(encoded_ciphertext, key, iv)

cryptor.encrypt_AESECB(data, key)
cryptor.decrypt_AESECB(encoded_ciphertext, key)
```  
**2、DES系列**
```python  
from cryptools import Cryptor
cryptor = Cryptor()   

cryptor.encrypt_DESCBC(data, key, iv)
cryptor.decrypt_DESCBC(encoded_ciphertext, key, iv)

cryptor.encrypt_DESECB(data, key)
cryptor.decrypt_DESECB(encoded_ciphertext, key)
```  
**3、RSA系列**
```python  
from cryptools import Cryptor
cryptor = Cryptor()   

cryptor.encrypt_RSA(data, pubkey)
cryptor.decrypt_RSA(data, privkey)
```  
**4、SHA系列**
```python  
from cryptools import Cryptor
cryptor = Cryptor()   

cryptor.encrypt_MD5(data)
cryptor.encrypt_SHA1(data)
cryptor.encrypt_SHA256(data)
cryptor.encrypt_SHA384(data)
cryptor.encrypt_SHA512(data)
```  
**5、BASE64**
```python  
from cryptools import Cryptor
cryptor = Cryptor()   

cryptor.encrypt_Base64(data)
```  
**6、HMAC**
```python  
from cryptools import Cryptor
cryptor = Cryptor()   

cryptor.encrypt_HMAC(data, key, digestmod)
```  
**7、PBKDF2**
```python  
from cryptools import Cryptor
cryptor = Cryptor()  

cryptor.encrypt_PBKDF2(password, salt)
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



