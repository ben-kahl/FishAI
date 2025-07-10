async function sendFishCommand(action) {
  const statusMessageDiv = document.getElementById('status-message');
  statusMessageDiv.textContent = 'Status: Sending fish command...';

  try {
    const response = await fetch('/control_fish', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `action=${action}`
    });

    if (response.ok) {
      const message = await response.text();
      statusMessageDiv.textContent = `Status: ${message}`;
    } else {
      const errorText = await response.text();
      statusMessageDiv.textContent = `Status: Error - ${response.status} ${response.statusText} (${errorText})`;
    }
  } catch (error) {
    statusMessageDiv.textContent = `Status: Network Error - ${error}`;
  }
}

async function sendGeminiCommand() {
  const statusMessageDiv = document.getElementById('status-message');
  const geminiInput = document.getElementById('gemini-input');
  const userText = geminiInput.value;

  if (!userText.trim()) {
    statusMessageDiv.textContent = 'Status: Please enter some text for Gemini.';
    return;
  }

  statusMessageDiv.textContent = 'Status: Sending text to Gemini...';

  try {
    const response = await fetch('/ask_gemini', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `user_text=${encodeURIComponent(userText)}` // Encode the text for URL safety
    });

    if (response.ok) {
      const message = await response.text();
      statusMessageDiv.textContent = `Status: ${message}`;
      geminiInput.value = ''; // Clear the textbox
    } else {
      const errorText = await response.text();
      statusMessageDiv.textContent = `Status: Error - ${response.status} ${response.statusText} (${errorText})`;
    }
  } catch (error) {
    statusMessageDiv.textContent = `Status: Network Error - ${error}`;
  }
}


async function sendElevenLabsCommand() {
  const statusMessageDiv = document.getElementById('status-message');
  const elevenInput = document.getElementById('elevenlabs-input');
  const userText = elevenInput.value;

  if (!userText.trim()) {
    statusMessageDiv.textContent = 'Status: Please enter some text for ElevenLabs.';
    return;
  }

  statusMessageDiv.textContent = 'Status: Sending text to Elevenlabs...';

  try {
    const response = await fetch('/test_elevenlabs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `user_text=${encodeURIComponent(userText)}` // Encode the text for URL safety
    });

    if (response.ok) {
      const message = await response.text();
      statusMessageDiv.textContent = `Status: ${message}`;
      elevenInput.value = ''; // Clear the textbox
    } else {
      const errorText = await response.text();
      statusMessageDiv.textContent = `Status: Error - ${response.status} ${response.statusText} (${errorText})`;
    }
  } catch (error) {
    statusMessageDiv.textContent = `Status: Network Error - ${error}`;
  }
}
