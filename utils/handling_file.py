import os
import shutil
import glob
import datetime


def remove_outdated_files():
    remove_date = datetime.date.today() - datetime.timedelta(days=1)
    img_dir_path = r"static/images/{}".format(str(remove_date))
    vid_dir_path = r"static/videos/{}".format(str(remove_date))
    if os.path.exists(img_dir_path):
        shutil.rmtree(img_dir_path)
    if os.path.exists(vid_dir_path):
        shutil.rmtree(vid_dir_path)


def get_detected_images():
    images_path = os.path.join(os.getcwd(
    ), "static", "images", datetime.datetime.now().strftime('%Y-%m-%d'), "*.jpeg")
    images = glob.glob(images_path)
    images = sorted(images)

    file_list = []
    for image in images:
        file_name_splited = os.path.split(image)
        _, file_name = file_name_splited[-2], file_name_splited[-1]
        file_list.append(
            "images/{}/".format(datetime.datetime.now().strftime('%Y-%m-%d')) + file_name)

    return file_list
