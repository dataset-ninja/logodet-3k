import supervisely as sly
import os
import xml.etree.ElementTree as ET
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_name_with_ext, get_file_ext
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    batch_size = 500

    dataset_path = "LogoDet-3K"

    errors_pathes = ['LogoDet-3K/Food/Indomie Mi goreng/Indomie Mi goreng_8.jpg', 'LogoDet-3K/Food/Cream of Wheat/Cream of Wheat_1.jpg', 'LogoDet-3K/Food/Cream of Wheat/Cream of Wheat_2.jpg', 'LogoDet-3K/Food/Amora/Amora_0.jpg']
    errors = ['Indomie Mi goreng_8.jpg', 'Cream of Wheat_1.jpg', 'Cream of Wheat_2.jpg', 'Amora_0.jpg']

    def create_ann(image_path):
        tags = []
        labels = []

        path2img, img_name = os.path.split(image_path)
        path2sub, _ = os.path.split(path2img)
        subfolder = os.path.basename(path2sub).lower()
        tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == subfolder]

        if get_file_name_with_ext(image_path) in errors:
            mask_np = sly.imaging.image.read(image_path)
            img_height = mask_np.shape[0]
            img_wight = mask_np.shape[1]
            return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)
        

        ann_name = f"{get_file_name(img_name)}.xml"
        ann_path = os.path.join(path2img, ann_name)
        tree = ET.parse(ann_path)
        root = tree.getroot()
        img_height = int(root.find(".//height").text)
        img_wight = int(root.find(".//width").text)
        objects_content = root.findall(".//object")

        for obj_data in objects_content:
            name = obj_data.find(".//name").text
            name = "_".join(name.split()).lower()
            obj_class = meta.get_obj_class(name)
            bndbox = obj_data.find(".//bndbox")
            top = int(bndbox.find(".//ymin").text)
            left = int(bndbox.find(".//xmin").text)
            bottom = int(bndbox.find(".//ymax").text)
            right = int(bndbox.find(".//xmax").text)
            rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
            label = sly.Label(rectangle, obj_class)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    tags = os.listdir(dataset_path)

    tag_metas = [sly.TagMeta(name.lower(), sly.TagValueType.NONE) for name in tags]

    obj_classes = []
    image_pathes = []

    for r, d, f in os.walk(dataset_path):
        for dir in d:
            if dir not in tags:
                dir = "_".join(dir.split())
                obj_class = sly.ObjClass(dir.lower(), sly.Rectangle)
                obj_classes.append(obj_class)
        for file in f:
            old_path = os.path.join(r, file)
            old_name = get_file_name(file)
            if os.path.basename(r) not in old_name:
                file_ext = get_file_ext(file)
                new_name = f"{os.path.basename(r)}_{old_name}{file_ext}"
                new_path = os.path.join(r, new_name)
                os.rename(old_path, new_path)
            else:
                new_path = old_path
            if file.endswith(".jpg"):
                image_pathes.append(new_path)
            
    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=obj_classes, tag_metas=tag_metas)
    api.project.update_meta(project.id, meta.to_json())

    ds_name = "ds"

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    progress = sly.Progress("Create dataset {}".format(ds_name), len(image_pathes))

    for img_pathes_batch in sly.batched(image_pathes, batch_size=batch_size):
        images_names_batch = [
            get_file_name_with_ext(image_path) for image_path in img_pathes_batch
        ]

        img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns_batch = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns_batch)

        progress.iters_done_report(len(images_names_batch))

    return project
