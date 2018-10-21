from pixivpic import PicGet
from picup import PicUp
from mspost import Post


def main():
    Get = PicGet()
    Up = PicUp()
    Po = Post()

    while True:
        a = input("1-顺序执行 2-下载图片 3-上传图片 4-发表文章 5-结束程序: ")
        if a == '1':
            Get.Key()
            Get.login()
            Get.dailypic()
            y = input('请确认每张图片都小宇4MB,y-继续 n-返回')
            if y == 'y':
                Up.up()
                Up.saveUpData()
            elif y == 'n':
                continue
            Po.message()
            Po.messagePost()

        if a == '2':
            Get.Key()
            Get.login()
            Get.dailypic()

        if a == '3':
            Up.up()
            Up.saveUpData()

        if a == '4':
            Po.message()
            Po.messagePost()

        if a == '5':
            break


if __name__ == "__main__":
    main()
