<a id="readme-top"></a>

[![LinkedIn][linkedin-shield]][https://www.linkedin.com/in/ben-kahl/]

<br />
<div align="center">
<h3 align="center">FishAI</h3>

  <p align="center">
    A fully fledged AI powered assitant running on a Big Mouth Billy Bass! FishAI runs a web based configuration and testing site alongside a voice powered response pipeline all on a Raspberry Pi 4b. It utilizes Picovoice Porcupine for wake word detection, Picovoice Leopard for speech to text transcription, Google Gemini Flash 2.5 for responses, and ElevenLabs for voice synthesis.
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a silly little summer project that I got the idea for after seeing GPTARS.ai on Youtube make this and stumbling across a Big Mouth Billy Bass at a thrift store. As his code and process aren't available online, I decided to make my own open-source version.
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python
* Google Gemini
* Picovoice
* Elevenlabs
* A Fish

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

To get started, you'll need a few hardware and software components

#### Hardware
* Rasberry Pi (I used a 4b 2gb, but it should work on anything newer than a Pi 3)
* Big Mouth Billy Bass (Or a animitronic of your choice)
* Microphone (I used a INMP441 MEMS mic, but a usb mic should work too)
* 2 H-Bridges
* 9 volt battery/battery pack
* Jumper wires for connecting everything together

#### Software
* The latest version of Raspbian
* Python 3

### Installation

1. Get API keys for Google Gemini, ElevenlabsAI, and Picovoice
2. Clone the repo
   ```sh
   git clone https://github.com/ben-kahl/FishAI.git
   ```
3. Everything you need software-wise is included in requirements.txt, so go ahead and pip install that as shown below.
  pip
  ```sh
  pip install -r requirements.txt
  ```
4. Enter your API keys in your own `.env`
   ```python
   ELEVENLABS_API_KEY=<YOUR_ELEVENLABS_API_KEY>
   GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
   PICOVOICE_API_KEY=<YOUR_PICOVOICE_API_KEY>
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin <your_github_username>/<your_repo>
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To start the project, run the following command
```sh
   python main.py
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [O] Voice to Audio AI response Pipeline
- [In-Progress] Website to configure settings and manually input queries
- [In-Progress] Fully fledged fish speech and listening animations

See the [open issues](https://github.com/ben-kahl/FishAI/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ben Kahl - [linkedin-url](https://www.linkedin.com/in/ben-kahl/)

Project Link: [https://github.com/ben-kahl/FishAI](https://github.com/ben-kahl/FishAI)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Thank you to GPTARS.ai for the idea!

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/ben-kahl/FishAI.svg?style=for-the-badge
[contributors-url]: https://github.com/ben-kahl/FishAI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ben-kahl/FishAI.svg?style=for-the-badge
[forks-url]: https://github.com/ben-kahl/FishAI/network/members
[stars-shield]: https://img.shields.io/github/stars/ben-kahl/FishAI.svg?style=for-the-badge
[stars-url]: https://github.com/ben-kahl/FishAI/stargazers
[issues-shield]: https://img.shields.io/github/issues/ben-kahl/FishAI.svg?style=for-the-badge
[issues-url]: https://github.com/ben-kahl/FishAI/issues
[license-shield]: https://img.shields.io/github/license/ben-kahl/FishAI.svg?style=for-the-badge
[license-url]: https://github.com/ben-kahl/FishAI/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ben-kahl
