[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# IconMatch

Part of the Hands Free Computing project. This subproject aims to allow a user to easily select icons on the screen in any environment.

## Table of Contents

- [IconMatch](#iconmatch)
  - [Table of Contents](#table-of-contents)
  - [About The Project](#about-the-project)
    - [Built With](#built-with)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Roadmap](#roadmap)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## About The Project

[![Showcasing bounding boxes and original image][product-screenshot]](https://luiszugasti.me)

### Built With

- [OpenCV 3.12](https://opencv.org)
- [Python 3.8](https://python.org)

## Getting Started 

### Prerequisites

Refer to the [requirements.txt](https://github.com/luiszugasti/IconMatch/blob/main/requirements.txt) file.

### Installation

Clone this repository to your computer.  
Install the project using Python 3.8; then install the requirements in the requirements.txt file.  
A sample demo of how the engine works so far can be found within the icondetection module.

## Usage

You can use (box.py)[https://github.com/luiszugasti/IconMatch/blob/main/icondetection/box.py] as a default entry point.

In the below example, the main set of functions is called within a callback function, as this allows the threshold value
to be controlled from a GUI in OpenCV.

    def threshold_callback(val):
    """
    Function modified from this tutorial:
    Takes a value of threshold for the canny edge detector and finds the
    bounding rectangles of appropriate edges within an image.
    """

    # accept an input image and convert it to grayscale, and blur it
    gray_scale_image = grayscale_blur(src)

    # determine the bounding rectangles from canny detection
    _, bound_rect = canny_detection(gray_scale_image, min_threshold=val)

    # group the rectangles from this step
    grouped_rects = group_rects(bound_rect, 0, src.shape[1])

    # (for display purposes) use the provided rectangles to display in your program
    _render_rectangles(grouped_rects, bound_rect, src)


## Roadmap

Currently focusing on detection of "icon-like" objects on the screen.

Next steps are to provide context into detected icons for easier usage of the computer.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Luis Zugasti - [@luis\_\_zugasti](https://twitter.com/luis__zugasti)

Project Link: [https://github.com/luiszugasti/IconMatch](https://github.com/luiszugasti/IconMatch)

[contributors-shield]: https://img.shields.io/github/contributors/luiszugasti/IconMatch.svg?style=flat-square
[contributors-url]: https://github.com/luiszugasti/IconMatch/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/luiszugasti/IconMatch.svg?style=flat-square
[forks-url]: https://github.com/luiszugasti/IconMatch/network/members
[stars-shield]: https://img.shields.io/github/stars/luiszugasti/IconMatch.svg?style=flat-square
[stars-url]: https://github.com/luiszugasti/IconMatch/stargazers
[issues-shield]: https://img.shields.io/github/issues/luiszugasti/IconMatch.svg?style=flat-square
[issues-url]: https://github.com/luiszugasti/IconMatch/issues
[license-shield]: https://img.shields.io/github/license/luiszugasti/IconMatch.svg?style=flat-square
[license-url]: https://github.com/luiszugasti/IconMatch/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/luiszugasti
[product-screenshot]: https://i.imgur.com/Q4Rm7M6.png
