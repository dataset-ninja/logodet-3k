The **LogoDet-3K: A Large-Scale Image Dataset for Logo Detection** is a significant contribution to the logo detection, with broad applications in multimedia such as copyright infringement detection, brand visibility monitoring, and product brand management on social media. It features 3,000 logo categories, approximately 200,000 manually annotated logo objects, and 158,652 images, sets a new standard for logo detection benchmarks. The authors detail the dataset construction process, including logo image collection, filtering, and object annotation. The dataset is divided into nine super-classes based on daily life needs and common enterprise positioning.

For the construction of LogoDet-3K, the authors followed a meticulous three-step process, involving logo image collection, logo image filtering, and logo object annotation. Each image was thoroughly examined and reviewed to ensure the dataset's quality after filtering and annotation.

## Logo image collection

During the phase, it was compiled a comprehensive logo list based on various reputable sources, resulting in a vocabulary of 3,000 logo names spanning nine super-classes: **sports**, **leisure**, **transportation**, **food**, **electronic**, **necessities**, **clothes**, **medical**, **others**. Images were then retrieved from search engines using these names as queries. The dataset creation process involved manual cleaning and filtering to ensure data quality, including the removal of images with unsuitable sizes or extreme aspect ratios and those without logos.

| Root Category    | Sub-Category    | Images | Objects |
| ---------------- | --------------- | ------ | ------- |
| Food             | 932             | 53,350 | 64,276  |
| Clothes          | 604             | 31,266 | 37,601  |
| Necessities      | 432             | 24,822 | 30,643  |
| Others           | 371             | 15,513 | 20,016  |
| Electronic       | 224             | 9,675  | 12,139  |
| Transportation   | 213             | 10,445 | 12,791  |
| Leisure          | 111             | 5,685  | 6,573   |
| Sports           | 66              | 3,945  | 5,041   |
| Medical          | 47              | 3,945  | 5,185   |
| Total            | 3,000           | 158,652| 194,261 |


## Logo object annotation

During the process a considerable amount of time was required. The resulting LogoDet-3K dataset consists of 3,000 logo classes, 158,652 images, and 194,261 logo objects. The dataset exhibits imbalanced distributions across different logo categories, presenting a challenge for effective logo detection, particularly for categories with fewer samples. The statistics at the superclass and category levels illustrate this imbalance.

<img src="https://github.com/supervisely/dataset-tools/assets/78355358/bd990d73-5e53-4fa8-a2fe-1fbd35dcc39b" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Multiple logo categories for some brands, where a distinction between these logo categories via adding the suffix ‘-1’, ‘-2’.</span>

Additionally, the authors provide insights into the distribution of images and categories in LogoDet-3K, highlighting the challenges posed by imbalances across different logo objects and images. The dataset is characterized by a large percentage of small and medium logo objects, creating additional challenges for logo detection, as smaller logos are inherently harder to detect.

<img src="https://github.com/supervisely/dataset-tools/assets/78355358/354d6a3b-f33d-4597-95a1-78376044c470" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Sorted distribution of images for each logo in LogoDet-3K.</span>

The dataset's statistics further detail the distribution of logo categories, images, and logo objects across nine super-classes, revealing variations in sizes and numbers. Notably, the Food, Clothes, and Necessities classes exhibit larger numbers of objects and images compared to other classes in the dataset.

<img src="https://github.com/supervisely/dataset-tools/assets/78355358/c6956782-9b83-4986-bbf8-a7aefe2fe681" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">The detailed statistics of LogoDet-3K about Image and object distribution in per category, the number of objects in per image and object size in per image.</span>

<img src="https://github.com/supervisely/dataset-tools/assets/78355358/8e32b371-b130-485e-817b-b058de87a81c" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Distributions of categories, images and objects from LogoDet-3K on super-classes.</span>
