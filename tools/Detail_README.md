# 安装指南 

## 1、安装依赖
见spider_toolsbox/README.md  
# 使用指南  

**声明**  
此篇readme是用于详细讲解每一个api的使用，  
如果是不需要将源码打包，那么个人建议按照列表的readme去使用即可，  
如果需要打包源码，那么考虑到内存，最好是用什么import什么， 
各位按需所取即可。  
以上！ 
 
## 一、识别验证码  

**1、识别英文＋数字验证码**
```python  
from spider_toolsbox.tools.ocr.ocrer import ocr_img

result = ocr_img(img_path)
```
返回给图片中显示的验证码  
<br>---------------------------------------------------------------------------------------------------------------------------------<br>


**2、识别滑块验证码**  

一张图为带坑位的原图，如下图

![Test](https://cdn.wenanzhe.com/img/bg.jpg) 

一张图为原图，如下图 

![Test](https://cdn.wenanzhe.com/img/fullpage.jpg) 
```python  
from spider_toolsbox.tools.ocr.ocrer import ocr_slide_with_hole

result = ocr_slide_with_hole(bgimg_path, fullpage_path)
```    
返回图片中显示的滑块图缺口坐标
<br>---------------------------------------------------------------------------------------------------------------------------------<br>
小滑块为单独的png图片，背景是透明图，如下图

![Test](https://cdn.wenanzhe.com/img/b.png) 

然后背景为带小滑块坑位的，如下图 

![Test](https://cdn.wenanzhe.com/img/a.png) <br>
```python  
from spider_toolsbox.tools.ocr.ocrer import ocr_slide_with_clean

result = ocr_slide_with_clean(bgimg_path, fullpage_path)
```   
返回图片中显示的滑块图缺口坐标
<br>---------------------------------------------------------------------------------------------------------------------------------<br>

**3、识别点选验证码**  

![Test](https://cdn.wenanzhe.com/img/0446fe794381489f90719d5e0506f2da.jpg) 

![Test](https://cdn.wenanzhe.com/img/6175e944c1dc408a89aabe4f7fc07fca.jpg) 

![Test](https://cdn.wenanzhe.com/img/20211226135747.png) 

![Test](https://cdn.wenanzhe.com/img/f34390d4911c45ce9058dc2e7e9d847a.jpg) 
```python  
from spider_toolsbox.tools.ocr.ocrer import ocr_click_choose

result = ocr_click_choose(test_img_path, result_img_path)
```
返回图片中显示的 点选验证码 所在坐标  

## 二、下载系列

**1、下载视频**
```python  
from spider_toolsbox.tools.download.downloader import download_video

download_video(url)
```
**2、下载图片**
```python  
from spider_toolsbox.tools.download.downloader import download_img

download_img(url)
```
**3、下载文本**
```python  
from spider_toolsbox.tools.download.downloader import download_character_by_response_xpath

download_character_by_response_xpath(url, xpath)
```  
**4、下载附件**
```python  
from spider_toolsbox.tools.download.downloader import download_file

download_file(url, file_name, file_type)
```  
**5、下载其他**
```python  
from spider_toolsbox.tools.download.downloader import download_others

download_others(others)
```

## 三、快捷操作

**1、快速打开JS文件**
```python  
from spider_toolsbox.tools.other_tools.other_tools import open_js   

open_js(js_file_path)
```
**2、快速创建一个时间戳**
```python  
from spider_toolsbox.tools.request.info import create_timestamp   

create_timestamp()
```
**3、快速创建一个随机字符串**
```python  
from spider_toolsbox.tools.request.info import create_random_str

create_random_str()
```

**4、快速创建UA**
```python  
from spider_toolsbox.tools.request.info import create_headers

create_headers()
```  
```python  
from spider_toolsbox.tools.request.info import create_default_headers

# 因为create_headers创建的请求头是使用random随机创建，所以可能是移动端的请求头
# 可能导致和web端的页面xpath结构不一致，导致锁定不了页面元素
# 所以可以使用create_default_headers方法，返回一个web端的请求头
# 并且使用fakeua库之后，打包出来的exe文件体积会比较大，
# 所以如果请求头校验不是很严格，建议使用create_default_headers
create_default_headers()
```  
```python  
from spider_toolsbox.tools.request.info import ua_pool

random_ua = ua_pool.random
chrome_ua = ua_pool.chrome
firefox_ua = ua_pool.firefox
```  

**5、快速通过xpath获取元素链接**
`extract_link_by_response_xpath`传入的`response`，  
必须是`spider_toolsbox`里面的`create_request`，  
或者是`scrapy`里面的`response`，  
否则报错！  

**create_request**用法见: **四、发送各类请求**  
```python  
from spider_toolsbox.tools.request.client import create_request
from spider_toolsbox.tools.link_extractors.html_response import extract_link_by_response_xpath

response = create_request(url)
extract_link_by_response_xpath(response, xpath="//a") # 得到xpath中 a标签中的链接
```  

**6、快速通过xpath获取元素内容**
```python  
from spider_toolsbox.tools.request.client import create_request
from spider_toolsbox.tools.link_extractors.html_response import extract_text_by_response_xpath

response = create_request(url)
extract_text_by_response_xpath(response, xpath="//a") # 得到xpath中 a标签中的文本
```  

## 四、发送各类请求  
请求方式有三种类型: 同步请求、异步请求、会话请求  
分别用形参的req_mode="Request"、req_mode="SessionRequest"、req_mode="AsyncRequest"进行初始化   
  

**特殊的**, 初始化异步函数时，  
在初始化后需要手动执行load_async方法，  
load_async方法是一个异步函数，所以同时用await挂起。  
```python  
from spider_toolsbox.tools.request.client import create_request   
from spider_toolsbox.tools.request.info import create_headers
from spider_toolsbox.tools.request.models import run_script

url = "https://www.baidu.com"
headers = create_headers()

def test_Request_create_request():
    req_mode1 = "Request"
    urequest1 = create_request(url=url, req_mode=req_mode1, headers=headers)
    assert urequest1.xpath("//title/text()").get() == "百度一下，你就知道"


def test_Session_Request_create_request():
    req_mode2 = "SessionRequest"
    urequest2 = create_request(url=url, req_mode=req_mode2, headers=headers)
    assert urequest2.xpath("//title/text()").get() == "百度一下，你就知道"



async def test_Async_Request_create_request():
    req_mode3 = "AsyncRequest"
    urequest3 = create_request(url=url, req_mode=req_mode3, headers=headers)
    await urequest3.load_async()
    assert urequest3.xpath("//title/text()").get() == "百度一下，你就知道"


async def main():
    test_Request_create_request()
    test_Session_Request_create_request()
    await test_Async_Request_create_request()

if __name__ == '__main__':
    run_script(main)
```

## 五、重构response
```python  
from spider_toolsbox.tools.other_tools.other_tools import rebuidtext    

rebuidtext(res)
```  

## 六、美化控制台输出格式
```python  
from spider_toolsbox.tools.log.logger import info, debug, warning, error, success, critical, exception

info()
debug()
warning()
error()
success()
critical()
```

## 七、常用装饰器
```python  
from spider_toolsbox.tools.wapper.wappers import catch_bug, test_time, retry    

catch_bug
def test1:...

test_time
def test2:...

retry(max_attempts, delay)
def test3:...
```  

## 九、常用加密类型  
### **使用说明**:
除RSA、SHA系列以外的加密模式，  
填充类型统一设定为**PKCS7**  
RSA的填充模式可选有**pkcs1_v1_5**和**PKCS1_OAEP**， 默认为**pkcs1_v1_5**  
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
from spider_toolsbox.tools.cryptools.cryptor import AESCipher  
cryptor = AESCipher()

cryptor.encrypt_AESCBC(data, key, iv)
cryptor.decrypt_AESCBC(encoded_ciphertext, key, iv)

cryptor.encrypt_AESECB(data, key)
cryptor.decrypt_AESECB(encoded_ciphertext, key)
```  
**2、DES系列**
```python  
from spider_toolsbox.tools.cryptools.cryptor import DESCipher  
cryptor = DESCipher()  

cryptor.encrypt_DESCBC(data, key, iv)
cryptor.decrypt_DESCBC(encoded_ciphertext, key, iv)

cryptor.encrypt_DESECB(data, key)
cryptor.decrypt_DESECB(encoded_ciphertext, key)
```  
**3、RSA系列**
```python  
from spider_toolsbox.tools.cryptools.cryptor import RSACipher  
cryptor = RSACipher()    

cryptor.encrypt_RSA(data, pubkey)
cryptor.decrypt_RSA(data, privkey)
```  
**4、SHA系列**
```python  
from spider_toolsbox.tools.cryptools.cryptor import SHACipher  
cryptor = SHACipher()    

cryptor.encrypt_MD5(data)
cryptor.encrypt_SHA1(data)
cryptor.encrypt_SHA256(data)
cryptor.encrypt_SHA384(data)
cryptor.encrypt_SHA512(data)
```  
**5、BASE64**
```python  
from spider_toolsbox.tools.cryptools.cryptor import Base64Encoder  
cryptor = Base64Encoder()    

cryptor.encrypt_Base64(data)
```  
**6、HMAC**
```python  
from spider_toolsbox.tools.cryptools.cryptor import SHACipher  
cryptor = SHACipher()   

cryptor.encrypt_HMAC(data, key, digestmod)
```  
**7、PBKDF2**
```python  
from spider_toolsbox.tools.cryptools.cryptor import SHACipher  
cryptor = SHACipher()  

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



