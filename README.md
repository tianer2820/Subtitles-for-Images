# 自动图片字幕
这个项目用来给漫画自动加字幕，或者说是台词。

## 安装说明
这个项目需要安装pillow。之后直接运行main.py就可以了

## 使用
把需要加字幕的图片放到imgs文件夹里，编辑台词和颜色文件，
准备好后运行main.py，按照指示操作即可。输出文件会出现在
products文件夹里

## 设置
所有设置文件请用utf8编码

### 配置文件
settings.txt里包含所有的设置。

settings.txt中每一行是一个设置项，用#开头表示这一行是注释。
用key=value的方式赋值，允许空行。其中working folder是工作文件夹，所有其他的文件位置都是相对这个文件夹的。

### 台词文件
这个文件用来提供要加到图片上的台词。

台词用换行来分割，一行角色姓名，下一行是角色台词。中间的任何空行会被忽略。
页与页之间用分割行来分割，分隔行需要以"---"开始，并以"---"结束，中间可以有任何字符，建议使用文件名做标注。

最后一页后面不要加横线

### 颜色文件
颜色文件用来自动为不同角色的台词添加不同的颜色。如果角色名称不在这个文件里，台词会用默认颜色显示。

颜色设置和settings文件很像，名字=颜色。颜色可以是'(r, g, b)'格式，'#RRGGBB'的16进制格式，也可以是颜色名称，例如'white'， 但颜色名称支持并不完善，可能会出现意外情况（比如无法识别这个颜色），可能的话尽量使用前两个。

在写好台词文件之后可以用generate_color_file.py自动生成颜色配置文件。这个脚本不会删除已经存在的颜色配置，只会把新增的名字设置为默认颜色。

## 输入输出格式
输出的文件最终会放到输出文件夹，不会覆盖原图。输入图片会按照文件名排序，然后从0开始计页数。输出文件格式是png，命名是0001.png 0002.png的格式。
