dogemsg
=======

嘛大概就是想做一个<del>有趣的</del>且安全的通讯工具.

尽可能的削减服务器的功能. 目前就是提供一个收/存取信息的API, 一个保存用户信息(用户名及相关信息)的API, 以及一个保存用户好友列表(用public key加密)的API.

用户的身份识别由ECC生成的keypair来完成, 对用户身份的校验就是以private key签名的指定信息可以被public key正确解密. 双方的信息完全被加密,暴露出的仅仅是来源及去向(我们也想做到更好啊QwQ).
在双方能够保证身份确认的情况下, 可以在发起一个request, 交换IP以完成p2p的连接, 然后使用AES进行加密, 从而保证安全.

#计划

目前实现了的部分:


`api.php`

收/存取信息的API

删除冗余信息的API(待完善身份验证)


`dogemsg.ui`

客户端UI设计(prototype) 


仍需实现:

对用户信息的保存

对用户列表的保存


客户端核心代码(加密解密,生成keypair等)(决定使用`pyelliptic`)


#更新日志


###2014/07/16

完成了对API的初步设计

仍需要更新对SQL注入的保护 以及对身份校验的完成


###2014/07/17

随便画了一个UI(ry

本来想用RSA 但是因为publickey 太 <del>他 妈</del>长了 改用ECC

python3的decode真他喵难用啥

找不到一个合适的php ecc库 QwQ

最后决定在php里以system的形式调用python. auth的部分解决.

目前的校验方式是, 以private key签名, 同时将signature和message发至服务器验证身份

signature的生成 `key.sign(msg)`

校验:`ECC(pubkey = public_key).verify(signature, msg)`


###2014/07/18

`sendmessage`基本实现完成
<del>`receive` 校验部分仍待实现</del>

ok Server端基本撸完 下午完善client 然后开始GUI开发

`receive`校验部分完成, 最后将返回一个包含所有信息的list
(之前若msg是中文的话会有bug, 果断encode, 解决问题)

下午将函数封装, 并且初步完成一个命令行下的客户端.

函数基本上弄的差不多了

主要的函数都在`operators.py`里.

添加了一个保存keypair的功能 添加的时候发现这个功能其实特别的自然, 其实是之前的设计问题吧.

添加了一个Class:`Contact`, 用以存放联系人信息.

接下来的主要任务: 

1.先撸出一个本地的friendlist的存取和维护.
2.完成一个对config的读取和维护.

与此同时还实现了对message structure的完善, 接下来所有的信息发送都将完成的被纳入所定义的信息结构体系中.

还需要实现的是将收回的信息按照相同联系人分配. 其实还是先撸完friendlist再说啦.

