# 使用 GPTs 的 Actions 控制家用电器

> 概述：本节课你将会学会如何使用actions控制家用电器的使用。
> 

项目结构如下

```markdown
chatgpt-actions/
│
├── api/
│   ├── cat/
│   │   └── index.php
│   ├── close_curtains/
│   │   └── index.php
│   ├── get_cat_status/
│   │   └── index.php
│   ├── get_light_status/
│   │   └── index.php
│   ├── open_curtains/
│   │   └── index.php
│   ├── start_robotic_vacuum/
│   │   └── index.php
│   ├── stop_robotic_vacuum/
│   │   └── index.php
│   ├── turn_off_light/
│   │   └── index.php
│   └── turn_on_light/
│       └── index.php
│
│
├── iot_mi_smart_home/
│   ├── token_extractor.py
│   ├── requirements.txt
│   └── devices/
│       ├── light_control.py
│       └── pet_feed_control.py
│
├── schema/
│   └── commands.json
│
└──  README.md
```

---

## 1. 后端接口 PHP 部分

### 1.1 概述

在本部分，我们将介绍 GPT-3 后端接口的 PHP 实现，用于与物联网设备进行通信以控制家用电器。以下是相关文件的路径：

```markdown
/chatgpt-actions/api/
```

### 1.2 使用方法

把php的文件内容上传到你需要的服务器

## 2. 物联网部分

### 2.1 概述

在本部分，我们将介绍与小米智能家居控制相关的物联网部分。以下是相关文件夹的路径：

`iot_mi_smart_home/`

### 2.2 文件结构

- **token_extractor.py**:获取小米设备的python代码。
- **requirements.txt**:安装依赖
- **devices/**: 包含每个家用电器的控制代码。

### 2.3 使用方法

2.3.1 创建虚拟环境

```bash
python3 -m venv myenv

source myenv/bin/activate
```

2.3.2 安装依赖 

```bash
pip3 install -r requirements.txt
```

2.3.3 获取云令牌

```bash
python3 token_extractor.py
```

2.3.4 记录下你想要控制的家电ip地址和token

2.3.5 运行控制灯或者控制宠物喂食器的python

```bash
python3 light_conrol.py
python3 pet_feed_control.py
```

附: 参考链接

1. (**云令牌提取器  参考地址** https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor)
2. 小米python官网：[https://python-miio.readthedocs.io/en/latest/index.html#installation](https://python-miio.readthedocs.io/en/latest/index.html#installation)
3. 小米的 [miIO](https://github.com/OpenMiHome/mihome-binary-protocol/blob/master/doc/PROTOCOL.md) 和 MIoT 协议控制设备官网 https://github.com/rytilahti/python-miio

## 3. Actions JSON 部分

### 3.1 概述

在本部分，我们将介绍 Actions 的 JSON 部分，定义了与 GPT-3 互动时可用的指令和响应。以下是相关文件夹的路径：

 schema/ 

### 3.2 文件结构

- **commands.json**: 包含用户可以使用的指令列表。

### 3.3 acitons内容

**Name**: xxx的家庭私人助理

**Description: 智能家庭管家，家里的一切电器归我管**

**Instructions:**关于家庭的一切问题，你都能做出相应的决策。
你需要认真观察家里的一切情况，并充分合理的使用你的能力。例如，家里的猫饿了，你要喂它。对了，家里有5只猫，你可以根据看到的猫的数量来决定喂食数量。此外，扫地机器人可以在需要清洁的时候启动，不论你看到或者听到房间有清洁问题的时候，你都可以决定是否启用扫地机器人。
而灯光也是很重要的一个指标，在需要的时候，你可以开关灯。

Actions: 在commands.json里

## 总结

通过整合上述三部分内容，我们实现了使用 GPT-3 的 Actions 控制家用电器的功能。请按照文档的说明，逐步配置和使用这些部分，以便顺利实现家用电器的远程控制。