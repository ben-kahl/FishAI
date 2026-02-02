<a id="readme-top"></a>

<br />
<div align="center">
<h3 align="center">FishAI</h3>

  <p align="center">
    A fully fledged AI powered assistant running on a Big Mouth Billy Bass! <br />
    FishAI has evolved into a hybrid edge/cloud IoT device. The "Fish" (Client) runs on a Raspberry Pi with vision and audio processing, while the "Brain" (Server) runs in the cloud (or locally) handling intelligence, state, and complex logic.
  </p>
</div>


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
        <li><a href="#hardware-prerequisites">Hardware Prerequisites</a></li>
        <li><a href="#software-architecture">Software Architecture</a></li>
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



## About The Project

What started as a silly summer project to clone GPTARS.ai has evolved into a possibly over-engineered IoT platform. The project now utilizes a **Client-Server architecture**:

1.  **The Fish (Client):** A Raspberry Pi 4b inside the fish that handles:
    * **Wake Word Detection:** Uses Picovoice Porcupine to listen for keywords.
    * **Vision:** Captures images via a connected camera to send to the AI.
    * **Animatronics:** Controls the mouth, head, and tail via H-Bridges.
    * **Audio:** Plays responses using `mpg123`.
    * **Health Monitoring:** Reports CPU/Temp stats to the dashboard.

2.  **The Brain (Cloud/Server):** A Flask-based backend (deployable to AWS App Runner via Terraform) that handles:
    * **Intelligence:** Google Gemini Flash 2.5 for multimodal understanding (Text + Image).
    * **Speech:** ElevenLabs for voice synthesis.
    * **State Management:** Redis for command queuing (movements, speech) and health status.

3.  **The Dashboard:** A Next.js web application for configuring personalities, monitoring device health, and manual control.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* **Hardware Control:** Python, OpenCV (Computer Vision)
* **AI Services:** Google Gemini, Picovoice, ElevenLabs
* **Backend:** Flask, Redis, Docker
* **Frontend:** Next.js, React, TypeScript
* **Infrastructure:** AWS (App Runner, ECR), Terraform

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Getting Started

Because the project is split into three parts (Client, Server, Dashboard), setup is a bit more involved than before.

### Hardware Prerequisites

* Raspberry Pi (4b recommended)
* Big Mouth Billy Bass
* **Camera:** USB Webcam or Pi Camera (for vision capabilities)
* **Microphone:** INMP441 MEMS mic or USB mic
* 2 H-Bridges (for motor control)
* 9V battery/power supply
* Speaker/Audio output

### Installation

1.  **Get API Keys**
    You will need keys for: **Google Gemini**, **ElevenLabs**, and **Picovoice**.

2.  **Clone the Repo**
    ```sh
    git clone [https://github.com/ben-kahl/FishAI.git](https://github.com/ben-kahl/FishAI.git)
    cd FishAI
    ```

#### Part 1: The Server (Cloud/Local)
You can run the server locally or deploy it to AWS.

* **Local Run:**
    Ensure you have a local Redis instance running (`redis-server`).
    ```sh
    cd cloud
    pip install -r cloud_requirements.txt
    python server.py
    ```

* **AWS Deployment:**
    Infrastructure is managed via Terraform.
    ```sh
    cd cloud
    # Ensure AWS credentials are set
    terraform init
    terraform apply
    ```

#### Part 2: The Fish (Raspberry Pi)
Run this on the Raspberry Pi.

1.  Install system dependencies:
    ```sh
    sudo apt-get install mpg123 libatlas-base-dev
    ```
2.  Install Python dependencies:
    ```sh
    cd client
    pip install -r client_requirements.txt
    ```
3.  Configure Environment:
    Create a `.env` file in the `client/` directory:
    ```env
    PICOVOICE_API_KEY=<YOUR_KEY>
    CLOUD_URL=http://<YOUR_SERVER_IP>:5000
    MICROPHONE_INDEX=0
    CAMERA_INDEX=0
    ```
4.  Start the Client:
    ```sh
    python main.py
    ```

#### Part 3: The Dashboard (Optional)
A web interface to control the fish.

1.  Navigate to dashboard:
    ```sh
    cd fish-dashboard
    ```
2.  Install and Run:
    ```sh
    npm install
    npm next dev
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Usage

Once everything is running:

1.  **Voice Control:** Say the wake word (default: "Jarvis" or similar, based on your `.ppn` file). The Fish will wake up, snap a picture of what it sees, listen to your query, and respond using Gemini's multimodal capabilities.
2.  **Web Control:** Open the Next.js dashboard to:
    * Change the Fish's "Personality" (e.g., Sarcastic, Pirate, Helpful).
    * View live health stats (Temperature, CPU load).
    * Manually send text queries.
    * Control volume.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Roadmap

- [x] Voice to Audio AI response Pipeline
- [x] **Vision Capabilities:** The fish can now "see" you.
- [x] **Cloud Infrastructure:** Terraform + AWS App Runner support.
- [x] **Web Dashboard:** Full Next.js control panel.
- [x] **Personality Engine:** Dynamic personality switching via Redis.

See the [open issues](https://github.com/ben-kahl/FishAI/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Contact

Ben Kahl - [linkedin-url](https://www.linkedin.com/in/ben-kahl/)

Project Link: [https://github.com/ben-kahl/FishAI](https://github.com/ben-kahl/FishAI)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
