# wpa-dictionary

用于 Wi-Fi 密码破解。

### Linux 篇（推荐）

* 使用相应包管理工具安装，例如 Debian/Ubuntu 使用 apt 安装：

~~~shell
sudo apt install aircrack-ng
~~~

待续...

## MAC OS 篇

### 1. 查看网卡名称

在终端中执行 `ifconfig` 即可查看，通常是 en0

### 2. 使用 airport 监听无线网络

由于某些原因，airmon-ng 无法在 MAC OS 使用，所以只能使用 airport 进行扫描和抓包了，但是并不好用，所以还是使用 linux 吧尽量...

开始扫描，终端中执行：

~~~shell
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport en0 scan
~~~

扫描结果会是这样的：

| SSID | BSSID | RSSI | CHANNEL | HT | CC | SECURITY (auth/unicast/group) |
| - | - | - | - | - | - | - |
| 小米手机 | 22:47:da:62:2a:f0 | -29 | 6 | Y | -- | WPA2(PSK/AES/AES) |

* SSID 表示 Wi-Fi 名称
* BSSID 表示 Wi-Fi 设备的硬件地址
* RSSI 表示信号强度，值是负数，绝对值越小信号越强
* CHANNEL 表示 Wi-Fi 信道
* HT 表示吞吐量模式，一般都为 Y
* CC 表示国家，中国为 CN
* SECURITY 表示加密方式

### 3. 使用 airport 进行抓包

~~~shell
sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport en0 sniff
~~~

抓一段儿事件之后，使用 Ctrl + C 停止抓包，完成后会生成一个 cap 包，看到如下提示：

~~~
Session saved to /tmp/airportSniff0RjCAO.cap.
~~~

### 4. 安装 [aircrack-ng](https://aircrack-ng.org/)

* 使用 [Homebrew](https://brew.sh/) 安装：

~~~shell
brew install aircrack-ng
~~~

### 5. 使用 aircrack-ng 执行破解

~~~shell
aircrack-ng -w huanying-0.txt /tmp/airportSniff0RjCAO.cap
~~~

### Windows

* [下载 Aircrack-ng](https://aircrack-ng.org/downloads.html) 提供了 Windows 的二进制包

* 使用 [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)

### 更多安装方式参考：[安装 Aircrack-ng](https://aircrack-ng.org/install.html)

## 2. 
