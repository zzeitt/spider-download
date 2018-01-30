from selenium import webdriver
from time import sleep
from urllib.request import urlopen
from urllib.request import urlretrieve
from tqdm import *


# ***************************************【爬取视频链接】***************************************
# **********************************************************************************************

# -----------------【定义获取链接函数】-----------------
# ------------------------------------------------------
def get_video_link(page_url): # 用Chrome打开并获取视频下载链接的函数
	# 初始化浏览器为手机模式
	mobileEmulation = {'deviceName':'iPhone 6'}
	options = webdriver.ChromeOptions()
	options.add_experimental_option('mobileEmulation',mobileEmulation)
	browser = webdriver.Chrome(chrome_options=options)
	# 定位iframe
	url = page_url # 本函数唯一传入的参数
	browser.get(url)
	sleep(1)
	element_iframe = browser.find_element_by_class_name('video_iframe') # iframe没有name或id时先定位到该iframe元素，再传入switch中
	browser.switch_to.frame(element_iframe)
	# 找到下载链接
	element_video = browser.find_element_by_class_name('tvp_video').find_element_by_id('tenvideo_video_player_0')
	video_link = element_video.get_attribute('src')
	# 关闭浏览器，返回链接
	browser.close()
	return video_link


# ************************************【对视频链接进行下载】************************************
# **********************************************************************************************

# -------------------【进度条加下载】-------------------
# ------------------------------------------------------
class TqdmUpTo(tqdm): # 官方写好的类
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize

def download(address,filename,url,filesize): # [下载过程封装为函数]
    ''' [About args]:
    address: 	文件存放的地址 	eg. 「D:\example」
    filename: 	含后缀的文件名	eg. 「emmmmm.txt」
    url: 		文件所在的链接	eg. 「http://www.baidu.com」
    filesize: 	文件大小（MB）	eg. 「**MB」
    '''
    path = address+'\\'+filename # 文件地址之烦人的反斜杠
    print("\nBegin ["+filename+"]("+filesize+")»»["+path+"]")
    with TqdmUpTo(unit="B", unit_scale=True, unit_divisor=1024,miniters=1,ncols=75,
              desc="Downloading → ["+filename+"]("+filesize+") ") as t:
        urlretrieve(url,path,reporthook=t.update_to, data=None)
    print("\n["+filename+"]"+" ← Completed!\n")

# ---------------------【正式下载】---------------------
# ------------------------------------------------------
if __name__ == '__main__':
	# 打招呼
    print("\nGlad to help you! Let's start downloading 「Wechat-Video」now. \n")
    # 获取输入
    address = input("Input the store-address(eg.「D:\example」): ")
    video_name = input("Input the video file name(eg.「emm.mp4」): ")
    url = input("Paste the page-URL here(eg.「http://mp.weixin.qq.com/s/1234657890123456798012」): ")
    video_size = '*'
    # 以防手抖
    key = input("\nAre you sure download ["+video_name+"]("+video_size+")»»["+address+'\\'+video_name+"] (y/n):")
    if key == 'y':
        print("\nLet's begin! \n")
        video_link = get_video_link(url)
        download(address,video_name,video_link,video_size)
    else:
        print("\nOK, goodbye! \n")