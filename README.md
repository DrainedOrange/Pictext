# Pictext
###### DrainedOrange 2025.1.1
Pictext是一个将指定图片和文章融合，并导出字格图的小程序。整个程序大致分为以下三个部分。
* **PART 1** - 将图片色块化，转换为合适的、带有RGB颜色信息的空网格。
* **PART 2** - 用文章中的字段填充网格，导出待打印信息。
* **PART 3** - 打印并导出PDF。

## 待解决问题
- [ ] PART 3 中的`read_to_print_strings()`有问题。
- [ ] 填充方式效率太低。
- [ ] pyplot里的fontsize规定得很奇怪。