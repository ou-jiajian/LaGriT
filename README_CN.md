## LaGriT: 洛斯阿拉莫斯网格工具箱 ##

**LANL软件: LA-CC-15-069 编号 C15097**

[![最新版本](https://img.shields.io/github/release/lanl/lagrit.svg?style=flat-square)](https://github.com/lanl/lagrit/releases) [![PyPI](https://img.shields.io/pypi/l/Django.svg)](https://lanl.github.io/LaGriT/pages/licensing.html)

[![dockerhub](https://img.shields.io/static/v1?label=Docker&message=下载%20V3.3.3&color=blue&style=for-the-badge&logo=docker)](https://hub.docker.com/r/ees16/lagrit) <br/>
[![readthedocs](https://img.shields.io/static/v1?label=文档&message=在线阅读&color=blue&style=for-the-badge&logo=read-the-docs)](https://lanl.github.io/LaGriT/) <br/>
[![readthedocs](https://img.shields.io/static/v1?label=LaGriT主页&message=在线阅读&color=blue&style=for-the-badge&logo=read-the-docs)](https://lagrit.lanl.gov/) <br/>
[![readthedocs](https://img.shields.io/static/v1?label=网格生成组合&message=在线阅读&color=blue&style=for-the-badge&logo=read-the-docs)](https://meshing.lanl.gov/) <br/>


> [!注意]
> 我们目前正在开发3D泊松盘功能。


洛斯阿拉莫斯网格工具箱（**LaGriT**）是一个用户可调用工具库，提供二维和三维的网格生成、网格优化和动态网格维护功能。LaGriT用于各种地质和地球物理建模应用，包括多孔流动和传输模型构建、地壳断层系统应力/应变的有限元建模、地震学、离散裂缝网络、小行星和热液系统。

LaGriT的通用功能也可以用于地球科学应用之外，并应用于几乎任何需要网格/网格和初始边界条件、材料属性设置和其他模型设置功能的系统。它也可以用作预处理和后处理以及分析顶点和基于网格数据的工具。

**PyLaGriT**是LaGriT的Python接口，允许从Python交互式和批处理模式访问LaGriT功能。
这允许将LaGriT的网格生成功能与Python的数值和科学功能相结合。
PyLaGriT允许交互式和自动查询网格属性、增强的循环功能以及基于LaGriT输出的用户定义错误检查。

---

### 快速开始

#### Docker容器

开始使用LaGriT最简单的方法是通过[Docker](https://hub.docker.com/r/ees16/lagrit)：

    $ docker pull ees16/lagrit:latest
    $ docker run -it -v $(pwd):/docker_user/work ees16/lagrit:latest

容器启动后，导航到：

    $ cd bin
    $ ./lagrit

---

### 构建LaGriT

#### 依赖项 ####

- 使用CMake生成构建系统。
- C、C++和兼容的Fortran编译器。MacOS可能需要更新命令行工具。
- 可选：在TPLs中安装Exodus库，需要bash和wget。

**注意：** 使用任何Brew安装的编译器和Gnu 10-12时，泊松盘命令存在问题。在Clang 14-15和Gnu 9.4上工作正常。

#### 下载LaGriT ####

通过运行以下命令下载Https仓库：

```bash
git clone https://github.com/lanl/LaGriT.git
cd LaGriT/
```

注意：对于开发者，您需要SSH版本才能启用Git版本控制到此仓库。

[使用cmake和exodus构建LaGriT的详细说明](cmake/README.md)


构建LaGriT最简单的方法是使用cmake进行自动检测且无选项。
输入以下内容（您可以将构建目录命名为任何您想要的名称）。

```bash
mkdir build/ && cd build/
cmake .. && make
```

cmake命令创建lagrit的配置和构建文件，看起来类似于这样：
```
-- ==========================================
-- ============配置LaGriT============
-- ===================v3.3.3=================
-- 将LaGriT编译为静态二进制文件 = ON
-- 使用ExodusII编译LaGriT = OFF
LaGriT编译时不支持ExodusII。

-- 配置完成
-- 生成完成
```

make命令将编译库并构建lagrit。使用`make VERBOSE=1`查看编译进度。
`lagrit`可执行文件安装在`build/`目录中。


- 输入`./lagrit`确保可执行文件正常工作。
- 在LaGriT命令行中输入`test`，这将执行一组LaGriT命令。
- 输入`finish`退出。

结果将如下所示：
```
nnodes:              27                                                         
nelements:            8                                                         
xic(1:3):  1.00 1.25 1.50                                                       
imt(1:3):     1    1    1                                                       
epsilonl:   1.9229627E-13                                                       
     Released Mesh Object: test_hex                                             
lagrit test done.                                                               
 
 Enter a command
finish                                                                          
LaGriT successfully completed             
```

### 测试LaGriT

要测试LaGriT，从顶部开始并简单运行：

```bash
$ python test/runtests.py
```

测试输出可以在`test/lagrit-tests.log`文件中找到。

通过运行以下命令可以获得其他选项：

```bash
$ python test/runtests.py --help
```


### （可选）使用ExodusII构建LaGriT ###


唯一使用ExodusII库的LaGriT命令是`dump/exodus`和相关的面集和节点集命令。
要包含这些命令，您需要安装Seacas-Exodus。

使用install-exodus.sh或MAC_install-exodus.sh安装Exodus和相关库。您可以运行文件或使用文件作为指南来复制和粘贴安装命令。脚本提供LaGriT所需的标志，并将seacas安装在TPLs目录中。

有关完整和当前的Exodus安装说明，请访问：
[Seacas ExodusII](https://github.com/sandialabs/seacas)

使用脚本安装、配置和构建ExodusII（对于mac机器使用MAC_install-exodus.sh）：

```bash
$ ./install-exodus.sh
```

使用ExodusII库配置和构建LaGriT：

```bash
mkdir build/ && cd build/
cmake .. -DLAGRIT_BUILD_EXODUS=ON
make
```

[使用cmake和exodus构建LaGriT的详细说明](cmake/README.md)


### CMake构建选项

您可以在CMakeLists.txt文件中进行更改，但您的构建目录必须为空才能使全局变量生效。这些选项在命令行中可用，并将更新cmake全局变量。

要使用cmake选项，请使用-D，如本示例所示：

```bash
mkdir dir_name/ && cd dir_name/
cmake .. -DCMAKE_BUILD_TYPE=Debug -DLAGRIT_BUILD_EXODUS=ON
make
```

- `-D CMAKE_BUILD_TYPE`
  - 设置构建类型。在`Debug`和`Release`之间选择。
- `-D LAGRIT_BUILD_EXODUS=ON`
  - 如果已安装，则使用ExodusII构建LaGriT。
- `-D CMAKE_INSTALL_PREFIX`
  - 设置运行`make install`时安装LaGriT的位置。默认为`/usr/local/`。
- `-D LaGriT_BUILD_STATIC`
  - 将LaGriT构建为静态二进制文件（默认；`ON`）或共享库（`.so`、`.dylib`、`.dll`）

### 支持文档 ###
---
* [LaGriT文档](https://lanl.github.io/LaGriT/)
* [PyLaGriT文档](https://lanl.github.io/LaGriT/pylagrit/original/index.html)
* [lagrit.lanl.gov: 网页](http://lagrit.lanl.gov)
* [外部协作者的贡献协议](CONTRIBUTING.md)
* [版权许可证](LICENSE.md)
* [使用cmake进行代码开发](cmake/README.md)
* [旧版LaGriT V2安装](documentation/INSTALL.md)

![细化样本](screenshots/refine_samples_TN1000.png)

##### LaGriT网格图像位于 https://meshing.lanl.gov/proj/screenshots/GRID_GALLERY.html 