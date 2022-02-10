# game_robot

国内gitee镜像：https://gitee.com/ly674/game_robot
## Introduction - 介绍
windows下游戏脚本工具

### Summary - 概要
目前市面上做脚本的基本都是按键精灵，然后就是一些易语言的工具。当然也有人用网易airtest做脚本。但是大都是基于window下一些按键之类的操作，同时也需要游戏进程处于活跃，无法去做别的事情，所以我自己写了这个基于win32层的脚本脚手架

## Requirements
对游戏的一些操作用的win32，pyqt做了一个简单的界面，opencv做的图像识别，加入了websocket做推送

## Development
目前这个脚本主要在做九阴真经ol的一些功能，不过由于个人时间目前不太够了，就把这个开源了。
当初在设计结构的时候考虑到了游戏移植，所以剥离了功能和整体框架的关系，并不影响对其他游戏同等脚本功能的开发。

### 九阴
目前对九阴这款游戏来说，已经完成了团练，授业，挂机，采集，自动接杀手的功能，自动琴和拉镖之前有做，不过做到一半后来有点事就放弃了。

### Dos - 文档


### Contact
qq群：978098280

## License
 
This project is licensed under the MulanPSL2 License - see the [LICENSE.md](LICENSE.md) file for details
