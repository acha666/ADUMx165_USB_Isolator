# ADUMx165 USB Isolator

这是一款 USB 2.0 高速（480Mbps）隔离模块，板载 1 分 4 USB HUB、1A 隔离 DC-DC 电源，并支持外部辅助电源输入，二者可自动切换。

## 项目状态

- [x] 原理图设计
- [x] PCB 设计
- [ ] PCB 制造
- [ ] PCB 验证

## 器件概览

- **[ADUM3165](https://www.analog.com/cn/products/adum3165.html)/[ADUM4165](https://www.analog.com/cn/products/adum4165.html) USB 隔离器**：提供 3.75kV/5.7kV RMS 下的 480Mbps USB 隔离，二者针脚兼容。
- **[SN6505A](https://www.ti.com.cn/product/cn/SN6505A)/[B](https://www.ti.com.cn/product/cn/SN6505B) 变压器驱动器**：直接从上游 USB 端口取电的隔离 DC-DC 电源控制器，二者开关频率不同。
- **[DA2303-AL](https://www.coilcraft.com/en-us/products/transformers/power-transformers/isolation/da230x/da2303-al) 变压器**：1:1.5 SMT 变压器。
- **[TPS2116](https://www.ti.com.cn/product/cn/TPS2116) 电源多路复用器**：优先从下行端口获取 5V 辅助电源，当该电源不可用时，自动切换至板载隔离 DC-DC 电源。
- **[CH334P](https://www.wch.cn/products/CH334.html) USB Hub**：简单的 USB 2.0 一拖四 HUB 芯片。

## 基本电路板参数

| 参数           | 数值              |
|:-------------:|:----------------:|
| **尺寸**       | 50.00mm x 36.50mm |
| **形状**       | 圆角矩形，r=1.50mm |
| **成品板厚**   | 1.60mm            |
| **铜箔层数**   | 4                  |
| **最小线宽**   | 0.12mm             |
| **最小线距**   | 0.12mm             |
| **最小金属化孔径** | 0.20mm          |
| **最小非金属化孔径** | >1.00mm      |
| **最小过孔外径** | 0.45mm            |
| **最小过孔内径** | 0.20mm            |
| **最小金属化槽宽** | 0.60mm         |
| **最小非金属化槽宽** | 无              |
| **特殊制造工艺** | 阻抗控制          |

## 阻抗控制参数

### 差分阻抗 1

| 用途           | USB 2.0 信号       |
|:-------------:|:----------------:|
| **信号层**     | L1, L4            |
| **阻抗**       | 90Ω               |
| **下参考层**   | L2, L3            |
| **上参考层**   | 无                |

| 当前设计参数  | 数值              |
|:-------------:|:----------------:|
| **线宽**       | 0.12mm            |
| **线距**       | 0.12mm            |
| **铜箔厚度**   | 1oz/0.5oz         |
| **适用板厂叠层** | 嘉立创 JLC04161H-3313 |

## 项目说明

本项目使用 KiCad 8.06 进行设计。

已部署 GitHub Action CI/CD，每次提交都会自动执行 DRC 检查，并生成 Gerber 等制造文件。

制造文件可在 [Release 页面](https://github.com/acha666/ADUMx165_USB_Isolator/releases) 下载。

### 电源设计

项目板载 1A 隔离 DC-DC 电源，并支持外部辅助电源输入，二者自动切换。

- 使用 5V 外部辅助电源时，输出端口优先使用外部电源供电，总输出能力受外部电源限制。每个接口均配有独立的板载自恢复保险丝，限流 500mA。
- 当未外接外部电源时，板载隔离 DC-DC 电源将生成 5V 供电，总输出能力受隔离 DC-DC 电源和上行 USB 端口共同限制。

请注意，外部辅助电源不得与上行 USB 端口连接至同一设备，否则会导致隔离失效。

### 器件选型建议

测试完成后将更新相关内容。