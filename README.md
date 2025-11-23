# COCO Human Parts

A minimal utility to convert the [COCO Body Parts annotations](https://github.com/soeaver/Hier-R-CNN#dataset) into a valid COCO instance annotation file. See the [releases page](https://github.com/z3lx/coco-human-parts/releases/latest) for downloading the converted annotations.

> Note: The conversion flattens annotations. Hierarchical relations between the person class and individual body part classes are not preserved. Each body part becomes an independent bounding box annotation with its own `category_id`.

## Categories

| Name       | Id |  Train |   Val |
|:-----------|---:|-------:|------:|
| Person     |  1 | 257306 | 10777 |
| Head       |  2 | 223049 |  9351 |
| Face       |  3 | 153195 |  6913 |
| Left hand  |  4 |  96078 |  4222 |
| Right hand |  5 | 100205 |  4324 |
| Left foot  |  6 |  77997 |  3134 |
| Right foot |  7 |  77870 |  3100 |
| Total      |    | 985700 | 41821 |

| Image type |  Train |  Val |
|:-----------|-------:|-----:|
| Positive   |  64115 | 2693 |
| Negative   |  54172 | 2307 |
| Total      | 118287 | 5000 |


## Requirements

- Python 3.8+

No external dependencies beyond the standard library.

## Usage

```bash
python convert.py <input_path> <output_path> --include <coco_path>
```

Arguments:
- `input_path`: Path to the Human Parts JSON in Hier-R-CNN format (e.g., `person_humanparts_train2017.json`).
- `output_path`: Destination path for the converted JSON in COCO format.
- `--include <coco_path>` (optional): Path to an existing COCO annotations file (e.g., `instances_train2017.json`). When provided, dataset metadata and negative images are merged from this file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information. Upstream dataset licenses still apply.

## Citation

If you use these annotations, consider citing the Hier-R-CNN paper:

```
@article{9229236,
  author={Yang, Lu and Song, Qing and Wang, Zhihui and Hu, Mengjie and Liu, Chun},
  journal={IEEE Transactions on Image Processing},
  title={Hier R-CNN: Instance-Level Human Parts Detection and A New Benchmark},
  year={2021},
  volume={30},
  number={},
  pages={39-54},
  keywords={Annotations;Faces;Visualization;Proposals;Benchmark testing;Task analysis;Human parts detection;COCO human parts;region-based approach;Hier R-CNN},
  doi={10.1109/TIP.2020.3029901}
}
```
