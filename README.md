# video-danmaku-mask
项目模仿了 bilibili 防挡弹幕效果
![](./intro.gif)

## 目录结构
```
.
├── binarysearchtree.js          // 二分查找法查询最匹配 mask
├── cxk.mp4                      // 视频素材
├── cxk.png              
├── maskdanmakuvideo.html        // 主页面
├── masksvg.js                   // 根据 bilibili 的请求生成的蒙版素材库 js 数据结构
├── maskurltosvgbase64           // 根据 bilibili 的请求生成的蒙版素材库
│   ├── Makefile
│   ├── main.go                  // 解压 bilibili 响应结果,得到所有蒙版
│   ├── maskurl.txt              // 指定 bilibili 请求 url
│   ├── maskurltosvgbase64.py    // 根据 bilibili 请求 url 下载蒙版数据
│   └── svgjs                    // 生成的 js 数据, 也就是 ./masksvg.js 文件的来源
│       └── 1715149827.js
└── svgurltoimage                // 根据 bilibili 请求生成 svg 图片
    ├── base64tosvg.py
    └── svg.txt
```

## 使用
### 直接看效果
目前测试项目可以直接使用, 直接启动文件服务器即可, 比如本项目使用 python 方式
```
make run
```
接着就可以在浏览器中,访问地址
```
http://localhost:8001/maskdanmakuvideo.html
```
### 重新生成蒙版数据
如果需要重新生成蒙版数据,则需要先根据 bilibili 请求生成蒙版的帧数据, 进入 maskurltosvgbase64 目录, 执行
```
make build
```
就会看到目录下生成了 svgjs 的目录, 把其中生成的文件移动到根目录下, 重命名成`masksvg.js`即可

### 换一个视频和蒙版
需要自己修改代码


## bilibili 防挡弹幕.webmask 文件格式解压
这里是直接参考了 [B-webmask](https://github.com/dreamCodeMan/B-webmask?tab=readme-ov-file) 的实现  


文件可分为头部和内容两部分
头部格式

name | desc | type | bytes | offset
---- | --- | --- | --- | ---
tag | 文件类型标识符，目前固定为 MASK, 4个字节 |bytes | 4 | 0
version | 版本号，目前为 1 | Int32 | 4 | 4
check code | 校验码？目前为 2 | Int8 | 1 | 8
segments | 所包含段数，每段时间10秒左右, 一个 3 分钟的视频大概会分成 18 段 | Int32 | 4 | 12
segments meta | 段的元数据，每段包含 16 个字节, 前 8 个字节表示时间，后 8 个字节表示数据 offset | bytes | 16 * segments | 16

B 站 .webmask 文件加载流程：

1. 通过 range 头进行分段加载；首先加载前 0-16 字节(理论上只需读取 0-15 前 16 字节即可)，校验文件类型
2. 校验成功，加载 16-(segments * 16) 字节元数据并进行解析
3. 下载后续最多不超过 22 段的数据，通过 pako 进行解压，根据当前视频播放时间从中选择蒙版进行渲染
4. 大部分视频不会超过 22 段(22 * 10 / 60 约 3 分钟)，超过的话，会按需继续加载后面的数据(每次最多不超过 22 段)


例子：
超过 22 段
// https://www.bilibili.com/video/av21101827

不超过 22 段
// https://www.bilibili.com/video/av46459801


## bilibli 弹幕蒙版和视频同步问题
### timeupdate event 方式
最开始使用的是 h5 的 video 的 [timeupdate_event](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLMediaElement/timeupdate_event)的回调, 但是经过测试,该回调在我机器上一秒内只会触发 5 次左右, 最终的效果是弹幕蒙版和视频有明显延迟. 而且该回调目前并没有提供可以修改触发频率的方式, 所以只能放弃.

### 定时器触发方式
直接使用 js 中的 [setInterval](https://developer.mozilla.org/zh-CN/docs/Web/API/setInterval) 方式, 定时获取视频当前时间点, 然后找到对应的蒙版, 但是最后发现效果不稳定, 研究发现原因是从 bilibili 网站上下载的蒙版本身是有一定频率间隔的. 如果通过定时器触发的方式更换蒙版, 有很大概率定时器的频率无法和 bilibili 蒙版评率对应, 导致了效果不理想.

### 查找最匹配时间点方式
最后使用了 [requestAnimationFrame](https://developer.mozilla.org/zh-CN/docs/Web/API/window/requestAnimationFrame)和递归结合不断地执行蒙版更换的逻辑. 然后每次调用的时候, 根据视频当前时间[currentTime](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLMediaElement/currentTime) 从 bilibili 蒙版素材中查找最匹配的时间点(ms). 最后效果不错