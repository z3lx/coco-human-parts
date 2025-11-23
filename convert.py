import argparse
import json
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Optional, Union


def convert(
    input_path: str,
    output_path: str,
    coco_path: Optional[str] = None
) -> None:
    def parse_float(s: str) -> Union[int, float]:
        d = Decimal(s)
        return int(d) if d == d.to_integral_value() else float(d)

    with open(input_path, "r", encoding="utf-8") as f:
        input_data = json.load(f, parse_float=parse_float)

    if coco_path:
        with open(coco_path, "r", encoding="utf-8") as f:
            coco_data = json.load(f, parse_float=parse_float)
    else:
        coco_data = None

    info = {
        "year": 2020,
        "version": "1.0",
        "description": "COCO Human Parts Dataset",
        "contributor": "COCO Consortium, Yang et al.",
        "url": "https://doi.org/10.1109/tip.2020.3029901",
        "date_created": date.today().strftime("%Y/%m/%d")
    }

    images = coco_data["images"] if coco_data else [
        {
            "id": image["id"],
            "width": image["width"],
            "height": image["height"],
            "file_name": image["file_name"],
            "license": None,
            "flickr_url": None,
            "coco_url": None,
            "date_captured": None
        }
        for image in input_data["images"]
    ]

    image_id_map = {
        image["id"]: (
            int(Path(image["file_name"]).stem)
            if coco_data else image["id"]
        )
        for image in input_data["images"]
    }

    annotations = []
    for annotation in input_data["annotations"]:
        def append_annotation(
            category_id: int,
            x: int,
            y: int,
            width: int,
            height: int
        ) -> None:
            annotations.append({
                "id": len(annotations) + 1,
                "image_id": image_id_map[annotation["image_id"]],
                "category_id": category_id,
                "segmentation": [],
                "area": width * height,
                "bbox": [x, y, width, height],
                "iscrowd": 0
            })

        append_annotation(
            category_id=1,
            x=annotation["bbox"][0],
            y=annotation["bbox"][1],
            width=annotation["bbox"][2],
            height=annotation["bbox"][3]
        )

        hier_count, hier_size = 6, 5
        for i in range(hier_count):
            hier = annotation["hier"]
            hier_index = i * hier_size
            if hier[hier_index + 4] == 0:
                continue
            append_annotation(
                category_id=i + 2,
                x=hier[hier_index + 0],
                y=hier[hier_index + 1],
                width=hier[hier_index + 2] - hier[hier_index + 0],
                height=hier[hier_index + 3] - hier[hier_index + 1]
            )

    categories = input_data["categories"]

    licenses = coco_data["licenses"] if coco_data else []

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
    parser.add_argument("--include", dest="coco_path", default=None)
    args = parser.parse_args()
    convert(**vars(args))
