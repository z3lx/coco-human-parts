import argparse
import json
import os
from datetime import date

from PIL import Image


def convert(input_path: str, output_path: str, image_directory: str) -> None:
    info = {
        "year": 2018,
        "version": "1.0",
        "description": "CrowdHuman",
        "contributor": "Shao et al.",
        "url": "https://www.crowdhuman.org/",
        "date_created": date.today().strftime("%Y/%m/%d")
    }

    images = []

    annotations = []

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)

        file_name = f"{data['ID']}.jpg"
        image_path = os.path.join(image_directory, file_name)
        with Image.open(image_path) as img:
            width, height = img.size
        image_id = len(images) + 1

        image_entry = {
            "id": image_id,
            "width": width,
            "height": height,
            "file_name": file_name,
            "license": None,
            "flickr_url": None,
            "coco_url": None,
            "date_captured": None,
        }
        images.append(image_entry)

        gtboxes = data["gtboxes"]
        for gtbox in gtboxes:
            tag = gtbox["tag"]
            if tag != "person":
                continue

            box_mappings = [
                (1, "vbox"),
                (2, "fbox"),
                (3, "hbox"),
            ]

            for category_id, box_key in box_mappings:
                bbox = gtbox[box_key]
                width, height = bbox[2], bbox[3]
                area = width * height
                annotation_id = len(annotations) + 1

                annotation = {
                    "id": annotation_id,
                    "image_id": image_id,
                    "category_id": category_id,
                    "segmentation": [],
                    "area": area,
                    "bbox": bbox,
                    "iscrowd": 0,
                }
                annotations.append(annotation)

    categories = [
        {"id": 1, "name": "person", "supercategory": "person"},
        {"id": 2, "name": "person_full", "supercategory": "person"},
        {"id": 3, "name": "head", "supercategory": "person"},
    ]

    licenses = []

    converted = {
        "info": info,
        "images": images,
        "annotations": annotations,
        "categories": categories,
        "licenses": licenses
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(converted, f, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    parser.add_argument("--include", dest="image_directory")
    args = parser.parse_args()
    convert(**vars(args))
